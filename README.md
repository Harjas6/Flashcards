# UBC Pharmacy Drug List Flashcards

An unofficial flashcard web app for studying the UBC Pharmacy Year 2 (PY2) Foundations Drug List (2026W): generic and brand names, therapeutic class, and dosage forms plus the module and what category (table name) they belong to. Cards can be shuffled and filtered by module and category.

> The data was extracted from the PDF by a script and then checked by hand with no errors found, but it is possibe I missed something.

**Live demo:** https://harjas6.github.io/Flashcards/

<img width="640" alt="image" src="https://github.com/user-attachments/assets/84a9bfa0-c4a5-4322-af2b-e4288a354406" />


## How it works

**Data pipeline (`extractor/`)**: A Python script pulls the drug tables out of the course PDF with `pdfplumber`, then cleans them into `drugs.json` for the app. Module and category headings are detected by font size, and grouped by vertical position. Tables that don't parse cleanly are logged to `bad_tables.json` where I then manual added them instead of being silently dropped.

**Frontend (`frontend/`)**: React, TypeScript, and Vite.

## Design choices

- **No backend:** The dataset (206 drugs, ~68 KB) is small enough to bundle into the app, so there's no server or database to host and pages load instantly.
- **Cascading filters:** Categories only appear after you pick a module. A flat list would show up to 52 categories at once, let you pair a module with a category from a different module (giving empty results), and include several identically named "Miscellaneous" categories you couldn't tell apart.
- **Shuffle:** Cards are randomized with a Fisher-Yates shuffle, so every order is equally likely.

## Deployment

A GitHub Actions workflow builds the frontend and deploys it to [GitHub Pages](https://harjas6.github.io/Flashcards/) on every push to `main`.

## Run locally

```bash
cd frontend
npm install
npm run dev
```

Open the local link it prints (e.g. `http://localhost:5173/Flashcards/`).

To rebuild the data from the PDF (optional, since `drugs.json` is already included):

```bash
cd extractor
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python clean_data.py
```
