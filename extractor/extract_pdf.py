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

# Words to ignore when extracting module names from the PDF. Chosen by examining the PDF and identifying common words that are not part of module names.
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
    """
    Extracts the module name from the PDF page by comparing font size and ignoring certain words.
    """
    words = page.extract_words(extra_attrs=["size"])
    name = ""
    for word in words:
        text = word["text"].strip(".,;:!?").lower()
        word_size = round(word["size"], 2)
        if word_size == MODULE_TXT_SIZE and text not in IGNORE:
            name += word["text"] + " "

    return name.strip()


def extract_headers(page):
    """
    Extracts headers from the PDF page by comparing
    font size and grouping words by their height position
    """
    words = page.extract_words(extra_attrs=["size"])
    headers = defaultdict(list)
    for word in words:
        if round(word["size"], 2) == HEADER_TXT_SIZE:
            headers[round(word["top"], 1)].append(word)
    headers = [
        " ".join(word["text"] for word in line_words) for line_words in headers.values()
    ]
    return headers


def normalize_columns(columns):
    """
    Certain PDF column names are abbreviated or inconsistent.
    This function normalizes them to match the expected column names.
    """
    aliases = {
        "generic": "generic name",
        "brand": "brand name",
    }

    return [aliases.get(col, col) for col in columns]


def extract_tables(
    page: pdfplumber.page.Page, prev_table_category: str, module_name: str
):
    """
    Extracts tables from a PDF page, matches headers to tables, and logs tables
    with invalid column structures for later review.
    """
    headers = extract_headers(page)
    index = 0
    current_header = prev_table_category
    low_col = [word.strip().lower() for word in TABLE_COL]

    tables = page.extract_tables()
    bad_tables = []
    successful_dfs = []
    for table_index, table in enumerate(tables, start=1):
        # any parsing issues logged for later review
        if any(len(row) != len(TABLE_COL) for row in table):
            bad_tables.append(
                log_bad_table(page, module_name, current_header, table_index, table)
            )
            continue

        first_row = [cell.strip().lower() if cell else "" for cell in table[0]]

        first_row = normalize_columns(first_row)
        if first_row != low_col:
            df = pd.DataFrame(table, columns=TABLE_COL)
        else:
            current_header = headers[index]
            index += 1
            df = pd.DataFrame(table[1:], columns=TABLE_COL)
        df["Category"] = current_header
        df["Module Name"] = module_name
        successful_dfs.append(df)

    return successful_dfs, current_header, bad_tables


def log_bad_table(page, module_name, current_header, table_index, table):
    bad_table = {
        "page": page.page_number,
        "table_index": table_index,
        "expected_columns": len(TABLE_COL),
        "actual_row_lengths": [len(row) for row in table],
        "category": current_header,
        "module": module_name,
        "table": table,
    }

    return bad_table


def make_dataframe(pdf_path):
    """
    Processes each PDF page, tracks the current module and category, and combines
    successfully extracted tables while collecting tables with parsing errors.
    """
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
