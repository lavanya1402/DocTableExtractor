import os
import tempfile
from typing import List

import cv2
import numpy as np
from PIL import Image
from pdf2image import convert_from_bytes

from config import PDF_DPI, POPPLER_PATH


def uploaded_file_to_images(uploaded_file) -> List[Image.Image]:
    """
    Convert uploaded PDF/image into a list of PIL images.
    """
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        pdf_bytes = uploaded_file.read()
        return convert_from_bytes(
            pdf_bytes,
            dpi=PDF_DPI,
            poppler_path=POPPLER_PATH
        )

    img = Image.open(uploaded_file).convert("RGB")
    return [img]


def preprocess_image_for_table(pil_img: Image.Image) -> Image.Image:
    """
    Make noisy scanned images more OCR/table-friendly.
    """
    img = np.array(pil_img.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Denoise while preserving edges
    gray = cv2.fastNlMeansDenoising(gray, None, 20, 7, 21)

    # Improve contrast
    gray = cv2.equalizeHist(gray)

    # Adaptive threshold for uneven scans
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11
    )

    # Light cleanup of pepper noise
    kernel = np.ones((2, 2), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    return Image.fromarray(cleaned)


def save_temp_image(pil_img: Image.Image) -> str:
    """
    Save PIL image as temporary PNG and return path.
    """
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    pil_img.save(tmp.name, format="PNG")
    return tmp.name


def remove_temp_file(path: str) -> None:
    try:
        os.remove(path)
    except Exception:
        pass