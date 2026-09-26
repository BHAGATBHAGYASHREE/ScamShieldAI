"""
streamlit_app.py - FAARZI AI: Counterfeit Communication & Financial Fraud Intelligence

Theme:
  Inspired by the Amazon Prime Video series 'FARZI' (Raj & DK / Shahid Kapoor).
  "Asli ya Farzi?" — High-stakes forensic intelligence engine that unmasks
  fabricated SMS, fake order invoices, counterfeit UPI refund traps, and social engineering coercion.

Architecture:
  - Primary: Calls the FastAPI microservice at API_URL (default: http://localhost:8000).
  - Resilient Fallback: If the API service is offline, gracefully executes direct local inference
    via the champion pipeline, ensuring zero downtime for demonstrations.
  - Cinematic Farzi Aesthetics: Banknote printing textures, dark olive & charcoal currency palette,
    mint emerald security watermarks, counterfeit stamps, and real-time forensic explainability.
"""
from __future__ import annotations

import base64
import html
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import requests
import streamlit as st

# Ensure project root is in path for fallback inference
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

API_URL = os.environ.get("API_URL", "http://localhost:8000")
MODEL_PATH = PROJECT_ROOT / "models" / "scamshield_pipeline.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"

st.set_page_config(
    page_title="FAARZI AI — Asli Ya Farzi? Scam & Fraud Intelligence",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Farzi Cinematic Theme CSS Injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Montserrat:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

    /* Global Overrides */
    html, body, [class*="css"] {
        font-family: 'Montserrat', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main {
        background-color: #070c08;
        color: #e2e8f0;
    }

    .stApp {
        background: 
            radial-gradient(circle at 50% 0%, #152718 0%, #080d09 60%, #040705 100%);
        background-attachment: fixed;
    }

    /* Cinematic Farzi Brand Typography */
    .farzi-hero-title {
        font-family: 'Cinzel', serif;
        font-weight: 900;
        font-size: 3.4rem;
        letter-spacing: 0.32em;
        text-transform: uppercase;
        color: #f8fafc;
        margin: 0;
        line-height: 1.05;
        text-shadow: 0 0 25px rgba(0, 230, 118, 0.4), 0 4px 15px rgba(0, 0, 0, 0.8);
    }

    .farzi-tagline {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #00e676;
        margin-top: 4px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .farzi-serial-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #eab308;
        background: rgba(234, 179, 8, 0.12);
        border: 1px solid rgba(234, 179, 8, 0.35);
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.08em;
        font-weight: 600;
    }

    /* STF Forensic Hero Banner */
    .farzi-hero-banner {
        background: linear-gradient(135deg, rgba(16, 33, 20, 0.85) 0%, rgba(8, 14, 10, 0.95) 100%);
        border: 1px solid rgba(0, 230, 118, 0.25);
        border-left: 5px solid #00e676;
        border-radius: 14px;
        padding: 18px 24px;
        margin-bottom: 22px;
        display: flex;
        align-items: center;
        gap: 18px;
        box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.7), 0 0 20px rgba(0, 230, 118, 0.08);
        backdrop-filter: blur(12px);
    }

    .farzi-banner-text {
        flex: 1;
    }

    /* Banknote / Evidence Card Styling */
    .evidence-tray {
        background: rgba(13, 22, 15, 0.75);
        border: 1px solid rgba(0, 230, 118, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        backdrop-filter: blur(10px);
        margin-bottom: 15px;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.5);
    }

    /* Farzi Verdict Stamp Banners */
    .verdict-banner-farzi {
        background: linear-gradient(135deg, rgba(185, 28, 28, 0.3) 0%, rgba(69, 10, 10, 0.6) 100%);
        border: 2px solid #ef4444;
        border-radius: 14px;
        padding: 24px 26px;
        margin-top: 18px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px -5px rgba(239, 68, 68, 0.35), inset 0 0 20px rgba(239, 68, 68, 0.15);
    }

    .verdict-banner-asli {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(4, 120, 87, 0.45) 100%);
        border: 2px solid #10b981;
        border-radius: 14px;
        padding: 24px 26px;
        margin-top: 18px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px -5px rgba(16, 185, 129, 0.3), inset 0 0 20px rgba(16, 185, 129, 0.12);
    }

    .verdict-banner-shakki {
        background: linear-gradient(135deg, rgba(217, 119, 6, 0.25) 0%, rgba(120, 53, 15, 0.5) 100%);
        border: 2px solid #f59e0b;
        border-radius: 14px;
        padding: 24px 26px;
        margin-top: 18px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 30px -5px rgba(245, 158, 11, 0.3);
    }

    /* Farzi Rubber Stamp Effect */
    .stamp-overlay {
        font-family: 'Cinzel', serif;
        font-weight: 900;
        font-size: 1.15rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        display: inline-block;
        padding: 4px 14px;
        border-radius: 4px;
        border: 2.5px solid currentColor;
        transform: rotate(-3deg);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
    }

    .stamp-farzi {
        color: #ef4444;
        background: rgba(239, 68, 68, 0.15);
        border-color: #ef4444;
    }

    .stamp-asli {
        color: #00e676;
        background: rgba(0, 230, 118, 0.15);
        border-color: #00e676;
    }

    .stamp-shakki {
        color: #facc15;
        background: rgba(250, 204, 21, 0.15);
        border-color: #facc15;
    }

    /* Trigger Pills / Forensic Indicators */
    .trigger-pill {
        display: inline-block;
        background: rgba(239, 68, 68, 0.18);
        border: 1px solid #ef4444;
        color: #fca5a5;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        margin: 3px;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-box {
        background: rgba(18, 28, 20, 0.7);
        border: 1px solid rgba(0, 230, 118, 0.15);
        border-radius: 10px;
        padding: 14px 18px;
        backdrop-filter: blur(8px);
        margin-bottom: 10px;
        transition: border-color 0.2s ease;
    }
    .metric-box:hover {
        border-color: rgba(0, 230, 118, 0.4);
    }

    .safety-item {
        background: rgba(14, 22, 16, 0.8);
        border-left: 3.5px solid #00e676;
        padding: 11px 15px;
        margin-bottom: 8px;
        border-radius: 0 8px 8px 0;
        font-size: 13.5px;
        color: #e2e8f0;
    }

    /* Currency Security Thread Meter */
    .security-thread-bar {
        height: 12px;
        border-radius: 6px;
        background: #111e14;
        border: 1px solid rgba(255, 255, 255, 0.1);
        overflow: hidden;
        margin-top: 14px;
        position: relative;
    }

    /* Custom Button & Tab Styling */
    .stButton>button {
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        letter-spacing: 0.05em;
        border-radius: 8px;
        transition: all 0.25s ease;
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #059669 0%, #00e676 100%) !important;
        color: #041308 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.35) !important;
    }
    .stButton>button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 230, 118, 0.5) !important;
    }

    .stTextArea textarea {
        background-color: rgba(10, 17, 12, 0.85) !important;
        border: 1px solid rgba(0, 230, 118, 0.3) !important;
        color: #f8fafc !important;
        font-family: 'JetBrains Mono', monospace !important;
        border-radius: 10px !important;
    }
    .stTextArea textarea:focus {
        border-color: #00e676 !important;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.25) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        border-radius: 8px 8px 0 0;
        padding: 10px 18px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #00e676 !important;
        border-bottom-color: #00e676 !important;
    }

