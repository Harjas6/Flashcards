from collections import defaultdict

import pandas as pd
import pdfplumber

TABLE_COL = [
    "Generic Name",
    "Brand Name",
    "Therapeutic Class",
    "Dosage Forms and Strengths",
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


def extract_headers(page):
    words = page.extract_words(extra_attrs=["size"])
    headers = defaultdict(list)
    for word in words:
        if round(word["size"], 2) == HEADER_TXT_SIZE:
            headers[round(word["top"], 1)].append(word)
    headers = [
        " ".join(word["text"] for word in line_words) for line_words in headers.values()
    ]
    return headers


def extract_tables(
    page: pdfplumber.page.Page, prev_table_category: str, module_name: str
):
    headers = extract_headers(page)
    index = 0
    current_header = prev_table_category
    low_col = [word.strip().lower() for word in TABLE_COL]

    tables = page.extract_tables()
    bad_tables = []
    successful_df = []
    for table_index, table in enumerate(tables, start=1):
        # any parsing issues logged for later review
        if any(len(row) != len(TABLE_COL) for row in table):
            bad_table = {
                "page": page.page_number,
                "table_index": table_index,
                "expected_columns": len(TABLE_COL),
                "actual_row_lengths": [len(row) for row in table],
                "category": current_header,
                "module": module_name,
                "table": table,
            }
            bad_tables.append(bad_table)
            continue

        first_row = [cell.strip().lower() if cell else "" for cell in table[0]]
        if first_row != low_col:
            df = pd.DataFrame(table, columns=TABLE_COL)
        else:
            current_header = headers[index]
            index += 1
            df = pd.DataFrame(table[1:], columns=TABLE_COL)
        df["Category"] = current_header
        df["Module Name"] = module_name
        successful_df.append(df)

    return successful_df, current_header, bad_tables


def make_dataframe(pdf_path):
    prev_table_category = ""
    module_name = ""
    tables = []
    bad_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            new_module = extract_module(page)
            if new_module:
                module_name = new_module

            extracted_tables, prev_table_category, errors = extract_tables(
                page, prev_table_category, module_name
            )

            tables.extend(extracted_tables)
            bad_tables.extend(errors)

        if tables:
            return pd.concat(tables, ignore_index=True), bad_tables

    return pd.DataFrame(columns=FINAL_COL), bad_tables


if __name__ == "__main__":
    pdf_path = "./FDL_PY2.pdf"
    df, bad_tables = make_dataframe(pdf_path)
    print(bad_tables)
