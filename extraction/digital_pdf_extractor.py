import pdfplumber
import camelot
from collections import defaultdict
from io import BytesIO
from .preprocessing import preprocess_text
import tempfile
import os

class DigitalPDFPipeline:
    def __init__(self, file_bytes: bytes, y_tolerance=3):
        self.file_bytes = file_bytes
        self.y_tolerance = y_tolerance
        self.text_by_page = []
        self.cleaned_text = ""
        self.tables = []

    def extract_text(self):
        clustered_lines = []

        with pdfplumber.open(BytesIO(self.file_bytes)) as pdf:
            for page_index, page in enumerate(pdf.pages):
                words = page.extract_words()

                # 1. Get table bounding boxes
                table_bboxes = []
                try:
                    table_settings = {
                        "vertical_strategy": "lines",
                        "horizontal_strategy": "lines"
                    }
                    tables = page.find_tables(table_settings)
                    table_bboxes = [table.bbox for table in tables]
                except Exception as e:
                    print(f"Warning: Could not find tables on page {page_index + 1}: {e}")

                # 2. Filter out words in tables
                filtered_words = []
                for word in words:
                    x0, y0, x1, y1 = word['x0'], word['top'], word['x1'], word['bottom']
                    in_table = False
                    for bbox in table_bboxes:
                        x_min, y_min, x_max, y_max = bbox
                        if x0 >= x_min and x1 <= x_max and y0 >= y_min and y1 <= y_max:
                            in_table = True
                            break
                    if not in_table:
                        filtered_words.append(word)

                # 3. Cluster words into lines
                lines = defaultdict(list)
                for word in filtered_words:
                    y = round(word['top'] / self.y_tolerance) * self.y_tolerance
                    lines[y].append((word['x0'], word['text']))

                for y in sorted(lines):
                    line_text = ' '.join(word for _, word in sorted(lines[y], key=lambda x: x[0]))
                    clustered_lines.append(line_text)

        self.text_by_page = clustered_lines
        return self.text_by_page

    def extract_tables(self):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(self.file_bytes)
                tmp_path = tmp_file.name

            tables = camelot.read_pdf(tmp_path, pages='all')
            parsed_tables = []

            for table in tables:
                df = table.df
                if df.shape[0] < 2:
                    continue
                headers = df.iloc[0].tolist()
                table_data = []
                for _, row in df.iloc[1:].iterrows():
                    row_dict = {headers[i]: row[i] for i in range(len(headers))}
                    table_data.append(row_dict)
                parsed_tables.append(table_data)

            return parsed_tables
        except Exception as e:
            print(f"Table extraction failed: {e}")
            return []
        finally:
            if 'tmp_path' in locals() and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text("\n".join(raw_text))

        tables = self.extract_tables()
        result = {"text": cleaned_text}
        if tables:
            result["tables"] = tables

        return result
