# ScamShield AI — Product Pitch Deck & Presentation Guide
*Format: 5–7 Minute Product Pitch | Target Audience: Investors, ML Engineers, Faculty & Classmates*

> **Interactive Presentation Deck:** You can open [`presentation.html`](./presentation.html) in any web browser to present these slides interactively using keyboard arrow keys!

---

## 1. Presentation Requirements & Guidelines

According to the course brief:
- **Tone:** Product pitch, not an academic lecture or homework submission. You are "selling" a security solution to an audience that doesn't know your problem yet.
- **Duration:** 5 to 7 minutes strictly.
- **Narrative Arc:**
  1. **The Hook & Problem (1.5 min):** Open with an authentic human story and why existing spam solutions fail.
  2. **The Solution & Value Proposition (1 min):** Present ScamShield AI.
  3. **Mandatory Live Demo (2 min):** Click through the running Streamlit UI connected to the live FastAPI backend.
  4. **The Technical Build & Defense (1.5 min):** Answer *"Why Did You Use It and Why Is It Better Than The Obvious Alternative?"* across architecture, feature engineering, and serving.
  5. **MLOps Delivery & Wrap-up (1 min):** Showcase DVC data versioning, MLflow experiments, and automated Docker Hub CI/CD.

---

## 2. Detailed Slide-by-Slide Pitch Script

### Slide 1: The Hook — A Rs. 15,000 Order I Never Placed
- **Visual on Slide:**
  - Redacted screenshot of your actual incoming smishing SMS:
    > *"Your order #AMZ-99381 of Rs. 14,999 has been placed. If you did not make this transaction, call our fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now"*
  - Two key psychological highlights: **Manufactured Panic** and **Obfuscated Trap Door**.
- **Speaker Script (0:00 – 0:45):**
  > *"Last month, my phone buzzed with an SMS. It claimed an Amazon order of fifteen thousand rupees had just been placed on my card. I hadn’t bought anything.*
  >
  > *In that split second, rational thinking stops and adrenaline takes over: 'Has my account been compromised?' You instinctively reach to dial the 'fraud desk' or tap the cancellation link. In that exact moment of manufactured panic, billions of dollars are drained from innocent consumers every year.*
  >
  > *This isn't annoying marketing spam. This is psychological warfare. And the worst part? Traditional spam filters let it right through."*

---

### Slide 2: Why Existing Filters Fail
- **Visual on Slide:**
  - Split comparison card:
    - **Traditional Spam Filters:** Keyword bag-of-words looking for marketing phrases ("50% off pizza", "buy watches").
    - **Modern Smishing Attacks:** Mimics legitimate corporate syntax, uses shortened redirection URLs (`bit.ly`), fake alphanumeric sender IDs, and phone callback lures.
- **Speaker Script (0:45 – 1:30):**
  > *"Why did my phone's default filter miss this message? Because traditional filters treat text as a simple bag of words looking for repetitive marketing junk.*
  >
  > *Modern scammers don't send marketing junk. They craft precise corporate impersonations—fake delivery notices, bank KYC blocks, electricity power cutoffs. They don't include obvious spam words; they use psychological triggers: urgent deadlines, monetary figures, and private callback numbers.*
  >
  > *We don't need another binary spam filter that guesses 'Spam or Not Spam.' We need an explainable, real-time Cyber Risk Analyzer. That is ScamShield AI."*

---

### Slide 3: The Solution — Meet ScamShield AI
- **Visual on Slide:**
  - Product screenshot / badge showcasing the 4 core deliverables:
    1. **0–100 Calibrated Risk Score:** Platt-scaled probability gauge.
    2. **Threat Taxonomy:** Categorizes attacks (Fake Orders, KYC Phishing, Utility Scams, Delivery Traps).
    3. **Explainable Trigger Signals:** Token-level breakdown of red flags.
    4. **Consumer Safety Directives:** Exact actionable guidance on what *not* to do.
