import os

# =========================
# PATH CONFIG
# =========================
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA_DIR = r"C:\Program Files\Tesseract-OCR\tessdata"
POPPLER_PATH = r"C:\Users\lavan\Desktop\poppler\poppler-25.12.0\Library\bin"

# =========================
# OCR / EXTRACTION CONFIG
# =========================
OCR_LANG = "eng"
OCR_PSM = 6
MIN_CONFIDENCE = 50
PDF_DPI = 300

# =========================
# EXPECTED TABLE STRUCTURE
# =========================
EXPECTED_COLUMNS = [
    "Unit and Room #",
    "Patient Name/Age/Gender",
    "Isolation",
    "Infection",
    "CrCl",
    "Attending",
    "Blank Column",
]

# =========================
# ENV SETUP
# =========================
os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR
os.environ["PATH"] += os.pathsep + os.path.dirname(TESSERACT_PATH)
os.environ["PATH"] += os.pathsep + POPPLER_PATH