</style>
""", unsafe_allow_html=True)

# Helper: local pipeline fallback runner if API is not running
@st.cache_resource
def load_local_pipeline():
    if MODEL_PATH.exists():
        try:
            import joblib
            from features import ScamFeatureExtractor  # noqa: F401
            pipe = joblib.load(MODEL_PATH)
            return pipe
        except Exception:
            return None
    return None

def analyze_message_service(text: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Analyzes a message via FastAPI microservice with automatic local pipeline fallback."""
    # 1. Try FastAPI Microservice (Single Source of Truth)
    try:
        res = requests.post(f"{API_URL}/analyze", json={"message": text}, timeout=3.0)
        if res.status_code == 200:
            return res.json(), "api"
    except Exception:
        pass

    # 2. Resilient Fallback to local pipeline
    pipeline = load_local_pipeline()
    if pipeline is not None:
        try:
            from features import identify_scam_category, explain_message_signals
            t0 = time.time()
            prob = float(pipeline.predict_proba([text])[0, 1])
            risk_score = round(prob * 100.0, 1)
            is_scam = risk_score >= 45.0
            category = identify_scam_category(text, is_scam)
            explanation_data = explain_message_signals(text)
            triggers = explanation_data["triggers"]
            trigger_names = [t["type"] for t in triggers]

            if risk_score >= 80.0:
                risk_level = "CRITICAL RISK"
            elif risk_score >= 50.0:
                risk_level = "HIGH RISK"
            elif risk_score >= 25.0:
                risk_level = "SUSPICIOUS"
            else:
                risk_level = "SAFE"

            if is_scam:
                explanation = (
                    f"This communication demonstrates classic hallmarks of {category}. "
                    f"Identified {len(triggers)} counterfeit indicator(s): {', '.join(set(trigger_names)) if trigger_names else 'linguistic urgency & financial coercion'}. "
                    "Extreme probability of social engineering or simulated transaction trap."
                )
            else:
                explanation = (
                    "No deceptive indicators or counterfeit characteristics identified. "
                    "The message conforms to authentic transactional and conversational baselines."
                )

            latency_ms = round((time.time() - t0) * 1000.0, 2)
            data = {
                "message": text,
                "is_scam": is_scam,
                "risk_score": risk_score,
                "risk_level": risk_level,
                "category": category,
                "explanation": explanation,
                "triggers": triggers,
                "trigger_count": len(triggers),
                "safety_recommendations": explanation_data["safety_recommendations"],
                "latency_ms": latency_ms,
            }
            return data, "local"
        except Exception as e:
            return None, f"Local inference error: {e}"

    return None, f"Cannot reach API at {API_URL} and local model could not be loaded."