- **Speaker Script (1:30 – 2:15):**
  > *"ScamShield AI intercepts suspicious communication before the victim clicks or calls.*
  >
  > *The user pastes any message into ScamShield. In less than 0.1 milliseconds, ScamShield returns four critical outputs:*
  > 1. *A calibrated risk percentage from 0 to 100.*
  > 2. *The exact scam category.*
  > 3. *An explainable breakdown of every malicious trigger token detected.*
  > 4. *Immediate safety directives: 'Do not dial this number. Inspect your real order history inside the official app.'*
  >
  > *Let's see it live."*

---

### Slide 4: LIVE WORKING PROTOTYPE DEMO (Mandatory)
- **Action:** Switch screen to the running Streamlit UI (`http://localhost:8501` or public URL).
- **Speaker Script (2:15 – 3:45):**
  > 1. *"Notice the status badge in our sidebar: 'API is up, model loaded'. Our UI does not load the machine learning model directly. It makes clean HTTP calls to our FastAPI microservice running on port 8000. This ensures a single source of truth—the API is the engine, the UI is just one client.*
  >
  > 2. *Now, let's test the actual message I received. I click 'Load Author's Real Fake Order SMS' and click 'Scan Threat Risk'.*
  >
  > 3. *Within 3 milliseconds, our champion pipeline flags this as **93.2% CRITICAL RISK** under the category 'Phishing Link / Malicious URL'.*
  >
  > 4. *Look at the trigger breakdown below: It didn't just guess—it extracted the shortened redirect 'bit.ly', the private callback phone number, and the financial monetary lure '49,999 INR'.*
  >
  > 5. *Finally, it tells the consumer exactly what to do: 'DO NOT dial numbers provided. Verify your genuine account directly.'*
  >
  > 6. *Now, to prove we don't just flag everything as a scam, let's load a legitimate transactional notification: a Swiggy food delivery alert. We click scan: **SAFE (0.8% risk)**. Zero false alarms."*

---

### Slide 5: The Engineering Defense — "Why This Over That?"
- **Visual on Slide:**
  - Clean comparison table:

| Decision Area | What We Built | Obvious Alternative | Why Ours Is Better |
|---|---|---|---|
| **Model Family** | Hybrid TF-IDF (1,2 n-grams) + 18 Cyber Threat Heuristics | Deep Learning / Heavy LLM (BERT/DeBERTa) | **0.08ms CPU latency** vs 300ms GPU latency. Runs on standard CPU containers with zero cloud GPU cost and full token explainability. |
| **Pipeline Modularity** | Standalone `features.py` module | Inline custom transformer in notebook | Prevents the fatal `__main__` joblib serialization bug when unpickled in Docker or FastAPI. |
| **Serving Pattern** | Dedicated FastAPI Microservice | Direct model loading in Streamlit | **Single Source of Truth:** Prevents version drift when multiple clients (web, iOS, Android, email gateways) consume predictions. |
| **Calibration** | Platt Scaling (`CalibratedClassifierCV`) | Raw uncalibrated decision margins | Translates raw model distance into authentic 0–100% probabilities that consumers can trust. |

- **Speaker Script (3:45 – 4:45):**
  > *"Now to the core engineering question: Why didn't we just fine-tune BERT or DeBERTa?*
  >
  > *In production consumer security, latency and infrastructure cost dictate feasibility. A heavy transformer takes 300 milliseconds and demands an expensive GPU instance that costs hundreds of dollars a month.*
  >
  > *Our hybrid architecture extracts 18 domain heuristics—Shannon character entropy, URL shorteners, currency syntax, callback telephone patterns—fused with pruned sublinear n-grams. The result? 95.1% accuracy, 98.6% ROC-AUC, and a blistering **0.08 millisecond inference latency** on a single CPU core.*
  >
  > *Furthermore, by decoupling `features.py` from our notebook, we eliminated the classic joblib `__main__` unpickling bug that breaks so many student models in production."*

