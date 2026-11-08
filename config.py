import os

# =========================
# PATH CONFIG
# =========================
# Tesseract and Poppler are found on the system PATH by default.
# On Windows, if they are not on PATH, set these in your environment or .env:
#   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
#   TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
#   POPPLER_PATH=C:\path\to\poppler\Library\bin
TESSERACT_PATH = os.getenv("TESSERACT_CMD") or None
TESSDATA_DIR = os.getenv("TESSDATA_PREFIX") or None
POPPLER_PATH = os.getenv("POPPLER_PATH") or None

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
if TESSDATA_DIR:
    os.environ["TESSDATA_PREFIX"] = TESSDATA_DIR
if TESSERACT_PATH:
    os.environ["PATH"] += os.pathsep + os.path.dirname(TESSERACT_PATH)
if POPPLER_PATH:
    os.environ["PATH"] += os.pathsep + POPPLER_PATH