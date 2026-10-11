import pandas as pd
import pdfplumber

TABLE_COL = [
    "Generic Name",
    "Brand Name",
    "Therapeutic Class",
    "Dosage Form and Strengths",
]

METADATA_COL = ["Category", "Module Name"]

FINAL_COL = TABLE_COL + METADATA_COL


def extract_module(page):
    return None  # Placeholder for metadata extraction logic


def extract_tables(page, prev_table_category, module_name):
    return None, prev_table_category  # Placeholder for table extraction logic


def make_dataframe(pdf_path):
    prev_table_category = ""
    module_name = ""
    tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            new_module = extract_module(page)
            if new_module:
                module_name = new_module

            extracted_tables, prev_table_category = extract_tables(
                page, prev_table_category, module_name
            )

            tables.extend(extracted_tables)

        if tables:
            return pd.concat(tables, ignore_index=True)

    return pd.DataFrame(columns=FINAL_COL)


if __name__ == "__main__":
    pdf_path = "./DrugList.pdf"
    df = make_dataframe(pdf_path)
    print(df)
