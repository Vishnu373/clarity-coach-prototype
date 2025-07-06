import boto3
import time
import uuid
import os

class ScannedPdfPipeline:
    def __init__(self, file_path, bucket_name=None, region="us-east-1"):
        self.file_path = file_path
        self.region = region
        self.s3 = boto3.client('s3', region_name=region)
        self.textract = boto3.client('textract', region_name=region)
        
        self.bucket_name = f"scanned-pdf-temp-{uuid.uuid4().hex[:8]}"
        self.object_name = os.path.basename(file_path)
        self.job_id = None

    def create_bucket(self):
        print(f"Creating bucket: {self.bucket_name}")
        if self.region == "us-east-1":
            self.s3.create_bucket(Bucket=self.bucket_name)

        else:
            self.s3.create_bucket(
                Bucket=self.bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.region}
            )

    def upload_pdf(self):
        print(f"Uploading PDF: {self.file_path} to {self.bucket_name}")
        self.s3.upload_file(self.file_path, self.bucket_name, self.object_name)

    def start_job(self):
        print("Extracting...")
        response = self.textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': self.bucket_name,
                    'Name': self.object_name
                }
            }
        )
        self.job_id = response['JobId']

    def wait_for_completion(self):
        print("Waiting for Textract job to complete...")
        while True:
            response = self.textract.get_document_text_detection(JobId=self.job_id)
            status = response['JobStatus']
            print(f"Job Status: {status}")
            if status in ['SUCCEEDED', 'FAILED']:
                return status == 'SUCCEEDED'
            time.sleep(15)

    def get_results(self):
        print("Fetching extracted text...")
        pages = []
        key_value_pairs = []
        tables = []
        next_token = None

        while True:
            if next_token:
                response = self.textract.get_document_text_detection(
                    JobId=self.job_id, NextToken=next_token)
            else:
                response = self.textract.get_document_text_detection(JobId=self.job_id)

            for block in response['Blocks']:
                # Print text
                if block['BlockType'] == 'LINE':
                    pages.append(block['Text'])

                # Print key value pairs
                elif block['BlockType'] == 'KEY_VALUE_SET':
                    key_value_pairs.append(block)

                # Print tables
                elif block['BlockType'] == 'TABLE':
                    tables.append(block)       

            next_token = response.get('NextToken')
            if not next_token:
                break

        return {
            "pages": pages,
            "key_value_pairs": key_value_pairs,
            "tables": tables
        }

    def cleanup(self):
        print("Cleaning up S3 resources...")
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket(self.bucket_name)
        # Delete uploaded file
        bucket.Object(self.object_name).delete()
        # Delete bucket
        bucket.delete()
        print("Cleanup complete.")

    def run_pipeline(self):
        try:
            self.create_bucket()
            self.upload_pdf()
            self.start_job()

            if not self.wait_for_completion():
                raise Exception("Textract job failed.")

            extracted = self.get_results()

            return {
                "text": "\n".join(extracted["pages"]),  # Consistent with other pipelines
                "key_value_pairs": extracted["key_value_pairs"],
                "tables": extracted["tables"]
            }

        finally:
            self.cleanup()

"""
if __name__ == "__main__":
    pdf_path = "Robert Cooper resume (column type).pdf"
    pipeline = ScannedPdfPipeline(file_path=pdf_path)
    result = pipeline.run_pipeline()
    print("Extracted Text:\n", result)
"""
