# 🎬 Movie Sentiment Intelligence & MLOps Platform

An end-to-end production-grade MLOps system for 5-class movie review sentiment analysis using the IMDb dataset. Features an interactive **4-Screen Streamlit Web Application**, a high-performance **FastAPI inference backend**, **DVC data pipelines**, **MLflow experiment tracking & model registry**, and **Evidently AI drift detection**.

---

## 📐 Architecture & Wireframe Layout

The application strictly implements the 4-screen design wireframe:

- **Screen 1 — Context & Overview**: Explains the relationship between movie reviews, audience sentiment, and the 5-point rating scale (1 to 5 stars).
- **Screen 2 — Postings**: Review submission portal capturing `Movie Name`, `Released Year`, `Cast`, `Direction & Additional Info`, and `About Movie (in 3 to 4 lines)`. Runs real-time NLP classification and registers entries into SQLite.
- **Screen 3 — Search Movie & Justification**: Search movie titles to view aggregated **Star Ratings**, all **Classified Postings**, and an automated **4–5 sentence NLP justification** synthesizing audience consensus on story, directing, and performances.
- **Screen 4 — Sentiment Analysis**: Direct text input testing for arbitrary review snippets, displaying confidence gauges and 5-class probability distributions.
- **⚙️ MLOps Dashboard**: Embedded Evidently AI interactive drift report tracking feature shift and sentiment distribution drift.

---

## 🛠️ Tech Stack & MLOps Tools

- **Models**:
  - **Baseline**: Calibrated Linear Support Vector Machine (`LinearSVC` + `CalibratedClassifierCV` + TF-IDF)
  - **Deep Learning**: DistilBERT (`distilbert-base-uncased`) with FP16 PyTorch training
- **Data Versioning**: DVC (`dvc.yaml`)
- **Experiment Tracking & Registry**: MLflow (SQLite backend with parameters, loss curves, confusion matrices, and registered model versions)
- **Serving / API**: FastAPI with Pydantic request/response validation
- **Persistence**: SQLite via SQLAlchemy (`movies`, `reviews`, `drift_logs`)
- **Monitoring**: Evidently AI (data drift & target distribution drift)
- **Containerization**: Docker, Docker Compose
- **CI/CD**: GitHub Actions (`.github/workflows/ci.yml`)

---

## 🚀 Quickstart Guide

### 1. Environment & Dependencies
```powershell
python -m pip install -r requirements.txt
```

### 2. Data Ingestion & Model Training
```powershell
# 1. Run DVC data pipeline (Ingest & create stratified 5-class splits)
python -m src.data.ingestion

# 2. Train and log Calibrated SVM Baseline to MLflow
python -m src.models.svm_model

# 3. (Optional) Fine-tune DistilBERT on GPU/CPU
python -m src.models.distilbert_model
```

### 3. Run FastAPI Backend
```powershell
uvicorn src.api.main:app --reload --port 8000
```
Interactive API docs available at: `http://localhost:8000/docs`

### 4. Run Streamlit 4-Screen Application
```powershell
streamlit run src/ui/app.py
```
UI dashboard opens at: `http://localhost:8501`

### 5. Launch MLflow Tracking UI
```powershell
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```
Navigate to: `http://localhost:5000`

### 6. Run Test Suite
```powershell
pytest -v
```

---

## 🐳 Docker Deployment

To launch the full containerized stack (FastAPI API + Streamlit UI):
```bash
docker-compose -f docker/docker-compose.yml up --build
```
