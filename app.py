import traceback

import streamlit as st

from config import TESSERACT_PATH, POPPLER_PATH
from pipeline import run_pipeline

st.set_page_config(page_title="DocTableExtractor", layout="wide")

st.title("DocTableExtractor")
st.write("Upload PDF/Image → Preprocess → Extract tables → Clean data → Download Excel")

uploaded_file = st.file_uploader(
    "Upload PDF / PNG / JPG / JPEG",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    try:
        st.caption(f"Tesseract path: {TESSERACT_PATH or 'system PATH'}")
        st.caption(f"Poppler path: {POPPLER_PATH or 'system PATH'}")

        with st.spinner("Running full extraction pipeline..."):
            result = run_pipeline(uploaded_file)

        st.success(f"{result['images_count']} page(s) loaded successfully.")

        for page in result["processed_pages"]:
            page_no = page["page_no"]
            st.subheader(f"Page {page_no}")
            st.image(page["raw_image"], caption=f"Original - Page {page_no}", width=700)
            st.image(page["cleaned_image"], caption=f"Preprocessed - Page {page_no}", width=700)

            if page["tables_found"] == 0:
                st.warning(f"No table detected on page {page_no}.")
                continue

            st.success(f"{page['tables_found']} table(s) detected on page {page_no}.")

            for table_no, df in page["display_tables"]:
                st.markdown(f"### Table {table_no} - Page {page_no}")
                st.dataframe(df, use_container_width=True)

        if not result["final_df"].empty:
            st.subheader("Final Extracted Data")
            st.dataframe(result["final_df"], use_container_width=True)

        if not result["final_review_df"].empty:
            st.subheader("Rows Needing Review")
            st.dataframe(result["final_review_df"], use_container_width=True)

        if result["excel_bytes"] is not None:
            st.download_button(
                label="Download Excel",
                data=result["excel_bytes"],
                file_name="extracted_tables.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.error("No usable tables were extracted from the uploaded file.")

    except Exception as e:
        st.error(f"Error: {e}")
        st.code(traceback.format_exc())
        st.info("Check Poppler path, Tesseract path, img2table version, and uploaded file quality.")