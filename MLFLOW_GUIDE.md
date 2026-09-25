# ScamShield AI — MLflow Tracking & Model Governance Guide

## 1. Why MLflow for ScamShield AI?
Without formal experiment tracking, ML engineers rely on fragmented notebook cells and ad-hoc print statements.
In a consumer cybersecurity product, tracking is mandatory to verify:
- Did an updated feature improve **Precision** on critical fraud classes without increasing false alarms?
- What was the exact inference latency under test load?
- Which model run produced the serialized weights running inside the container?

---

## 2. Experiments Logged

| Run Name | Architecture | Key Features | Precision | Recall | ROC-AUC | Inference Latency |
|---|---|---|---|---|---|---|
| `baseline_tfidf_nb` | Multinomial Naive Bayes | TF-IDF Unigrams (5k max) | 83.92% | 90.08% | 0.9725 | 0.05 ms |
| `domain_heuristics_rf` | Random Forest (100 trees) | 18 Cyber-Threat Heuristics | 87.71% | 78.25% | 0.9553 | 0.12 ms |
| `champion_hybrid_pipeline` | Calibrated Classifier + Hybrid | Pruned (1,2) N-grams + 18 Heuristics | **91.96%** | **91.03%** | **0.9858** | **0.08 ms** |

---

## 3. How to Launch the MLflow UI

```bash
cd "ScamShield AI"
mlflow ui --port 5000
```

Open `http://localhost:5000` in your browser to:
1. Inspect parallel coordinates and parameter-vs-metric scatter plots.
2. Compare confusion matrices and ROC curves across all 3 runs.
3. Download the model artifact and view the logged `model_metadata.json`.
