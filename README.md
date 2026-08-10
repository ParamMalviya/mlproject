# Student Performance Predictor

An end-to-end regression pipeline that predicts a student's **math score** from their reading/writing scores and background features. It trains seven regressors, keeps the best by R², and serves live predictions through a FastAPI backend with a Streamlit UI.

## What it does

Given a student's profile — gender, race/ethnicity, parental education, lunch type, test-prep status, reading score, writing score — the model predicts their likely math score. It's a supervised regression problem on the "Students Performance in Exams" dataset.

## Architecture

```
TRAINING (offline, run once)
────────────────────────────
notebook/data/StudentsPerformance.csv
            │
            ▼
    data_ingestion        clean column names, train/test split
            │
            ├──> artifacts/train.csv, test.csv   (gitignored)
            ▼
    data_transformation   impute + one-hot + scale
            │
            ├──> artifacts/preprocessor.pkl
            ▼
    model_trainer         GridSearchCV over 7 regressors, keep best by R²
            │
            └──> artifacts/model.pkl

SERVING (online)
────────────────
  Streamlit UI  ──HTTP POST──>  FastAPI /predict
  (streamlit_app.py)            (app.py)
                                    │
                                    ▼
                        load model.pkl + preprocessor.pkl
                                    │
                                    ▼
                            predicted math_score
```

## Tech stack

- **ML:** scikit-learn, XGBoost, CatBoost — 7 regressors selected via `GridSearchCV`
- **Serving:** FastAPI (REST) + Streamlit (UI), two servers over HTTP
- **Packaging:** src-layout package, editable install via `pyproject.toml`
- **Tooling:** rotating-file logging, project-wide custom exception with `from e` chaining

## Project structure

```
student-performance/
├── artifacts/
│   ├── model.pkl              # trained best regressor (committed)
│   └── preprocessor.pkl       # fitted ColumnTransformer (committed)
├── notebook/
│   ├── data/StudentsPerformance.csv
│   ├── 1.EDA STUDENT PERFORMANCE.ipynb
│   └── 2.Model Training.ipynb
├── src/studentPerformance/
│   ├── components/            # data_ingestion, data_transformation, model_trainer
│   ├── pipelines/             # train_pipeline, predict_pipeline
│   ├── exception/             # shared custom exception
│   ├── logger/                # shared rotating-file logger
│   ├── constants.py           # column names in one place
│   └── utils.py               # save/load objects, model evaluation
├── app.py                     # FastAPI backend (/predict)
├── streamlit_app.py           # Streamlit UI
├── pyproject.toml
└── requirements.txt
```

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Usage

### 1. Train (produces model.pkl + preprocessor.pkl)

```powershell
python -m studentPerformance.pipelines.train_pipeline
```

### 2. Serve (two terminals)

Terminal 1 — FastAPI backend:

```powershell
uvicorn app:app --port 8000
```

Terminal 2 — Streamlit UI:

```powershell
streamlit run streamlit_app.py
```

Open the Streamlit URL, enter a student's details, and get a predicted math score.

## Regenerating derived data

`artifacts/raw.csv`, `train.csv`, and `test.csv` are gitignored — they're deterministic outputs of the ingestion step (`random_state=42`). Rebuild them (along with the model and preprocessor) any time by running the training pipeline:

```powershell
python -m studentPerformance.pipelines.train_pipeline
```

## Results

The pipeline selects the best of seven regressors by test R². On the current run the best model reached **R² ≈ 0.88** on the held-out test set. Training hard-fails if no model clears R² = 0.60, as a quality guard.

## Design decisions

- **src-layout package** (`src/studentPerformance/`) installed editable — consistent with my other portfolio projects, and avoids the tutorial-artifact package literally named `src`.
- **Config as dataclasses**, kept deliberately lean rather than a full YAML config-manager — appropriate for a pipeline this size.
- **Committed** the trained model, preprocessor, and source CSV so the repo runs out of the box; **gitignored** the regenerable split CSVs to avoid churn.
- **Shared logger + exception modules** standardized across my three portfolio projects for consistent, debuggable output.