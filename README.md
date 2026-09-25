# ScamShield AI — Scam Communication Risk Analyzer

[![ScamShield AI CI/CD](https://github.com/BHAGATBHAGYASHREE/ScamShieldAI/actions/workflows/docker_build_push.yml/badge.svg)](https://github.com/BHAGATBHAGYASHREE/ScamShieldAI/actions/workflows/docker_build_push.yml)
[![Docker Image](https://img.shields.io/badge/docker-bhagyashreebhagat%2Fscamshield--ai-blue?logo=docker)](https://hub.docker.com/r/bhagyashreebhagat/scamshield-ai)
[![Python 3.11](https://img.shields.io/badge/python-3.11-brightgreen.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit Cloud App](https://img.shields.io/badge/Streamlit%20Cloud-Live%20App-FF4B4B?logo=streamlit)](https://bhagatbhagyashree-scamshieldai-streamlit-app-rctooz.streamlit.app/)
[![Render Cloud API](https://img.shields.io/badge/Render-Live%20API-46E3B7?logo=render)](https://scamshield-ai-r1o5.onrender.com/)

**Live Deployments:**
- ⚡ **Streamlit Web UI:** [https://bhagatbhagyashree-scamshieldai-streamlit-app-rctooz.streamlit.app/](https://bhagatbhagyashree-scamshieldai-streamlit-app-rctooz.streamlit.app/)
- 🌐 **Render Production API:** [https://scamshield-ai-r1o5.onrender.com/](https://scamshield-ai-r1o5.onrender.com/)
- 📊 **Interactive Deck:** [http://localhost:8088/presentation.html](http://localhost:8088/presentation.html)

A production-grade machine learning system designed to protect mobile and digital communication consumers from smishing, fake delivery notices, banking fraud, and coercive social engineering attacks.

---

## 1. The Real-World Storyline
Mobile users routinely receive deceptive messages engineered to induce panic:
> *"Your order #AMZ-99381 of Rs. 14,999 has been placed. If you did not make this transaction, call our fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now"*

The victim panics, assumes their card was charged, and dials the fake call center or clicks the shortened link.
**ScamShield AI** intercepts this flow:
1. User pastes message into ScamShield.
2. AI extracts structural entropy, shortened redirect links, currency syntax, and callback numbers.
3. System outputs: **99.9% Fraud Risk Score (CRITICAL)**.
4. Identifies Category: **Fake Order & Call-Back Phishing**.
5. Displays exact trigger signals and safety directives: *"DO NOT call this number or click the link. Verify your order history directly in the official Amazon app."*

---

## 2. "Why Did You Use It & Why Is It Better Than The Alternative?" (Defense Matrix)

| Component / Choice | What We Used | Obvious Alternative | Why Ours Is Better for This Problem |
|---|---|---|---|
| **Core Architecture** | Hybrid Pruned TF-IDF (1,2 ngrams) + 18 Handcrafted Threat Heuristics | Deep Learning / Heavy LLM (DeBERTa / RoBERTa) | **Latency & Explainability:** Consumer SMS triage requires < 5ms CPU latency. BERT requires dedicated GPUs, 100M+ parameters, and costs hundreds of dollars in cloud compute while acting as an opaque black box. Our hybrid model achieves **0.08 ms latency** with >98% ROC-AUC and exact token-level explainability. |
| **Feature Extraction** | Domain Heuristics in `features.py` (Shortened links, Shannon entropy, phone regex, currency regex, urgency scores) | Raw Word Counts (`CountVectorizer`) | **Evasion Resistance:** Modern scammers obfuscate words (`bit.ly`, `Rs. 14,999`, `URGENT!`). Word counts treat tokens as independent bags, missing link redirection, callback lures, and panic punctuation. |
| **Text Vectorization** | Sublinear TF-IDF with N-grams (1,2) and vocabulary pruning (`min_df=3`, `max_df=0.90`) | Dense Embeddings (Word2Vec / BERT) | **Sparsity & Speed:** Sublinear TF dampens spam repetition tactics, while bigrams capture deceptive phrases ("order placed", "call immediately", "kyc pending") with zero GPU overhead. |
| **Model Calibration** | `CalibratedClassifierCV` (Sigmoid / Platt scaling) | Raw SVM / Logistic margins | **Consumer Actionability:** Raw decision distances cannot be presented to consumers as a risk percentage. Calibrated probabilities ensure an 85% risk score corresponds to an authentic 85% likelihood of deceit. |
| **Pipeline Modularity** | Custom transformer in standalone `features.py` | Defining custom transformer inline inside the Jupyter Notebook | **Joblib Serialization Safety:** `joblib.dump()` only saves the module path of custom classes. Defining them in a notebook serializes `<module '__main__'>`, causing `AttributeError` when unpickled inside FastAPI or Docker. `features.py` ensures 100% cross-environment portability. |
| **Serving Architecture** | FastAPI REST Microservice (`app/main.py`) | Loading `scamshield_pipeline.joblib` directly inside Streamlit | **Single Source of Truth:** Direct UI loading creates two places that predict (API and UI). The moment one updates without the other, they silently disagree. FastAPI provides one unified API for Streamlit, mobile apps, or enterprise gateways. |
| **Data Versioning** | DVC (`dvc.yaml` + `params.yaml`) | Ad-hoc CSV copying or Git LFS | **Pipeline Reproducibility:** DVC hashes data states and links code commits to dataset revisions, enabling deterministic pipeline rebuilds via `dvc repro`. |
| **Experiment Tracking** | MLflow (`mlflow.log_params`, `mlflow.log_metrics`) | Manual Excel sheets or terminal stdout | **Governance:** Records parallel runs, hyperparameter sweeps, latency metrics, and versioned artifacts in a searchable dashboard. |
| **Deployment & CI/CD** | Multi-process Docker (`entrypoint.sh`) + GitHub Actions | Running locally / Manual `docker push` | **Zero-Drift Delivery:** Packages FastAPI and Streamlit into a production container with automated testing and Docker Hub deployment on every git push. |

---

## 3. Project Structure

```
ScamShield AI/
├── data/
│   ├── raw/                        # 4 raw datasets (DeBERTa, 10k OTP, Financial, India)
│   └── processed/                  # Leakage-safe train/test splits (train.csv, test.csv)
├── features.py                     # Standalone Sklearn transformer (prevents __main__ bug)
├── notebooks/
│   └── scamshield_pipeline.ipynb   # Executed end-to-end notebook with outputs
├── src/
│   ├── data_loader.py              # Ingestion, validation, and stratified splitting
│   └── train_mlflow.py             # MLflow experiment comparison and champion registration
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI microservice (Single source of truth)
│   └── schemas.py                  # Pydantic request/response schemas
├── models/
│   ├── scamshield_pipeline.joblib  # Serialized champion pipeline
│   └── model_metadata.json         # Version, accuracy, precision, and latency metrics
├── tests/
│   ├── test_pipeline.py            # Unit tests for transformer & model
│   └── test_api.py                 # Integration tests for FastAPI endpoints
├── streamlit_app.py                # Consumer cybersecurity web interface
├── Dockerfile                      # Production container image
├── entrypoint.sh                   # Supervisor script running FastAPI + Streamlit
├── .github/workflows/
│   └── docker_build_push.yml       # CI/CD pipeline
├── dvc.yaml                        # DVC reproducibility pipeline
├── params.yaml                     # Pipeline parameters
├── requirements.txt
├── DVC_GUIDE.md
├── MLFLOW_GUIDE.md
└── PRESENTATION.md                 # 5–7 min pitch deck outline
```

---

## 4. Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Full Test Suite
```bash
pytest tests/ -v
```

### 3. Launch the FastAPI Backend
```bash
uvicorn app.main:app --reload --port 8000
```
*Interactive Swagger Documentation:* `http://localhost:8000/docs`

### 4. Launch the Streamlit Consumer App (in a second terminal)
```bash
streamlit run streamlit_app.py --server.port 8501
```
*Open in Browser:* `http://localhost:8501`

### 5. Launch the MLflow Experiment Dashboard
```bash
mlflow ui --port 5000
```
