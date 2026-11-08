import numpy as np
import pandas as pd

from cleaner import basic_clean_text, clean_dataframe, split_review_rows, standardize_columns
from config import EXPECTED_COLUMNS


def test_basic_clean_text_handles_many_input_types():
    assert basic_clean_text(None) == ""
    assert basic_clean_text(float("nan")) == ""
    assert basic_clean_text(["Room", None, "12"]) == "Room 12"
    assert basic_clean_text(np.array([["A", "B"]])) == "A B"
    assert basic_clean_text("  two\n\tlines  ") == "two lines"


def test_clean_dataframe_drops_blank_rows_and_columns():
    df = pd.DataFrame({"a": ["x ", None, ""], "b": ["", None, ""], "c": ["y", None, "z"]})
    out = clean_dataframe(df)
    assert list(out.columns) == ["a", "c"]
    assert out.values.tolist() == [["x", "y"], ["", "z"]]


def test_standardize_columns_uses_expected_names_only_when_count_matches():
    matching = pd.DataFrame([range(len(EXPECTED_COLUMNS))])
    assert list(standardize_columns(matching).columns) == EXPECTED_COLUMNS
    other = pd.DataFrame([[1, 2]])
    assert list(standardize_columns(other).columns) == ["Column_1", "Column_2"]


def test_suspicious_rows_go_to_review():
    df = pd.DataFrame({"a": ["Room 12 Smith", "??", "@#$ bad"], "b": ["Isolation", "?", "%%"]})
    good, review = split_review_rows(df)
    assert good["a"].tolist() == ["Room 12 Smith"]
    assert len(review) == 2
