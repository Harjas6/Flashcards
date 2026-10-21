import json
import re
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

OUTPUT_DIR = Path(__file__).resolve().parent

raw_drugs_file = OUTPUT_DIR / "raw_drugs.csv"
cleaned_drugs_file = OUTPUT_DIR / "cleaned_drugs.csv"
bad_tables_file = OUTPUT_DIR / "bad_tables.json"


def load_data(path):

    # leaving this in case i ever want to manipulate the data without rerunning the whole extraction process
    if raw_drugs_file.exists() and bad_tables_file.exists():
        df = pd.read_csv(raw_drugs_file)

        with open(bad_tables_file, "r", encoding="utf-8") as f:
            bad_tables = json.load(f)

    else:
        df, bad_tables = extract_pdf.make_dataframe(path)
        df = fix_PY2_tables(df)  # completed raw data, not cleaned

        df.to_csv(raw_drugs_file, index=False)

        with open(bad_tables_file, "w", encoding="utf-8") as f:
            json.dump(bad_tables, f, indent=4, ensure_ascii=False)

    return df, bad_tables


def fix_PY2_tables(df):
    """
    Adds missing tables to the dataframe and fills missing rows. only run after buiding from scratch.
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
    return df


def standardize_therapeutic_class(df):
    """
    Standardize names to acronyms for easier searching and filtering
    """
    df.loc[
        df["Therapeutic Class"] == "Short-Acting Muscarinic\nAntagonist (SAMA)",
        "Therapeutic Class",
    ] = "SAMA"
    df.loc[
        df["Therapeutic Class"] == "Long-Acting Muscarinic\nAntagonist (LAMA)",
        "Therapeutic Class",
    ] = "LAMA"
    df.loc[
        df["Therapeutic Class"] == "Short-Acting Beta\nAgonist (SABA)",
        "Therapeutic Class",
    ] = "SABA"
    df.loc[
        df["Therapeutic Class"] == "Long-Acting Beta Agonist\n(LABA)",
        "Therapeutic Class",
    ] = "LABA"

    df.loc[
        df["Therapeutic Class"] == "Inhaled Corticosteroid\n(ICS)",
        "Therapeutic Class",
    ] = "ICS"

    df.loc[
        df["Therapeutic Class"] == "Non-dihydropyridine (DHP) CCB",
        "Therapeutic Class",
    ] = "Non-DHP CCB"

    df.loc[
        df["Therapeutic Class"] == "Sodium-glucose cotransporter 2 (SGLT2) Inhibitor",
        "Therapeutic Class",
    ] = "SGLT2 Inhibitor"


def add_key(df):
    """
    Add a unique key to each row for frontend to use as a unique identifier
    """

    def slug(s):
        return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")

    df.insert(
        0,
        "id",
        df["Module Name"].map(slug) + "__" + df["Generic Name"].map(slug),
    )
    assert df["id"].is_unique, df[df["id"].duplicated(keep=False)]


def clean_data(df):
    """
    Clean the data by standardizing the therapeutic class and adding a unique key.
    Can rerun whenever.
    """
    # There are missing values in the "Therapeutic Class" column due to PDF
    # having merged mega cells. Filling with forward fill to fixes this
    df[FINAL_COL[2]] = df[FINAL_COL[2]].ffill()

    standardize_therapeutic_class(df)

    add_key(df)

    return df


if __name__ == "__main__":
    pdf_path = Path(__file__).resolve().parent / "FDL_PY2.pdf"
    df, bad_tables = load_data(pdf_path)
    clean_df = clean_data(df)
    clean_df.to_csv(cleaned_drugs_file, index=False)
    clean_df.to_json(output_path, orient="records", indent=2)
