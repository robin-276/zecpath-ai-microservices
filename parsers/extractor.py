import os
import re
import json
import pdfplumber
import docx
import logging

# Assuming your logger is set up in utils/logger.py
# from utils.logger import get_logger
# logger = get_logger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.extension = os.path.splitext(file_path)[1].lower()

    def extract_raw_text(self) -> str:
        """Routes to the correct parser based on file extension."""
        if self.extension == '.pdf':
            return self._extract_from_pdf()
        elif self.extension in ['.docx', '.doc']:
            return self._extract_from_docx()
        else:
            logger.error(f"Unsupported file format: {self.extension}")
            raise ValueError(f"Unsupported file format: {self.extension}")

    def _extract_from_pdf(self) -> str:
        """Extracts text from PDF while attempting to maintain layout/columns."""
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    # extract_text(layout=True) helps with columns and tables
                    page_text = page.extract_text(layout=True)
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.error(f"Error reading PDF {self.file_path}: {e}")
            raise
        return text

    def _extract_from_docx(self) -> str:
        """Extracts text from DOCX files."""
        try:
            doc = docx.Document(self.file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        except Exception as e:
            logger.error(f"Error reading DOCX {self.file_path}: {e}")
            raise

    def clean_and_normalize(self, text: str) -> str:
        """Cleans noise, normalizes bullets, and standardizes spacing."""
        if not text:
            return ""

        # 1. Normalize bullet points (convert unicode bullets to standard '-')
        text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219]', '-', text)
        
        # 2. Clean unwanted noise/symbols (keep alphanumeric, punctuation, and newlines)
        text = re.sub(r'[^\w\s\.\,\-\:\;\@\+\(\)\/]', ' ', text)
        
        # 3. Normalize whitespace (reduce multiple spaces to one)
        text = re.sub(r' {2,}', ' ', text)
        
        # 4. Normalize newlines (reduce 3+ newlines to max 2 for paragraph separation)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # 5. Normalize capitalization for common section headings
        headings = ['experience', 'education', 'skills', 'projects', 'summary']
        for heading in headings:
            # Matches heading if it's on its own line (case insensitive)
            text = re.sub(rf'(?im)^({heading})\s*[:]?\s*$', heading.upper() + ':', text)

        return text.strip()

    def process_and_store(self, output_dir: str = "data/cleaned_resumes"):
        """Executes the pipeline and stores the structured result."""
        logger.info(f"Processing resume: {self.file_path}")
        
        raw_text = self.extract_raw_text()
        cleaned_text = self.clean_and_normalize(raw_text)
        
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.basename(self.file_path).split('.')[0]
        output_path = os.path.join(output_dir, f"{base_name}_extracted.json")
        
        structured_data = {
            "source_file": self.file_path,
            "cleaned_text": cleaned_text
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(structured_data, f, indent=4)
            
        logger.info(f"Extraction saved to: {output_path}")
        return structured_data