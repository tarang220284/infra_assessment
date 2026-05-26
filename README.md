## Discovery Tool

Locally-runnable, offline facilitator app for the **Backup and Isolated Recovery Environment (IRE)** discovery questionnaire. Built for live consulting workshops — replaces the Word doc + Excel tracker workflow.

- 15 primary questions across 5 facilitator layers, with 71 probing sub-questions
- Multiple named discovery sessions (one per customer engagement)
- Per-question maturity rating (Initial → Optimized), evidence notes, owner, follow-up flag, status
- Dashboard: maturity heatmap, layer averages, open follow-ups
- Exports: Markdown, JSON, full DOCX (facilitator format), client-summary DOCX
- 100% local — no internet, no telemetry, no CDN. SQLite persistence under `data/`.

## Source artifacts

The canonical questionnaire is derived from two artifacts placed in `src/`:

- `Backup Discussion.docx` — facilitator-grade primary + sub-question text, 5 layers
- `DRAFT - GIC_Discovery_Questions_4.28.26.xlsx` (sheet **Backup**) — granular Subdomain/Topic taxonomy

`ingest.py` reads both and emits `data/seed.json`. The DOCX is the canonical voice for the 15 primary questions and their probing sub-questions; the Excel taxonomy is preserved alongside it. **Exact wording from the DOCX is preserved.**

## Run (macOS / Linux)

```bash
./run.sh
```

## Run (Windows)

```bat
run.bat
```

Either launcher will:

1. Create a local `.venv` and install `requirements.txt` (first run only).
2. Run `python ingest.py` to produce `data/seed.json` if missing.
3. Start the FastAPI app on `http://127.0.0.1:8765` and auto-open the browser.

To skip the browser auto-open: `./run.sh --no-browser`
To pick a different port: `PORT=9000 ./run.sh`

## Manual / minimal install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python ingest.py
python app.py
```

## Project tree

```
ire-tool/
├── app.py                       FastAPI backend (API + static serving + DOCX/MD/JSON export)
├── ingest.py                    Parses src/*.docx + .xlsx → data/seed.json
├── requirements.txt             Pinned Python deps
├── run.sh / run.bat             Single-command launchers
├── README.md
├── src/
│   ├── Backup Discussion.docx
│   └── DRAFT - GIC_Discovery_Questions_4.28.26.xlsx
├── static/
│   ├── index.html               SPA shell
│   ├── app.js                   Vanilla JS SPA (no bundler)
│   └── styles.css               Dark consultant theme
├── data/
│   ├── seed.json                Generated canonical model
│   └── sessions.db              SQLite (created on first run)
└── exports/                     Generated reports land here
```

## API summary

| Method | Path                                        | Purpose                                  |
| ------ | ------------------------------------------- | ---------------------------------------- |
| GET    | `/api/model`                                | Canonical 5-layer / 15-question model    |
| GET    | `/api/sessions`                             | List sessions with progress              |
| POST   | `/api/sessions`                             | Create session                           |
| GET    | `/api/sessions/{id}`                        | Session + answers                        |
| PATCH  | `/api/sessions/{id}`                        | Rename / update metadata                 |
| DELETE | `/api/sessions/{id}`                        | Delete session (cascades answers)        |
| PATCH  | `/api/sessions/{id}/answers/{qid}`          | Update any answer field                  |
| GET    | `/api/sessions/{id}/summary`                | Heatmap, layer averages, follow-up count |
| GET    | `/api/sessions/{id}/export/{md\|json\|docx\|summary-docx}` | Download exports                 |

## Data model (per question)

```
response         : free text  — captured client narrative
maturity         : initial | developing | defined | managed | optimized
evidence         : free text  — doc refs, quotes
owner            : free text
status           : unanswered | in_progress | complete
follow_up        : none | open | closed
follow_up_note   : free text
```

## Notes on source reconciliation

- The 15 primary questions and their sub-questions are loaded **verbatim** from `Backup Discussion.docx`.
- Q8 and Q9 in the DOCX merge multiple probes into a single paragraph; these are split by `SUBQ_SPLITS` in `ingest.py` so every probe renders as its own bullet. The wording is unchanged.
- The Excel `Backup` sheet contains a much broader granular taxonomy (~170 rows). It is **not** mapped 1:1 to the 15 primaries — Excel rows are exposed in `seed.json` as `granular_questions[]` and `taxonomy{}` for optional UI use, but the live questionnaire is driven strictly by the DOCX.
- Maturity definitions (Initial → Optimized, CMMI-style 5-tier) are not present in either source; they are defined in `ingest.py::MATURITY_SCALE`. Flagged here because they exceed what the source documents explicitly define.

## Offline guarantee

- No `<script src="https://…">`, no `<link href="https://…">`, no CDN. Inspect `static/index.html`.
- No outbound HTTP from `app.py` or `ingest.py`.
- All persistence is local SQLite + JSON.
