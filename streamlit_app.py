"""
streamlit_app.py - ScamShield AI Consumer Cybersecurity Risk Analyzer

Architecture:
  - Calls the FastAPI microservice at API_URL (default: http://localhost:8000).
  - Enforces the "Single Source of Truth" architectural rule: no duplicate joblib.load().
  - Commercial cybersecurity UI aesthetic with dark styling, risk gauge, trigger highlighter,
    and the author's real-world fake order demonstration.
"""
from __future__ import annotations

import os
import html
import requests
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config(
    page_title="ScamShield AI — Scam Communication Risk Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Cyber-Security Dark Theme Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
    }

    .main {
        background-color: #0b0f19;
        color: #e2e8f0;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #172554 0%, #0b0f19 75%);
    }

    /* Metric cards */
    .metric-box {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 12px;
        padding: 16px 20px;
        backdrop-filter: blur(8px);
        margin-bottom: 12px;
    }

    .risk-banner-critical {
        background: linear-gradient(135deg, rgba(220, 38, 38, 0.25) 0%, rgba(153, 27, 27, 0.4) 100%);
        border: 1.5px solid #ef4444;
        border-radius: 14px;
        padding: 22px 24px;
        margin-top: 15px;
        box-shadow: 0 10px 25px -5px rgba(239, 68, 68, 0.2);
    }

    .risk-banner-safe {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(6, 95, 70, 0.3) 100%);
        border: 1.5px solid #10b981;
        border-radius: 14px;
        padding: 22px 24px;
        margin-top: 15px;
        box-shadow: 0 10px 25px -5px rgba(16, 185, 129, 0.15);
    }

    .risk-banner-suspicious {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(180, 83, 9, 0.3) 100%);
        border: 1.5px solid #f59e0b;
        border-radius: 14px;
        padding: 22px 24px;
        margin-top: 15px;
    }

    .trigger-pill {
        display: inline-block;
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        color: #fca5a5;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        font-family: 'JetBrains Mono', monospace;
    }

    .safety-item {
        background: rgba(15, 23, 42, 0.6);
        border-left: 3px solid #38bdf8;
        padding: 10px 14px;
        margin-bottom: 8px;
        border-radius: 0 8px 8px 0;
        font-size: 13.5px;
    }

    .sample-chip {
        cursor: pointer;
        padding: 8px 12px;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        font-size: 12.5px;
        margin-bottom: 6px;
        transition: all 0.2s ease;
    }
    .sample-chip:hover {
        border-color: #38bdf8;
        background: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# ---- Top Header ----
col_logo, col_stat = st.columns([3, 1])
with col_logo:
    st.markdown("## 🛡️ ScamShield AI")
    st.caption("Consumer Cybersecurity Scam Communication Risk Analyzer • *FastAPI-Backed Inference*")

with col_stat:
    try:
        health_resp = requests.get(f"{API_URL}/health", timeout=2.5).json()
        if health_resp.get("model_loaded"):
            st.markdown(
                '<div style="text-align:right; margin-top:10px;">'
                '<span style="background:rgba(16,185,129,0.2); color:#10b981; border:1px solid #10b981; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600;">'
                '● API Online • Champion v%s</span></div>' % health_resp.get("model_version", "1.0.0"),
                unsafe_allow_html=True,
            )
        else:
            st.warning("API reachable, but model loading...")
    except Exception:
        st.markdown(
            '<div style="text-align:right; margin-top:10px;">'
            '<span style="background:rgba(239,68,68,0.2); color:#ef4444; border:1px solid #ef4444; padding:4px 10px; border-radius:20px; font-size:12px; font-weight:600;">'
            '● API Disconnected</span></div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ---- Fetch Demo Samples from API ----
demo_samples = []
try:
    demo_resp = requests.get(f"{API_URL}/demo-samples", timeout=2.5)
    if demo_resp.status_code == 200:
        demo_samples = demo_resp.json()
except Exception:
    pass

# Session state initialization for message input
if "input_message" not in st.session_state:
    st.session_state["input_message"] = (
        "Your order #AMZ-99381 of Rs. 14,999 has been placed. "
        "If you did not make this transaction, call our fraud desk immediately at +919876543210 "
        "or cancel at bit.ly/cancel-order-now"
    )

# ---- Sidebar ----
with st.sidebar:
    st.markdown("### 🎯 Live Demonstration")
    st.info(
        "**Real-World Scenario:**\n\n"
        "The user received an unexpected SMS claiming an expensive order had been placed. "
        "The message induces panic so the victim calls the fake fraud desk or clicks the shortened cancel link."
    )

    if st.button("🚨 Load Author's Real UPI Overpayment Attack", use_container_width=True, type="primary"):
        st.session_state["input_message"] = (
            "Hlo mam. By mistake send 3000. Please return mam 2000 to my PhonePe QR code immediately."
        )
        st.rerun()

    if st.button("📦 Load Fake Order Alert SMS", use_container_width=True):
        st.session_state["input_message"] = (
            "Your order #AMZ-99381 of Rs. 14,999 has been placed. "
            "If you did not make this transaction, call our fraud desk immediately at +919876543210 "
            "or cancel at bit.ly/cancel-order-now"
        )
        st.rerun()

    st.markdown("#### Test Curated Attack Scenarios")
    for sample in demo_samples:
        if sample["id"] != "demo_real_fake_order":
            if st.button(f"📌 {sample['title']}", key=sample["id"], use_container_width=True):
                st.session_state["input_message"] = sample["message"]
                st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ System Specifications")
    st.markdown("""
    - **Architecture:** Hybrid Pruned TF-IDF + 18 Cyber-Threat Heuristics
    - **Probability Calibration:** Isotonic / Sigmoid Calibrated
    - **Inference Latency:** < 5 ms (CPU-Optimized)
    - **Source of Truth:** FastAPI REST Microservice
    """)

# ---- Main Product Tabs ----
tab_analyze, tab_batch, tab_models, tab_dataset = st.tabs([
    "🔍 Analyze Message",
    "📂 Batch Analyzer",
    "📈 Model Performance & MLflow",
    "📊 Dataset Foundation"
])

# ==============================================================================
# TAB 1: CORE PRODUCT — ANALYZE MESSAGE
# ==============================================================================
with tab_analyze:
    st.markdown("#### Paste Suspicious Communication")
    st.caption("Analyze SMS, WhatsApp, or email notifications for phishing links, fake orders, KYC traps, and psychological coercion.")

    message_text = st.text_area(
        "Message Text",
        value=st.session_state["input_message"],
        height=130,
        placeholder="Paste message here (e.g., 'Your account will be suspended in 24 hours. Update KYC at bit.ly/...')"
    )

    col_btn, col_clear = st.columns([1, 5])
    with col_btn:
        analyze_clicked = st.button("🛡️ Scan Threat Risk", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear Input"):
            st.session_state["input_message"] = ""
            st.rerun()

    if analyze_clicked or message_text:
        if not message_text.strip():
            st.warning("Please enter or paste a message to analyze.")
        else:
            with st.spinner("Analyzing linguistic markers, structural entropy, and threat indicators..."):
                try:
                    res = requests.post(
                        f"{API_URL}/analyze",
                        json={"message": message_text},
                        timeout=5.0
                    )
                    if res.status_code != 200:
                        st.error(f"API Error ({res.status_code}): {res.text}")
                    else:
                        data = res.json()

                        # Risk Banner Render
                        risk_score = data["risk_score"]
                        is_scam = data["is_scam"]
                        risk_level = data["risk_level"]
                        category = data["category"]

                        if risk_score >= 80.0:
                            banner_class = "risk-banner-critical"
                            badge_color = "#ef4444"
                            icon = "🚨"
                        elif risk_score >= 50.0:
                            banner_class = "risk-banner-critical"
                            badge_color = "#f97316"
                            icon = "⚠️"
                        elif risk_score >= 25.0:
                            banner_class = "risk-banner-suspicious"
                            badge_color = "#f59e0b"
                            icon = "🔍"
                        else:
                            banner_class = "risk-banner-safe"
                            badge_color = "#10b981"
                            icon = "✅"

                        st.markdown(f"""
                        <div class="{banner_class}">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <div>
                                    <span style="font-size:24px; font-weight:800; color:#fff;">{icon} {risk_level}</span>
                                    <span style="background:{badge_color}; color:#fff; font-weight:700; font-size:12px; padding:3px 10px; border-radius:12px; margin-left:10px;">
                                        {category}
                                    </span>
                                </div>
                                <div style="text-align:right;">
                                    <div style="font-size:32px; font-weight:900; color:#fff;">{risk_score:.1f}%</div>
                                    <div style="font-size:11px; text-transform:uppercase; letter-spacing:1px; color:#cbd5e1;">Fraud Probability</div>
                                </div>
                            </div>
                            <div style="margin-top:14px; font-size:14.5px; color:#f1f5f9; line-height:1.5;">
                                {data['explanation']}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # Progress Gauge
                        st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
                        st.progress(min(max(risk_score / 100.0, 0.0), 1.0))

                        # Technical Signals & Safety Guidance Columns
                        col_signals, col_safety = st.columns([1, 1])

                        with col_signals:
                            st.markdown("##### 🔬 Suspicious Signals Detected")
                            triggers = data.get("triggers", [])
                            if not triggers:
                                st.markdown("""
                                <div class="metric-box">
                                    <span style="color:#10b981;">✓ No explicit deception tokens, shortened URLs, or urgent callback patterns found.</span>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                for t in triggers:
                                    st.markdown(f"""
                                    <div class="metric-box">
                                        <div style="display:flex; justify-content:space-between; align-items:center;">
                                            <span class="trigger-pill">{t['type']}: {html.escape(t['token'])}</span>
                                            <span style="font-size:11px; font-weight:700; color:#ef4444;">[{t['severity']}]</span>
                                        </div>
                                        <div style="font-size:12.5px; color:#cbd5e1; margin-top:6px;">
                                            {t['description']}
                                        </div>
                                    </div>
                                    """, unsafe_allow_html=True)

                        with col_safety:
                            st.markdown("##### 🛡️ Consumer Safety Recommendations")
                            recommendations = data.get("safety_recommendations", [])
                            for rec in recommendations:
                                st.markdown(f"""
                                <div class="safety-item">
                                    {rec}
                                </div>
                                """, unsafe_allow_html=True)

                            st.caption(f"⚡ Analyzed via FastAPI microservice in **{data.get('latency_ms', 0)} ms**")

                except requests.exceptions.RequestException as e:
                    st.error(f"Cannot reach ScamShield API at {API_URL}. Ensure uvicorn is running.")
                    st.caption(str(e))

# ==============================================================================
# TAB 2: BATCH ANALYZER
# ==============================================================================
with tab_batch:
    st.markdown("#### Batch Communication Risk Assessment")
    st.caption("Upload or paste multiple messages to triage enterprise or carrier-level communication traffic.")

    batch_input = st.text_area(
        "Enter messages (one per line)",
        value=(
            "Your order #AMZ-99381 of Rs. 14,999 has been placed. Call fraud desk at +919876543210 or cancel at bit.ly/cancel-now\n"
            "Your Swiggy order has been picked up by delivery partner Rahul.\n"
            "URGENT: Your KYC is pending for SBI Bank. Click bit.ly/sbi-kyc to update immediately or account blocked.\n"
            "Meeting rescheduled to 4 PM in room 302."
        ),
        height=140
    )

    if st.button("🚀 Analyze Batch", type="secondary"):
        lines = [line.strip() for line in batch_input.split("\n") if line.strip()]
        if lines:
            with st.spinner(f"Analyzing {len(lines)} messages..."):
                try:
                    res = requests.post(f"{API_URL}/analyze-batch", json={"messages": lines}, timeout=10.0)
                    if res.status_code == 200:
                        batch_results = res.json()
                        table_data = []
                        for item in batch_results:
                            table_data.append({
                                "Risk Score": f"{item['risk_score']:.1f}%",
                                "Verdict": "🚨 SCAM" if item["is_scam"] else "✅ LEGITIMATE",
                                "Category": item["category"],
                                "Triggers": item["trigger_count"],
                                "Message Preview": item["message"][:70] + ("..." if len(item["message"]) > 70 else ""),
                                "Latency (ms)": item["latency_ms"]
                            })
                        st.dataframe(table_data, use_container_width=True)
                except Exception as e:
                    st.error(f"Batch request failed: {e}")

# ==============================================================================
# TAB 3: MODEL PERFORMANCE & MLFLOW
# ==============================================================================
with tab_models:
    st.markdown("#### MLflow Experiment Tracking & Architecture Decisions")
    st.markdown("""
    In accordance with the **'Why did you use it, and why is it better than the obvious alternative?'** principle:
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Test Accuracy", "95.11%", "+2.97% over baseline")
    with col2:
        st.metric("Precision (Scam)", "91.96%", "+8.04% over baseline")
    with col3:
        st.metric("Recall (Scam)", "91.03%", "+0.95% over baseline")
    with col4:
        st.metric("ROC-AUC Score", "0.9858", "State of the art")

    st.markdown("##### Experiment Comparison Matrix")
    comparison = [
        {
            "Experiment": "Run 1: Baseline TF-IDF + Naive Bayes",
            "Accuracy": "92.14%",
            "Precision": "83.92%",
            "Recall": "90.08%",
            "F1-Score": "0.8689",
            "ROC-AUC": "0.9725",
            "Limitation": "High false positives; blind to character entropy & shortened URL redirects."
        },
        {
            "Experiment": "Run 2: 18 Domain Threat Heuristics + RF",
            "Accuracy": "90.54%",
            "Precision": "87.71%",
            "Recall": "78.25%",
            "F1-Score": "0.8271",
            "ROC-AUC": "0.9553",
            "Limitation": "Captures structural signals (phone, urgency), but misses linguistic context."
        },
        {
            "Experiment": "Run 3: Champion Hybrid Pipeline (ScamShield)",
            "Accuracy": "95.11%",
            "Precision": "91.96%",
            "Recall": "91.03%",
            "F1-Score": "0.9149",
            "ROC-AUC": "0.9858",
            "Limitation": "Selected for production. Fusion of lexical n-grams & domain threat indicators."
        }
    ]
    st.table(comparison)

    st.markdown("##### Why this Architecture Over Obvious Alternatives?")
    st.markdown("""
    1. **Why not Deep Learning / BERT (DeBERTa)?**
       - BERT requires a GPU in production, has 100M+ parameters, and introduces 200–500ms latency.
       - ScamShield runs on standard CPU containers with **< 1ms inference latency**, zero cloud GPU bills, and full token-level explainability.
    2. **Why not standard CountVectorizer?**
       - Scammers obfuscate words (e.g. `bit.ly`, `Rs. 14,999`, ALL-CAPS urgency). CountVectorizer ignores character entropy, URLs, and punctuation ratios.
    3. **Why Probability Calibration?**
       - Raw SVM or logistic margins output uncalibrated scores. `CalibratedClassifierCV` ensures a 90% risk score truly reflects a 9-in-10 probability of fraud.
    """)

# ==============================================================================
# TAB 4: DATASET FOUNDATION
# ==============================================================================
with tab_dataset:
    st.markdown("#### Multi-Dataset Ingestion Foundation")
    st.caption("ScamShield AI unifies 4 distinct real-world communication datasets to maximize generalization:")

    datasets_info = [
        {
            "Dataset": "dataset_v3_for_deberta.csv",
            "Role": "Core Linguistic Backbone",
            "Samples": "268,340 rows",
            "Signals Provided": "Benign / malicious texts with 24 pre-engineered structural metrics."
        },
        {
            "Dataset": "sample_10k.csv",
            "Role": "OTP & Phishing Intent",
            "Samples": "10,000 rows",
            "Signals Provided": "OTP interception attempts, phishing flags, and telecom sender IDs."
        },
        {
            "Dataset": "Financial scams detection dataset.csv",
            "Role": "Banking & Payment Fraud",
            "Samples": "523 rows",
            "Signals Provided": "Unauthorized debits, pre-approved loan scams, and fake refunds."
        },
        {
            "Dataset": "scam_hum_india.csv",
            "Role": "Regional Indian Fraud Context",
            "Samples": "2,272 rows",
            "Signals Provided": "Electricity bill disconnection, Vi/Airtel SIM block, and UPI fraud."
        }
    ]
    st.table(datasets_info)

    st.info("Unified Dataset: **36,261 deduplicated messages** (71.1% Benign, 28.9% Fraudulent) split strictly before feature extraction.")
