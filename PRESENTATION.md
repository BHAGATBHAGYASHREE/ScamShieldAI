# ScamShield AI — Product Pitch & Engineering Architecture Guide
*Presenter: Bhagyashree Bhagat | Roll No. 34 | B.Tech CSE*
*Course: Feature Engineering & MLOps | Individual Mini-Project*

> **Interactive Presentation Deck:** Open [`presentation.html`](./presentation.html) or [`SCAMSHIELD_AI_PRESENTATION.html`](./SCAMSHIELD_AI_PRESENTATION.html) in your browser. Navigate with keyboard arrow keys (`←` / `→`) or click buttons. Evidence screenshots feature click-to-zoom modal view.

---

## 1. Live Public Cloud Deployments

- **⚡ Streamlit Cloud Web Application:** [https://bhagatbhagyashree-scamshieldai-streamlit-app-rctooz.streamlit.app/](https://bhagatbhagyashree-scamshieldai-streamlit-app-rctooz.streamlit.app/)
- **🌐 Render Production API (FastAPI Microservice):** [https://scamshield-ai-r1o5.onrender.com/](https://scamshield-ai-r1o5.onrender.com/)
- **📦 Docker Hub Official Image:** `docker pull bhagyashreebhagat/scamshield-ai:latest`
- **📁 GitHub Source Code:** [https://github.com/BHAGATBHAGYASHREE/ScamShieldAI](https://github.com/BHAGATBHAGYASHREE/ScamShieldAI)

---

## 2. Complete 19-Slide Presentation Structure

```
Part 1: The Human Story & Problem Pitch (Non-Technical & Story-Driven)
├── Slide 1: Title & Identity (Bhagyashree Bhagat, Roll No. 34, DETECT • EXPLAIN • WARN)
├── Slide 2: The Real Incident (WhatsApp timeline & 3 high-res evidence cards with modal zoom)
├── Slide 3: Anatomy of the Deception: Why It Works (Urgency, Social Engineering, Proof Illusion)
├── Slide 4: The Larger Problem ($1.4B lost, 74.4% cybercrimes, real Indian smishing archetypes)
├── Slide 5: Meet ScamShield AI (Solution overview, 5-step flow, live prediction UI mockup)
└── Slide 6: Product Differentiation (“Not Just Scam / Not Scam”: Detect, Explain, Classify)

Part 2: Feature Engineering Curriculum Alignment (The 5 Phases)
├── Slide 7: Ingestion & Data Strategy (3-tier corpus, Stratified 80/20 split, Zero-leakage rule)
├── Slide 8: Phase 1 — Foundations & Lifecycle (Bias-variance, Pipeline recipe, Derived vs Raw)
├── Slide 9: Phase 2 — Cleaning, Scaling & Transformations (StandardScaler, sublinear_tf, missing values)
├── Slide 10: Phase 3 — Feature Creation & Domain Heuristics (18 cyber-threat signals, Shannon Entropy H(X))
└── Slide 11: Phase 4 & 5 — Selection & Dimensionality Defense (Filter min_df/max_df, L2 C=2.5, Sparse vs PCA)

Part 3: Production Engineering, MLOps & Live Demonstration
├── Slide 12: Code Architecture (`features.py`, BaseEstimator, TransformerMixin, FeatureUnion, Joblib fix)
├── Slide 13: MLflow Experiment Tracking Matrix (Runs 1, 2, 3 with accuracy, precision, recall, F1, ROC-AUC)
├── Slide 14: Architectural Defense: Why Over Obvious Alternatives? (BERT vs CPU, CountVectorizer vs Entropy, Calibration)
├── Slide 15: MLOps Infrastructure (DVC stages, params.yaml, 13 pytest tests, GitHub Actions CI/CD)
├── Slide 16: Live Cloud Deployments & Demonstration (Render API + Streamlit Cloud URLs, JSON schemas)
├── Slide 17: Held-Out Benchmark Results & Product Vision (2,272 unseen messages, latency benchmark, vision)
├── Slide 18: The Consumer Dilemma (Futurama Fry Meme: "Not sure if real or phishing... Don't guess, use ScamShield AI")
└── Slide 19: Thank You & Closing Thought ("The strongest lock on the door cannot protect against someone who convinces you to open it...")
```

---

## 3. Curriculum Mapping: 5 Phases of Feature Engineering

### Phase 1: Foundations
- **ML Lifecycle:** `data_loader.py` (Ingestion) $\rightarrow$ `features.py` (Transformation) $\rightarrow$ `train_mlflow.py` (Modeling & Tracking) $\rightarrow$ `app/main.py` (FastAPI Serving) $\rightarrow$ `streamlit_app.py` (Consumer Feedback).
- **Bias-Variance Tradeoff:** Too few features underfits subtle social engineering cues; unconstrained 100k+ n-grams overfit on noisy typos. Bounded via `max_features=8000` + L2 penalty ($C=2.5$).
- **Raw vs. Engineered:** Raw input message string is transformed into derived quantitative signals: `digit_ratio`, `uppercase_ratio`, `special_char_ratio`, and Shannon character entropy.
- **Pipeline Automation (One Recipe):** Encapsulated `sklearn.pipeline.Pipeline` executes `fit()` strictly on `X_train` before any scaling or vectorization occurs, preventing vocabulary and distribution leakage into `X_test`.

### Phase 2: Cleaning & Prep
- **Missing Values:** Defensively handled in `extract_features_single()` with type-safe sanitization (`str(text) if pd.notna(text) else ""`) and neutral zero defaults, preventing runtime crashes on empty or null messages.
- **Scaling Techniques:** `StandardScaler` standardizes the 18 continuous heuristic features into zero-mean, unit-variance ($z = \frac{x - \mu}{\sigma}$) inside `FeatureUnion`, ensuring large integers like message length don't dominate normalized ratios.
- **Transformations & Skew Correction:**
  - `sublinear_tf=True` applies a logarithmic scale $1 + \log(\text{tf})$ to term frequencies, preventing repeated spam words from skewing predictions.
  - Normalized ratios (`digit_ratio`, `uppercase_ratio`) correct for text length skewness.

### Phase 3: Feature Creation
- **Time & Urgency Signals:** Coercion keywords with temporal deadlines (`urgent`, `immediately`, `within 24 hours`, `expires`, `action required`) extracted via precompiled regex `RE_URGENCY`.
- **Domain Cyber-Threat Heuristics:** 18 handcrafted features:
  - Communication hooks: `has_url`, `has_short_url` (bit.ly, tinyurl), `has_phone`, `has_currency` (₹, Rs), `has_email`.
  - Structural entropy: $H(X) = -\sum P(x) \log_2 P(x)$ to distinguish human language from encrypted/shortened slugs.
- **Curse of Dimensionality Management:** Combining n-grams can create combinatorial explosion (millions of pairs). We cap features at 8,000 using `max_features=8000` and `ngram_range=(1,2)`.

### Phase 4: Feature Selection
- **Filter Methods:** Term frequency thresholds (`min_df=3` removes rare typos/noise; `max_df=0.90` filters universal stop-words) filter features before model training.
- **Embedded Methods (L2 Regularization):** Logistic regression with parameter $C=2.5$ applies ridge regularization, shrinking weights of redundant features while maintaining stability across correlated signals.
- **Tree Importance:** In Run 2 (Random Forest), tree-based Gini importance validated that urgency, Shannon entropy, and phone count are the top predictive structural features.

### Phase 5: Dimensionality Reduction & Sparsity Defense
- **Why Sparse Linear Representation Over Dense PCA:**
  - Dense PCA transforms sparse text matrices into dense principal components, which destroys token-level explainability (we could no longer highlight "bit.ly" or "₹3,000" to the user).
  - High-dimensional sparse TF-IDF spaces (8,000 features) are naturally linearly separable.
  - Linear inference runs in **0.08ms on standard CPU**, making PCA projection computationally unnecessary and counterproductive.

---

## 4. Key Engineering Metrics & Architectural Defenses

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
