import pdfplumber
import camelot
import re
from collections import defaultdict
from src.preprocessing.cleaning import preprocess_text

class DigitalPDFPipeline:
    def __init__(self, filepath, y_tolerance=3):
        self.filepath = filepath
        self.y_tolerance = y_tolerance
        self.text_by_page = []
        self.cleaned_text = ""
        self.tables = []

    def extract_text(self):
        clustered_lines = []

        with pdfplumber.open(self.filepath) as pdf:
            for page in pdf.pages:
                words = page.extract_words()
                lines = defaultdict(list)

                for word in words:
                    y = round(word['top'] / self.y_tolerance) * self.y_tolerance
                    lines[y].append((word['x0'], word['text']))

                for y in sorted(lines):
                    line_text = ' '.join(word for _, word in sorted(lines[y], key=lambda x: x[0]))
                    clustered_lines.append(line_text)

        self.text_by_page = clustered_lines
        return self.text_by_page

    def extract_tables(self):
        try:
            tables = camelot.read_pdf(self.filepath, pages='all')
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

            self.tables = parsed_tables
            return parsed_tables
        except Exception as e:
            print(f"Table extraction failed: {e}")
            self.tables = []
            return []

    def run_pipeline(self):
        raw_text = self.extract_text()
        cleaned_text = preprocess_text(raw_text)

        tables = self.extract_tables()
        resultant_data = {"text": cleaned_text}

        if tables:
            resultant_data["tables"] = tables

        return resultant_data