---

### Slide 6: Model Progression & Experiment Tracking (MLflow)
- **Visual on Slide:**
  - MLflow comparison chart of our 3 tracked experiments:
    1. **Baseline Model:** Vanilla Logistic Regression (91.2% accuracy, missed shortened links).
    2. **Engineered Model:** Heuristic LightGBM (93.8% accuracy, 1.4ms latency).
    3. **Champion Model:** Hybrid Calibrated SGD Classifier (**95.11% accuracy, 91.96% precision, 0.9858 ROC-AUC, 0.08ms latency**).
- **Speaker Script (4:45 – 5:30):**
  > *"We didn't just pick a model blindly. In MLflow, we tracked and compared three distinct architectures against 7,253 held-out test messages.*
  >
  > *The baseline linear model struggled with evasion tactics. The tree-based LightGBM improved accuracy but increased inference latency. Our registered Champion model—the Hybrid Calibrated SGD—delivered our highest precision (91.96%), ensuring that legitimate banking notifications are almost never falsely blocked, while keeping latency under 0.1ms."*

---

### Slide 7: Enterprise MLOps Delivery & CI/CD
- **Visual on Slide:**
  - Architecture diagram from raw data to cloud deployment:
    - **DVC:** Versioned 36,261 messages across 4 raw datasets into a reproducible 2-stage DAG (`prepare_data` &rarr; `train_and_evaluate`).
    - **GitHub Actions:** CI pipeline runs 13 unit tests on every push, builds a multi-stage Docker container, and publishes to Docker Hub.
    - **Docker Hub:** Public production image [`bhagyashreebhagat/scamshield-ai:latest`](https://hub.docker.com/r/bhagyashreebhagat/scamshield-ai) with 6 automated version tags.
    - **Cloud Deployment:** Ready-to-run Render Blueprint (`render.yaml`) and AWS EC2 user-data script.
- **Speaker Script (5:30 – 6:15):**
  > *"Finally, this is not just a model—it is a production system. Our data pipeline is locked and versioned with DVC so anyone can reproduce our training run with a single command.*
  >
  > *Every commit to our GitHub repository triggers GitHub Actions to run 13 automated unit tests, build a multi-process Docker container, and push the verified image directly to Docker Hub. Anyone in the world can run our system with one command:*
  > `docker run -p 8000:8000 -p 8501:8501 bhagyashreebhagat/scamshield-ai:latest`
  >
  > *From an unexpected SMS to a hardened, cloud-ready cyber defense system—that is ScamShield AI. Thank you!"*

---

## 3. Anticipated Questions from Professor & How to Answer

### Q1: "Why not use a pre-trained Large Language Model (LLM) or OpenAI API?"
- **Answer:**
  > *"Three reasons: Latency, Cost, and Privacy. Calling an external LLM API introduces 800ms–2000ms network latency and costs $0.002 per message. At 1 million messages a day, that's $2,000 daily. More importantly, mobile consumers cannot transmit private SMS containing personal order numbers to third-party cloud APIs. ScamShield AI runs locally or on edge servers in 0.08 milliseconds with zero per-query API costs."*

### Q2: "How did you prevent data leakage during feature engineering?"
- **Answer:**
  > *"All dataset splits were performed strictly BEFORE any vectorizer or heuristic scaler was fitted. In `src/data_loader.py`, we stratified train and test sets (80/20) on the raw text. The TF-IDF vocabulary and IDF weights were fitted exclusively on the 29,008 training messages. The 7,253 test messages were transformed using the already-fitted pipeline, ensuring zero vocabulary leakage."*

### Q3: "What happens if a scammer invents a new shortened domain?"
- **Answer:**
  > *"Our `ScamFeatureExtractor` doesn't just rely on a static blacklist. It computes Shannon character entropy and URL length heuristics. Scrambled redirect strings generate high structural entropy that triggers our anomaly heuristics regardless of the specific registrar used."*
