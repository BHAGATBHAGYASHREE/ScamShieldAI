# ScamShield AI — Product Pitch & Engineering Architecture Guide
*Presenter: Bhagyashree Bhagat | Roll No. 34 | B.Tech CSE*
*Course: Feature Engineering & MLOps | Individual Mini-Project*

> **Interactive Presentation Deck:** Open [`presentation.html`](./presentation.html) or [`SCAMSHIELD_AI_PRESENTATION.html`](./SCAMSHIELD_AI_PRESENTATION.html) in your browser. Navigate seamlessly with your keyboard arrow keys (`←` / `→`) or click buttons. Evidence screenshots feature click-to-zoom modal view.

---

## 1. Presentation Structure Overview (15 Slides)

```
Part 1: The Human Story & Problem Pitch (Non-Technical & Story-Driven)
├── Slide 1: Title & Identity (Bhagyashree Bhagat, Roll No. 34, DETECT • EXPLAIN • WARN)
├── Slide 2: The Real Incident (WhatsApp timeline & 3 high-res evidence cards with modal zoom)
├── Slide 3: Anatomy of the Deception: Why It Works (Urgency, Social Engineering, Proof Illusion)
├── Slide 4: The Larger Problem ($1.4B lost, 74.4% cybercrimes, real Indian smishing archetypes)
├── Slide 5: Meet ScamShield AI (Solution overview, 5-step flow, live prediction UI mockup)
└── Slide 6: Product Differentiation (“Not Just Scam / Not Scam”: Detect, Explain, Classify)

Part 2: Feature Engineering, ML & MLOps Technical Deep-Dive
├── Slide 7: Data Strategy & Zero-Leakage Split (268K+ vocabulary, 10K intent, 2.2K unseen benchmark, 80/20 split)
├── Slide 8: Feature Engineering Taxonomy (18+ domain heuristic dimensions across 4 families)
├── Slide 9: Feature Engineering Architecture (`features.py`, Shannon Entropy H(X), Regex engine, FeatureUnion, Joblib fix)
├── Slide 10: MLflow Experiment Tracking & Comparison Matrix (Runs 1, 2, 3 with accuracy, precision, recall, F1, ROC-AUC)
├── Slide 11: Architectural Defense: Why Over Obvious Alternatives? (GPU vs CPU latency, CountVectorizer vs Entropy, Calibration)
├── Slide 12: MLOps Pipeline & Reproducibility (DVC stages, dvc repro, params.yaml tracking)
├── Slide 13: Automated CI/CD & Docker Container (GitHub Actions workflow, 13 pytest tests, Docker Hub image)
├── Slide 14: System Serving Architecture & Live Demo (FastAPI REST JSON schemas, Streamlit live UI walkthrough)
└── Slide 15: External Benchmark Results, Takeaways & Final Vision (2,272 unseen messages, latency benchmark, vision)
```

---

## 2. Key Engineering Metrics & Architectural Defenses (Rubric Core)

### Top MLflow Experiment Tracking Results
- **Test Accuracy:** `95.11%` (↑ +2.97% over baseline)
- **Precision (Scam):** `91.96%` (↑ +8.04% over baseline)
- **Recall (Scam):** `91.03%` (↑ +0.95% over baseline)
- **ROC-AUC Score:** `0.9858` (State of the art)

### Experiment Comparison Matrix
| Experiment | Accuracy | Precision | Recall | F1-Score | ROC-AUC | Engineering Limitation / Defense |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Run 1: Baseline TF-IDF + Naive Bayes** | 92.14% | 83.92% | 90.08% | 0.8689 | 0.9725 | High false positives; blind to character entropy & shortened URL redirects. |
| **Run 2: 18 Domain Threat Heuristics + RF** | 90.54% | 87.71% | 78.25% | 0.8271 | 0.9553 | Captures structural signals (phone, urgency), but misses linguistic context. |
| **Run 3: Champion Hybrid Pipeline (ScamShield)** | **95.11%** | **91.96%** | **91.03%** | **0.9149** | **0.9858** | **Selected for production.** Fusion of lexical n-grams & domain threat indicators. |

---

## 3. Four Core Architectural Defense Points

1. **Why Not Deep Learning / BERT (DeBERTa)?**
   - BERT requires an expensive GPU cluster in production, has 100M+ parameters, and introduces 200–500ms latency.
   - ScamShield runs on standard CPU containers with `< 1ms inference latency` (0.08ms), zero cloud GPU bills, and full token-level explainability.
2. **Why Not Standard CountVectorizer?**
   - Scammers deliberately obfuscate words (e.g. `bit.ly`, `Rs. 14,999`, ALL-CAPS urgency). CountVectorizer treats tokens in isolation and ignores character entropy, URL redirects, and regex syntax ratios.
3. **Why Probability Calibration (`CalibratedClassifierCV`)?**
   - Raw linear SVM or logistic margins output uncalibrated scores that distort real risk. `CalibratedClassifierCV` (Platt scaling with 3-fold CV) ensures a 90% risk score truly reflects a 9-in-10 probability of fraud.
4. **Why Standalone `features.py` Over Notebook Definitions?**
   - Custom transformers defined in a notebook serialize into `__main__`, causing `AttributeError: Can't get attribute 'ScamFeatureExtractor'` when unpickled in FastAPI or pytest. Defining it in an importable module ensures exact reproducibility.

---

## 4. End-to-End System Access Links
- **Presentation Deck:** `http://localhost:8088/presentation.html`
- **Streamlit Interactive UI:** `http://localhost:8501`
- **FastAPI OpenAPI Swagger:** `http://localhost:8000/docs`
- **GitHub Repository:** [BHAGATBHAGYASHREE/ScamShieldAI](https://github.com/BHAGATBHAGYASHREE/ScamShieldAI)
- **Docker Hub Container Image:** `bhagyashreebhagat/scamshield-ai:latest`
