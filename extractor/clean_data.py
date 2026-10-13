import json
from pathlib import Path

import extract_pdf
import pandas as pd
from extract_pdf import FINAL_COL

drugs_file = Path("drugs.csv")
bad_tables_file = Path("bad_tables.json")


def load_data(path):

    if drugs_file.exists() and bad_tables_file.exists():
        df = pd.read_csv(drugs_file)

        with open(bad_tables_file, "r", encoding="utf-8") as f:
            bad_tables = json.load(f)

    else:
        df, bad_tables = extract_pdf.make_dataframe(path)

        df.to_csv(drugs_file, index=False)

        with open(bad_tables_file, "w", encoding="utf-8") as f:
            json.dump(bad_tables, f, indent=4, ensure_ascii=False)

    return df, bad_tables


def fix_PY2_tables():
    # Inspected JSON file to find which tables are missing
    # manually building those three tables and returning them as a list of DataFrames

    # First Bad Table is actaully already in the csv. file mustve double read it
    # PDF seems to have a weird lines on it and color change on cell whihc may have caused it

    # Second Table also already in csv. Mustve double read it weirdly?

    # 3rd table is missing from the csv. Manually building it
    # Has right information but it is not formatted correctly
    # Examine the json and compare with the PDF to see how it should be formatted
    data = [
        [
            "memantine",
            "Ebixa",
            "NMDA Receptor\nAntagonist",
            "Tabs: 5 mg, 10 mg",
            "N-methyl-D-aspartate (NMDA) Receptor Antagonists",
            "NEUROLOGY MODULE",
        ],
        [
            "amantadine",
            "Symmetrel (d/c)",
            "Antiparkinsonian Agent\n/ Antiviral",
            "Caps: 100 mg\nSyrup: 10 mg/mL",
            "N-methyl-D-aspartate (NMDA) Receptor Antagonists",
            "NEUROLOGY MODULE",
        ],
    ]
    df = pd.DataFrame(data=data, columns=FINAL_COL)

    return df


if __name__ == "__main__":
    df, bad_tables = load_data("FDL_PY2.pdf")
    manual_table = fix_PY2_tables()
    df = pd.concat([df, manual_table], ignore_index=True)
    df.to_csv(drugs_file, index=False)
