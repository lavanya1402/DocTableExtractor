import re
import pandas as pd
import numpy as np

from config import EXPECTED_COLUMNS


def basic_clean_text(value) -> str:
    """
    Safely clean OCR output coming from strings, lists, numpy arrays, or NaN.
    """
    # Case 1: None
    if value is None:
        return ""

    # Case 2: list / tuple / set
    if isinstance(value, (list, tuple, set)):
        value = " ".join([str(v) for v in value if v is not None])

    # Case 3: numpy array
    elif isinstance(value, np.ndarray):
        value = " ".join([str(v) for v in value.flatten().tolist() if v is not None])

    # Case 4: handle NaN safely only for scalar values
    else:
        try:
            if pd.isna(value):
                return ""
        except Exception:
            pass

    # Convert to string
    value = str(value).strip()

    # Remove extra whitespace/newlines/tabs
    value = re.sub(r"\s+", " ", value)

    return value


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean dataframe safely cell by cell.
    """
    df = df.copy()
    df = df.fillna("")

    # Apply cleaning cell-wise
    df = df.applymap(basic_clean_text)

    # Drop fully blank rows
    df = df.loc[~(df == "").all(axis=1)]

    # Drop fully blank columns
    df = df.loc[:, ~(df == "").all(axis=0)]

    df.reset_index(drop=True, inplace=True)
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns if extracted count matches expected medical layout.
    Otherwise assign generic names.
    """
    df = df.copy()
    num_cols = len(df.columns)

    if num_cols == len(EXPECTED_COLUMNS):
        df.columns = EXPECTED_COLUMNS
    else:
        df.columns = [f"Column_{i+1}" for i in range(num_cols)]

    return df


def row_needs_review(row: pd.Series) -> bool:
    """
    Flag suspicious OCR rows for manual review.
    """
    text_row = " ".join([str(x) for x in row.values]).strip()

    if len(text_row) < 5:
        return True

    if text_row.count("?") >= 2:
        return True

    bad_chars = sum(ch in "@#$%^*~" for ch in text_row)
    if bad_chars >= 3:
        return True

    return False


def split_review_rows(df: pd.DataFrame):
    """
    Split dataframe into good rows and review rows.
    """
    review_mask = df.apply(row_needs_review, axis=1)

    review_df = df[review_mask].copy()
    good_df = df[~review_mask].copy()

    good_df.reset_index(drop=True, inplace=True)
    review_df.reset_index(drop=True, inplace=True)

    return good_df, review_df