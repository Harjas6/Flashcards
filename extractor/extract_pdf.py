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

# Text size constants obtained by examining the PDF's text properties
# using page.extract_words()
MODULE_TXT_SIZE = 15.96
HEADER_TXT_SIZE = 12.96
TXT_SIZE = 12.00

IGNORE = [
    "d/c",
    "updated",
    "2026",
    "not",
    "in",
    "drug",
    "24",
    "authorized",
    "list",
    "marketed",
    "discontinued",
    "canada",
    "foundations",
    "dormant",
    "pharmacy",
    "2026w",
    "sale",
    "py2",
    "but",
    "for",
    "means",
    "currently",
    "still",
    "of",
    "august",
]


def extract_module(page: pdfplumber.page.Page) -> str:
    words = page.extract_words(extra_attrs=["size"])
    name = ""
    for word in words:
        text = word["text"].strip(".,;:!?").lower()
        word_size = round(word["size"], 2)
        if word_size == MODULE_TXT_SIZE and text not in IGNORE:
            name += word["text"] + " "

    return name.strip()


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