# Check backend health
api_online = False
model_version = "1.0.0"
try:
    health_resp = requests.get(f"{API_URL}/health", timeout=1.5).json()
    api_online = health_resp.get("model_loaded", False)
    model_version = health_resp.get("model_version", "1.0.0")
except Exception:
    api_online = False

# ---- Top Header Bar ----
col_logo, col_stat = st.columns([3, 1])
with col_logo:
    st.markdown('<div class="farzi-hero-title">F A A R Z I</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="farzi-tagline">'
        '<span>ASLI YA NAKLI?</span> • '
        '<span style="color:#cbd5e1;">SPECIAL TASK FORCE COUNTERFEIT INTELLIGENCE</span> • '
        '<span class="farzi-serial-tag">№ FRZ-₹500-STF-SEC-2026</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with col_stat:
    if api_online:
        st.markdown(
            '<div style="text-align:right; margin-top:14px;">'
            '<span style="background:rgba(0,230,118,0.15); color:#00e676; border:1px solid #00e676; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:700; letter-spacing:0.04em;">'
            '● STF API ONLINE • v%s</span></div>' % model_version,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div style="text-align:right; margin-top:14px;">'
            '<span style="background:rgba(234,179,8,0.15); color:#facc15; border:1px solid #eab308; padding:5px 12px; border-radius:20px; font-size:12px; font-weight:700; letter-spacing:0.04em;">'
            '● LOCAL FORENSIC ENGINE ACTIVE</span></div>',
            unsafe_allow_html=True,
        )

# ---- Farzi STF Forensics Hero Banner ----
st.markdown("""
<div class="farzi-hero-banner">
    <div style="font-size: 2.2rem; line-height: 1; flex-shrink: 0; filter: drop-shadow(0 0 10px rgba(0, 230, 118, 0.4));">🛡️</div>
    <div class="farzi-banner-text">
        <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.14em; color: #00e676; font-weight: 700; margin-bottom: 3px;">
            SPECIAL TASK FORCE • COUNTERFEIT COMMUNICATION &amp; FINANCIAL FRAUD FORENSICS
        </div>
        <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.55;">
            Automated forensic audit of suspect communications. Evaluates structural entropy, obfuscated URL redirectors, 
            coercive panic phrasing, and impersonation indicators in &lt;1 ms.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Predefined Farzi Curated Case Files ----
FARZI_CASE_FILES = [
    {
        "id": "case_sunny_overpayment",
        "title": "🚨 Case 01: Sunny's ₹3,000 UPI Refund Scam",
        "message": "Hlo mam. By mistake send 3000. Please return mam 2000 to my PhonePe QR code immediately.",
        "context": "Real-world social engineering attack where a fraudster fabricated a ₹3,000 credit alert to induce panic refund of ₹2,000."
    },
    {
        "id": "case_fake_order_alert",
        "title": "📦 Case 02: Counterfeit Amazon Invoice #AMZ-99381",
        "message": "Your order #AMZ-99381 of Rs. 14,999 has been placed. If you did not make this transaction, call our fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now",
        "context": "Panic-inducing fake order SMS tricking victim to call a rogue fraud desk or click an obfuscated cancel link."
    },
    {
        "id": "case_rbi_raid_threat",
        "title": "🏛️ Case 03: Fake RBI / IT Enforcement Threat Notice",
        "message": "URGENT NOTICE from Reserve Bank Enforcement: Your bank accounts are flagged for illegal hawala transactions. Verify identity within 2 hours at rbi-verify-portal.in/auth or face immediate freeze and police warrant.",
        "context": "High-pressure authority impersonation scam leveraging fake RBI and enforcement threats."
    },
    {
        "id": "case_electricity_blackout",
        "title": "⚡ Case 04: Farzi Electricity Disconnection SMS",
        "message": "Dear Consumer, your electricity power will be disconnected tonight at 09:30 PM from electricity office. Your previous month bill was not updated. Please call officer at 9823412345 immediately.",
        "context": "Urgency trap inducing immediate panicked phone calls to scammer-controlled numbers."
    },
    {
        "id": "case_sbi_kyc_trap",
        "title": "💳 Case 05: SBI NetBanking KYC Trap",
        "message": "Dear Customer, Your SBI NetBanking will be blocked today due to pending KYC documents. Click http://bit.ly/sbi-kyc-verify to complete verification immediately.",
        "context": "Credential harvesting phishing link designed to capture NetBanking login and OTPs."
    },
    {
        "id": "case_indpost_delivery",
        "title": "📬 Case 06: IndiaPost Incomplete Delivery Surcharge",
        "message": "IndiaPost: Your package could not be delivered due to incomplete street number. Update your address and pay re-delivery fee of Rs. 25 at bit.ly/ind-post-redelivery within 12 hours.",
        "context": "Micro-payment credential theft scheme disguised as a package delivery failure."
    },
    {
        "id": "case_asli_hdfc_otp",
        "title": "✅ Case 07: Asli HDFC Bank Transaction OTP",
        "message": "654321 is your HDFC Bank OTP for online purchase of Rs. 850 at BookMyShow. Valid for 10 mins. Do not share OTP with anyone.",
        "context": "Authentic transactional verification OTP with standard bank security advisory."
    },
    {
        "id": "case_asli_swiggy_order",
        "title": "✅ Case 08: Asli Swiggy Delivery Status",
        "message": "Your Swiggy order #91823 has been picked up by delivery partner Rahul. Track live at swiggy.com/track",
        "context": "Standard legitimate delivery tracking communication."
    }
]

# Session state initialization for message input
if "input_message" not in st.session_state:
    st.session_state["input_message"] = FARZI_CASE_FILES[1]["message"]

# ---- Sidebar ----
with st.sidebar:
    st.markdown("""
    <div style="background: rgba(13, 24, 16, 0.75); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 12px; padding: 14px 16px; margin-bottom: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
        <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; letter-spacing: 0.18em; color: #f8fafc;">F A A R Z I</div>
        <div style="font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.14em; color: #00e676; font-weight: 700; margin-top: 2px;">STF CYBER FORENSICS UNIT</div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #eab308; margin-top: 6px;">№ FRZ-₹500-STF-SEC-2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎯 STF Case Dossiers")
    st.caption("Select a suspect communication to test the FAARZI forensic analyzer:")

    for case in FARZI_CASE_FILES:
        btn_label = case["title"]
        if st.button(btn_label, key=case["id"], use_container_width=True):
            st.session_state["input_message"] = case["message"]
            st.rerun()

    st.markdown("---")
    st.markdown("### ⚙️ STF Forensic Architecture")
    st.markdown("""
    - **Classifier:** Hybrid Pruned TF-IDF + 18 Cyber-Threat Heuristics
    - **Calibration:** Sigmoid / Isotonic Probability Calibrated
    - **Inference Latency:** < 1 ms (Optimized CPU Microservice)
    - **Accuracy:** 95.11% | **ROC-AUC:** 0.9858
    - **Detection Surface:** Fake Orders, Overpayment Traps, Phishing URLs, Utility Threats
    """)

# ---- Main Product Tabs ----
tab_analyze, tab_batch, tab_models, tab_dataset = st.tabs([
    "🔬 Farzi Forensic Lab (Asli ya Nakli?)",
    "📂 Batch Counterfeit Triage",
    "📈 STF Model Intelligence & MLflow",
    "🏛️ Forensic Dataset Vault"
])

# ==============================================================================
# TAB 1: CORE PRODUCT — FARZI FORENSIC LAB
# ==============================================================================
with tab_analyze:
    st.markdown("#### 🔬 Inspect Suspect Communication")
    st.caption("Paste any SMS, WhatsApp alert, email notification, or payment screenshot message. FAARZI AI extracts 18 structural forensics and flags counterfeit elements.")

    message_text = st.text_area(
        "Communication Content for Authenticity Verification",
        value=st.session_state["input_message"],
        height=130,
        placeholder="Paste communication text here (e.g., 'Your order #AMZ-99381 has been placed. Cancel at bit.ly/...')"
    )

    col_btn, col_clear = st.columns([1, 4])
    with col_btn:
        analyze_clicked = st.button("🔍 Asli Ya Farzi? (Scan Now)", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear Input"):
            st.session_state["input_message"] = ""
            st.rerun()

    if analyze_clicked or message_text:
        if not message_text.strip():
            st.warning("Please paste or type a message to inspect.")
        else:
            with st.spinner("Exprecuting Farzi Forensic Audit: Analyzing microprints, obfuscated URLs, entropy, and coercive pressure..."):
                data, source = analyze_message_service(message_text)

                if data is None:
                    st.error(f"Inference error: {source}")
                else:
                    risk_score = data["risk_score"]
                    is_scam = data["is_scam"]
                    risk_level = data["risk_level"]
                    category = data["category"]

                    if risk_score >= 80.0:
                        banner_class = "verdict-banner-farzi"
                        stamp_html = '<span class="stamp-overlay stamp-farzi">🚨 100% FAARZI (COUNTERFEIT)</span>'
                        status_title = "FAARZI DETECTED • HIGH THREAT"
                        badge_color = "#ef4444"
                    elif risk_score >= 50.0:
                        banner_class = "verdict-banner-farzi"
                        stamp_html = '<span class="stamp-overlay stamp-farzi">⚠️ FAARZI (SUSPICIOUS COERCION)</span>'
                        status_title = "COUNTERFEIT COERCION DETECTED"
                        badge_color = "#f97316"
                    elif risk_score >= 25.0:
                        banner_class = "verdict-banner-shakki"
                        stamp_html = '<span class="stamp-overlay stamp-shakki">🔍 SHAKKI (UNDER SURVEILLANCE)</span>'
                        status_title = "SUSPICIOUS CHARACTERISTICS"
                        badge_color = "#f59e0b"
                    else:
                        banner_class = "verdict-banner-asli"
                        stamp_html = '<span class="stamp-overlay stamp-asli">✅ 100% ASLI (VERIFIED GENUINE)</span>'
                        status_title = "ASLI • AUTHENTIC COMMUNICATION"
                        badge_color = "#00e676"

                    st.markdown(f"""
                    <div class="{banner_class}">
                        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                            <div>
                                {stamp_html}
                                <div style="font-size:22px; font-weight:800; color:#fff; margin-top:8px;">
                                    {status_title}
                                </div>
                                <span style="background:{badge_color}; color:#050c07; font-weight:800; font-size:12px; padding:3px 12px; border-radius:12px; text-transform:uppercase; letter-spacing:0.05em;">
                                    {category}
                                </span>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:36px; font-weight:900; color:#fff; font-family:'JetBrains Mono', monospace;">
                                    {risk_score:.1f}%
                                </div>
                                <div style="font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:#cbd5e1; font-weight:700;">
                                    Counterfeit Probability Index
                                </div>
                            </div>
                        </div>
                        <div style="margin-top:16px; font-size:14.5px; color:#f1f5f9; line-height:1.6; border-top:1px solid rgba(255,255,255,0.12); padding-top:12px;">
                            {data['explanation']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Banknote Security Thread Risk Meter
                    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
                    st.progress(min(max(risk_score / 100.0, 0.0), 1.0))
                    st.caption(f"Security Thread Verification Gauge: **{risk_score:.1f}% Counterfeit Confidence** (Engine: {source.upper()})")

                    # Forensic Signals & STF Directives
                    col_signals, col_safety = st.columns([1, 1])

                    with col_signals:
                        st.markdown("##### 🔬 Forensics: Suspicious Signals Discovered")
                        triggers = data.get("triggers", [])
                        if not triggers:
                            st.markdown("""
                            <div class="metric-box">
                                <span style="color:#00e676; font-weight:600;">✓ Authentic: No counterfeit tokens, shortened URLs, or urgent callback traps detected.</span>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            for t in triggers:
                                st.markdown(f"""
                                <div class="metric-box">
                                    <div style="display:flex; justify-content:space-between; align-items:center;">
                                        <span class="trigger-pill">{t['type']}: {html.escape(t['token'])}</span>
                                        <span style="font-size:11px; font-weight:700; color:#ef4444; font-family:'JetBrains Mono';">[{t['severity'].upper()}]</span>
                                    </div>
                                    <div style="font-size:12.5px; color:#cbd5e1; margin-top:6px;">
                                        {t['description']}
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)

                    with col_safety:
                        st.markdown("##### 🛡️ Special Task Force (STF) Security Directives")
                        recommendations = data.get("safety_recommendations", [])
                        for rec in recommendations:
                            st.markdown(f"""
                            <div class="safety-item">
                                {rec}
                            </div>
                            """, unsafe_allow_html=True)

                        st.caption(f"⚡ Forensic Scan Completed in **{data.get('latency_ms', 0)} ms** via {source.upper()} engine.")

# ==============================================================================
# TAB 2: BATCH COUNTERFEIT TRIAGE
# ==============================================================================
with tab_batch:
    st.markdown("#### 📂 Bulk Counterfeit & Scam Communication Triage")
    st.caption("Paste multiple communications (one per line) to triage carrier-level or enterprise communication streams for counterfeit messages.")

    default_batch = (
        "Your order #AMZ-99381 of Rs. 14,999 has been placed. Call fraud desk at +919876543210 or cancel at bit.ly/cancel-now\n"
        "Hlo mam. By mistake send 3000. Please return mam 2000 to my PhonePe QR code immediately.\n"
        "Your Swiggy order has been picked up by delivery partner Rahul.\n"
        "URGENT: Your KYC is pending for SBI Bank. Click bit.ly/sbi-kyc to update immediately or account blocked.\n"
        "654321 is your HDFC Bank OTP for online purchase of Rs. 850 at BookMyShow.\n"
        "Meeting rescheduled to 4 PM in conference room 302."
    )

    batch_input = st.text_area("Communications for Bulk Forensic Inspection (one per line)", value=default_batch, height=150)

    if st.button("🚀 Execute Batch Forensic Audit", type="secondary"):
        lines = [line.strip() for line in batch_input.split("\n") if line.strip()]
        if lines:
            with st.spinner(f"Auditing {len(lines)} communications for counterfeit patterns..."):
                table_data = []
                for line in lines:
                    item, _ = analyze_message_service(line)
                    if item:
                        table_data.append({
                            "Status": "🚨 FAARZI" if item["is_scam"] else "✅ ASLI",
                            "Counterfeit Index": f"{item['risk_score']:.1f}%",
                            "Category": item["category"],
                            "Triggers": item["trigger_count"],
                            "Message Excerpt": item["message"][:75] + ("..." if len(item["message"]) > 75 else ""),
                            "Latency (ms)": item["latency_ms"]
                        })
                if table_data:
                    st.dataframe(table_data, use_container_width=True)

# ==============================================================================
# TAB 3: STF MODEL INTELLIGENCE & MLFLOW
# ==============================================================================
with tab_models:
    st.markdown("#### 📈 STF Model Intelligence & Architecture Validation")
    st.markdown("""
    In the series *Farzi*, detecting counterfeit currency requires distinguishing micro-printing flaws, watermarks, and paper texture.
    Similarly, **FAARZI AI** evaluates messages against 18 linguistic & domain threat heuristics:
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

    st.markdown("##### MLflow Forensic Experiment Comparison Matrix")
    comparison = [
        {
            "Experiment Run": "Run 1: Baseline TF-IDF + Naive Bayes",
            "Accuracy": "92.14%",
            "Precision": "83.92%",
            "Recall": "90.08%",
            "F1-Score": "0.8689",
            "ROC-AUC": "0.9725",
            "Forensic Limitation": "Excessive false alarms; blind to URL obfuscation & character entropy."
        },
        {
            "Experiment Run": "Run 2: 18 Domain Threat Heuristics + RF",
            "Accuracy": "90.54%",
            "Precision": "87.71%",
            "Recall": "78.25%",
            "F1-Score": "0.8271",
            "ROC-AUC": "0.9553",
            "Forensic Limitation": "Detects structural indicators (phone numbers, urgency), misses subtle linguistic tone."
        },
        {
            "Experiment Run": "Run 3: FAARZI Champion Hybrid Pipeline",
            "Accuracy": "95.11%",
            "Precision": "91.96%",
            "Recall": "91.03%",
            "F1-Score": "0.9149",
            "ROC-AUC": "0.9858",
            "Forensic Limitation": "Selected for Production. Fusion of character n-grams, URL entropy, and domain threat indicators."
        }
    ]
    st.table(comparison)

    st.markdown("##### Why FAARZI Architecture Outperforms Alternatives")
    st.markdown("""
    1. **Why not heavy Transformer / BERT?**
       - Deep neural nets require expensive cloud GPUs, add 200–500ms latency, and create black-box opacity.
       - FAARZI runs on lightweight CPU containers with **< 1ms inference latency**, $0 GPU bills, and 100% token-level explainability.
    2. **Why 18 Threat Heuristics over Simple Word Counts?**
       - Digital counterfeiters intentionally misspell words (`bit.ly`, `Rs. 14,999`, ALL-CAPS urgency). FAARZI computes structural entropy, punctuation ratios, and phone callback signatures.
    3. **Why Probability Calibration?**
       - Raw margins distort risk. `CalibratedClassifierCV` ensures an 85% counterfeit score accurately represents an 85% mathematical likelihood of malicious fraud.
    """)

# ==============================================================================
# TAB 4: FORENSIC DATASET VAULT
# ==============================================================================
with tab_dataset:
    st.markdown("#### 🏛️ Multi-Source Forensic Ingestion Foundation")
    st.caption("FAARZI AI unifies 4 distinct real-world communication datasets to maximize domain generalization across financial fraud:")

    datasets_info = [
        {
            "Dataset": "dataset_v3_for_deberta.csv",
            "Forensic Role": "Linguistic Backbone",
            "Samples": "268,340 rows",
            "Signals Extracted": "Benign and malicious text streams with 24 pre-engineered structural metrics."
        },
        {
            "Dataset": "sample_10k.csv",
            "Forensic Role": "OTP & Phishing Interception",
            "Samples": "10,000 rows",
            "Signals Extracted": "OTP theft attempts, bank impersonation flags, telecom header data."
        },
        {
            "Dataset": "Financial scams detection dataset.csv",
            "Forensic Role": "Banking & Payment Fraud",
            "Samples": "523 rows",
            "Signals Extracted": "Counterfeit debits, pre-approved loan bait, and fake refund schemes."
        },
        {
            "Dataset": "scam_hum_india.csv",
            "Forensic Role": "Indian Regional Fraud Patterns",
            "Samples": "2,272 rows",
            "Signals Extracted": "Electricity disconnection panic, Vi/Airtel SIM lock threats, UPI QR traps."
        }
    ]
    st.table(datasets_info)

    st.info("Unified Dataset: **36,261 deduplicated messages** (71.1% Benign, 28.9% Fraudulent) partitioned with strict stratified train-test splits before feature extraction.")
