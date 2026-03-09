from typing import Dict, Any, List

import pandas as pd

from cleaner import clean_dataframe, standardize_columns, split_review_rows
from exporter import create_excel
from extractor import extract_tables_from_image
from preprocess import (
    uploaded_file_to_images,
    preprocess_image_for_table,
    save_temp_image,
    remove_temp_file,
)


def run_pipeline(uploaded_file) -> Dict[str, Any]:
    """
    End-to-end pipeline:
    uploaded file -> images -> preprocess -> extract -> clean -> review -> excel
    """
    images = uploaded_file_to_images(uploaded_file)

    extracted_tables: List[pd.DataFrame] = []
    combined_tables: List[pd.DataFrame] = []
    review_tables: List[pd.DataFrame] = []
    processed_pages: List[dict] = []

    for page_no, raw_pil_img in enumerate(images, start=1):
        cleaned_pil_img = preprocess_image_for_table(raw_pil_img)
        temp_img_path = save_temp_image(cleaned_pil_img)

        try:
            tables = extract_tables_from_image(temp_img_path)
        finally:
            remove_temp_file(temp_img_path)

        page_info = {
            "page_no": page_no,
            "raw_image": raw_pil_img,
            "cleaned_image": cleaned_pil_img,
            "tables_found": 0,
            "display_tables": [],
        }

        if not tables:
            processed_pages.append(page_info)
            continue

        page_info["tables_found"] = len(tables)

        for table_no, df in enumerate(tables, start=1):
            cleaned_df = clean_dataframe(df)
            cleaned_df = standardize_columns(cleaned_df)

            if cleaned_df.empty:
                continue

            cleaned_df.insert(0, "page_no", page_no)
            cleaned_df.insert(1, "table_no", table_no)

            good_df, review_df = split_review_rows(cleaned_df)

            if not good_df.empty:
                combined_tables.append(good_df)

            if not review_df.empty:
                review_tables.append(review_df)

            extracted_tables.append(cleaned_df)
            page_info["display_tables"].append((table_no, cleaned_df))

        processed_pages.append(page_info)

    final_df = pd.concat(combined_tables, ignore_index=True) if combined_tables else pd.DataFrame()
    final_review_df = pd.concat(review_tables, ignore_index=True) if review_tables else pd.DataFrame()
    excel_bytes = create_excel(final_df, final_review_df, extracted_tables) if extracted_tables else None

    return {
        "images_count": len(images),
        "processed_pages": processed_pages,
        "extracted_tables": extracted_tables,
        "final_df": final_df,
        "final_review_df": final_review_df,
        "excel_bytes": excel_bytes,
    }