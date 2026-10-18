import json
from pathlib import Path

import extract_pdf
import pandas as pd
from extract_pdf import FINAL_COL

# json file for frontend to use
output_path = (
    Path(__file__).resolve().parent.parent / "frontend" / "src" / "data" / "drugs.json"
)
# if directory doesn't exist make it
output_path.parent.mkdir(parents=True, exist_ok=True)

# csv for easy viewing in excel or sheets to verify data
drugs_file = Path("drugs.csv")
bad_tables_file = Path("bad_tables.json")


def load_data(path):

    # leaving this in case i ever want to manipulate the data without rerunning the whole extraction process
    if drugs_file.exists() and bad_tables_file.exists() and output_path.exists():
        df = pd.read_csv(drugs_file)

        with open(bad_tables_file, "r", encoding="utf-8") as f:
            bad_tables = json.load(f)

    else:
        df, bad_tables = extract_pdf.make_dataframe(path)
        df = fix_PY2_tables(df)

        df.to_csv(drugs_file, index=False)
        df.to_json(output_path, orient="records", indent=2)

        with open(bad_tables_file, "w", encoding="utf-8") as f:
            json.dump(bad_tables, f, indent=4, ensure_ascii=False)

    return df, bad_tables


def fix_PY2_tables(df):
    """
    Adds missing tables to the dataframe and fills missing rows
    """

    # Inspected JSON file to find which tables are missing

    # First Bad Table is actaully already in the csv. file mustve double read it
    # PDF seems to have a weird lines on it and color change on cell whihc may have caused it

    # Second Table IS NOT in csv. Some drugs are but they are a part of other categories
    # so still need to be included under this one

    # 3rd table is missing from the csv. Manually building it
    # Has right information but it is not formatted correctly
    # Examine the json and compare with the PDF to see how it should be formatted

    data = [
        # Second Table Contents
        [
            "sacubitril/valsartan",
            "Entresto",
            "Neprilysin Inhibitor/ARB",
            "Tabs: 24 mg/26 mg, 49 mg/51 mg,\n97 mg/103 mg",
            "Miscellaneous heart failure medications",
            "CARDIOVASCULAR MODULE",
        ],
        [
            "ivabradine",
            "Lancora",
            "If current (funny channel) Inhibitor",
            "Tabs: 5 mg, 7.5 mg",
            "Miscellaneous heart failure medications",
            "CARDIOVASCULAR MODULE",
        ],
        [
            "dapagliflozin",
            "Forxiga",
            "Sodium-glucose cotransporter 2 (SGLT2) Inhibitor",
            "Tabs: 10 mg",
            "Miscellaneous heart failure medications",
            "CARDIOVASCULAR MODULE",
        ],
        [
            "empagliflozin",
            "Jardiance",
            "SGLT2 Inhibitor",
            "Tabs: 10 mg, 25 mg",
            "Miscellaneous heart failure medications",
            "CARDIOVASCULAR MODULE",
        ],
        [
            "digoxin",
            "Lanoxin (d/c)\nToloxin (d/c)",
            "Cardiac Glycoside",
            "Tabs: 0.0625 mg, 0.125 mg\nOral Solution: 0.05 mg/mL",
            "Miscellaneous heart failure medications",
            "CARDIOVASCULAR MODULE",
        ],
        # Third Table Contents
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
    manual_table = pd.DataFrame(data=data, columns=FINAL_COL)
    df = pd.concat([df, manual_table], ignore_index=True)
    df = clean_data(df)

    return df


def clean_data(df):
    # There are missing values in the "Therapeutic Class" column due to PDF
    # having merged mega cells. Filling with forward fill to fixes this
    df[FINAL_COL[2]] = df[FINAL_COL[2]].ffill()
    return df


if __name__ == "__main__":
    df, bad_tables = load_data("FDL_PY2.pdf")
