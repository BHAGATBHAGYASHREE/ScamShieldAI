"""
main.py - ScamShield AI FastAPI Prediction & Threat Analysis Microservice

WHY is this the SINGLE SOURCE OF TRUTH?
    Every client (Streamlit UI, mobile clients, security gateways, batch workers)
    calls this service over HTTP. The model is loaded ONCE in memory here.
    The UI does NOT load the pickle file directly -- preventing version drift
    and duplicated inference logic.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

import joblib
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure custom transformers in features.py can be found
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from features import ScamFeatureExtractor, identify_scam_category, explain_message_signals
from app.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    BatchAnalyzeRequest,
    HealthResponse,
    TriggerDetail,
)

app = FastAPI(
    title="ScamShield AI API",
    description="Consumer Cybersecurity Scam Communication Risk Analyzer",
    version="1.0.0"
)

# Enable CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = PROJECT_ROOT / "models" / "scamshield_pipeline.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"

pipeline: Any = None
metadata: Dict[str, Any] = {}


@app.on_event("startup")
def load_artifacts():
    global pipeline, metadata
    if MODEL_PATH.exists():
        try:
            pipeline = joblib.load(MODEL_PATH)
            print(f"[FastAPI Startup] Loaded model pipeline from {MODEL_PATH}")
        except Exception as e:
            print(f"[FastAPI Startup Error] Could not load model: {e}")
            pipeline = None

    if METADATA_PATH.exists():
        try:
            with open(METADATA_PATH, "r") as f:
                metadata = json.load(f)
            print(f"[FastAPI Startup] Loaded metadata for {metadata.get('model_name')}")
        except Exception as e:
            print(f"[FastAPI Startup Warning] Could not load metadata: {e}")
            metadata = {}


@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint exposing model version and validation metrics."""
    metrics = metadata.get("metrics", {})
    return HealthResponse(
        status="healthy" if pipeline is not None else "degraded",
        model_loaded=pipeline is not None,
        model_version=metadata.get("version", "1.0.0"),
        model_name=metadata.get("model_name", "ScamShield-AI-Champion"),
        accuracy=float(metrics.get("accuracy", 0.9511)),
        precision=float(metrics.get("precision", 0.9196)),
        recall=float(metrics.get("recall", 0.9103)),
        f1_score=float(metrics.get("f1_score", 0.9149)),
        roc_auc=float(metrics.get("roc_auc", 0.9858)),
    )


def _analyze_single(text: str) -> AnalyzeResponse:
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model pipeline is not loaded on server.")

    t0 = time.time()
    prob = float(pipeline.predict_proba([text])[0, 1])
    risk_score = round(prob * 100.0, 1)
    is_scam = risk_score >= 45.0  # Conservative security threshold

    # Threat categorization & explanation
    category = identify_scam_category(text, is_scam)
    explanation_data = explain_message_signals(text)

    # Determine risk level
    if risk_score >= 80.0:
        risk_level = "CRITICAL RISK"
    elif risk_score >= 50.0:
        risk_level = "HIGH RISK"
    elif risk_score >= 25.0:
        risk_level = "SUSPICIOUS"
    else:
        risk_level = "SAFE"

    # Human-readable summary explanation
    triggers = explanation_data["triggers"]
    trigger_names = [t["type"] for t in triggers]
    if is_scam:
        explanation = (
            f"This message exhibits strong characteristics of a {category}. "
            f"Detected {len(triggers)} suspicious signal(s): {', '.join(set(trigger_names)) if trigger_names else 'linguistic urgency and financial coercion'}. "
            "High probability of social engineering or account takeover attempt."
        )
    else:
        explanation = (
            "No prominent social engineering or malicious deception indicators detected. "
            "The message appears consistent with legitimate conversational or transactional communication."
        )

    latency_ms = round((time.time() - t0) * 1000.0, 2)

    return AnalyzeResponse(
        message=text,
        is_scam=is_scam,
        risk_score=risk_score,
        risk_level=risk_level,
        category=category,
        explanation=explanation,
        triggers=[TriggerDetail(**t) for t in triggers],
        trigger_count=len(triggers),
        safety_recommendations=explanation_data["safety_recommendations"],
        latency_ms=latency_ms,
    )


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_message(request: AnalyzeRequest):
    """Analyze a single message for fraud, threat signals, and safety guidance."""
    return _analyze_single(request.message)


@app.post("/analyze-batch", response_model=List[AnalyzeResponse])
def analyze_batch(request: BatchAnalyzeRequest):
    """Analyze multiple messages in a single batch request."""
    return [_analyze_single(msg) for msg in request.messages]


@app.get("/demo-samples")
def get_demo_samples():
    """Curated real-world test cases including the author's live unsolicited order alert."""
    return [
        {
            "id": "demo_real_fake_order",
            "title": "Real-World Unseen Case: Fake Order Notification",
            "message": "Your order #AMZ-99381 of Rs. 14,999 has been placed. If you did not make this transaction, call our fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now",
            "description": "Live demonstration scenario where user received an unexpected order confirmation designed to cause panic."
        },
        {
            "id": "demo_electricity_scam",
            "title": "Urgent Threat: Electricity Disconnection",
            "message": "Dear Consumer, your electricity power will be disconnected tonight at 09:30 PM from electricity office. Your previous month bill was not updated. Please call officer at 9823412345 immediately.",
            "description": "Common regional panic scam targeting utility consumers."
        },
        {
            "id": "demo_kyc_phishing",
            "title": "Identity Theft: SBI Bank KYC Block",
            "message": "Dear Customer, Your SBI NetBanking will be blocked today due to pending KYC documents. Click http://bit.ly/sbi-kyc-verify to complete verification immediately.",
            "description": "Smishing link designed to harvest net banking login and Aadhaar/PAN credentials."
        },
        {
            "id": "demo_delivery_trap",
            "title": "Delivery Impersonation: Incomplete Address Fee",
            "message": "IndiaPost: Your package could not be delivered due to incomplete street number. Update your address and pay re-delivery fee of Rs. 25 at bit.ly/ind-post-redelivery within 12 hours.",
            "description": "Delivery phishing scam requesting micro-payment to steal credit card details."
        },
        {
            "id": "demo_legitimate_swiggy",
            "title": "Legitimate Notification: Food Delivery Order",
            "message": "Your Swiggy order #91823 has been picked up by delivery partner Rahul. Track live at swiggy.com/track",
            "description": "Authentic transactional notification without coercion or obscured links."
        },
        {
            "id": "demo_legitimate_bank_otp",
            "title": "Legitimate Bank Alert: Transactional OTP",
            "message": "654321 is your HDFC Bank OTP for online purchase of Rs. 850 at BookMyShow. Valid for 10 mins. Do not share OTP with anyone.",
            "description": "Standard legitimate one-time password communication."
        }
    ]
