from io import BytesIO
from typing import List

import pandas as pd


def create_excel(main_df: pd.DataFrame,
                 review_df: pd.DataFrame,
                 all_tables: List[pd.DataFrame]) -> BytesIO:
    """
    Create in-memory Excel with multiple sheets.
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        if not main_df.empty:
            main_df.to_excel(writer, sheet_name="Extracted_Data", index=False)

        if not review_df.empty:
            review_df.to_excel(writer, sheet_name="Review_Required", index=False)

        for i, df in enumerate(all_tables, start=1):
            sheet_name = f"Table_{i}"[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    output.seek(0)
    return output