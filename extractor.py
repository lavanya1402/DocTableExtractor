from typing import List

import pandas as pd
import pytesseract
from img2table.document import Image as Img2TableImage
from img2table.ocr import TesseractOCR

from config import OCR_LANG, OCR_PSM, MIN_CONFIDENCE, TESSERACT_PATH

# Important: tell pytesseract exact executable
if TESSERACT_PATH:
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_tables_from_image(image_path: str) -> List[pd.DataFrame]:
    """
    Extract tables from a cleaned image using img2table + Tesseract.
    Compatible with img2table==1.2.11
    """
    ocr = TesseractOCR(
        n_threads=1,
        lang=OCR_LANG,
        psm=OCR_PSM
    )

    doc = Img2TableImage(src=image_path)

    tables = doc.extract_tables(
        ocr=ocr,
        borderless_tables=False,
        min_confidence=MIN_CONFIDENCE
    )

    extracted_tables: List[pd.DataFrame] = []
    for table in tables:
        df = table.df
        if df is not None and not df.empty:
            extracted_tables.append(df)

    return extracted_tables