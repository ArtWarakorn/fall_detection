# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Camera-based fall detection system (CSC447 team project): YOLO + tracking detects people, rules decide whether someone has fallen, alerts go out via Telegram, and a FastAPI backend serves an API and a web UI. The README and comments in `requirements.txt` are written in Thai.

**As of the initial scaffold, every file under `app/` and `tests/` is empty** and `web/`, `docs/`, `data/` contain only `.gitkeep`. The architecture below is the *planned* design taken from `README.md` and `requirements.txt`. Check what actually exists before assuming any module, function or endpoint is there.

## Commands

```bash
python -m venv .venv && source .venv/bin/activate   # Python 3.10+
pip install -r requirements.txt
cp .env.example .env.local                          # fill in real values; never commit

uvicorn app.main:app --reload                       # run API + web server
pytest tests/                                       # all tests
pytest tests/test_fall_logic.py::test_name          # single test
python tests/evaluate.py                            # offline evaluation (precision/recall/F1, confusion matrix)
```

No linter or formatter is configured.

## Planned architecture

Two halves connected through the database and the notifier:

- **Vision pipeline** (person 1): `camera.py` opens the webcam or reads a clip (OpenCV) → `detector.py` runs Ultralytics YOLO (pose/detect) with its built-in tracker (ByteTrack/BoT-SORT, needs `lap`) to get per-person track IDs and keypoints → `fall_logic.py` holds per-track state and rules (keypoint angles, velocity, etc.) that decide a fall → `pipeline.py` is the main loop that ties these together, saves snapshots to `data/snapshots/`, records events and triggers alerts.
- **Service layer** (person 2): `main.py` is the FastAPI app with all endpoints; `schemas.py` holds Pydantic v2 models for JSON; `database.py` uses stdlib `sqlite3` with the DB at `data/falls.db`; `notifier.py` sends messages and photos to the Telegram Bot API via `httpx`; `config.py` uses `pydantic-settings` to read `.env.local`.
- **Web** (person 3): four pages in `web/`, rendered with Jinja2 through FastAPI; snapshots and static files are served via `aiofiles`.
- **Data**: `data/clips/` holds test video clips for evaluation; `tests/evaluate.py` uses scikit-learn, pandas and matplotlib to produce metrics and plots for the report in `docs/`.

## Team conventions (from README)

- Each module has one owner (see the table in README.md). Work on a branch named `<name>/<task>` (e.g. `person1/detector`), edit only your own files to avoid conflicts, and open a PR into `main`.
- Never commit `.env.local`, `data/falls.db`, model weights (`*.pt`, `*.onnx`), or snapshot images (all of these are gitignored).
