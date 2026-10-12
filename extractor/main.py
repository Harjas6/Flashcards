import json
from pathlib import Path

import extract_pdf
import pandas as pd


def load_data():
    drugs_file = Path("drugs.csv")
    bad_tables_file = Path("bad_tables.json")

    if drugs_file.exists() and bad_tables_file.exists():
        df = pd.read_csv(drugs_file)

        with open(bad_tables_file, "r", encoding="utf-8") as f:
            bad_tables = json.load(f)

    else:
        df, bad_tables = extract_pdf.make_dataframe("FDL_PY2.pdf")

        df.to_csv(drugs_file, index=False)

        with open(bad_tables_file, "w", encoding="utf-8") as f:
            json.dump(bad_tables, f, indent=4, ensure_ascii=False)

    return df, bad_tables


if __name__ == "__main__":
    df, bad_tables = load_data()
