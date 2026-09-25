"""
test_pipeline.py - Unit tests for ScamShield AI feature extraction and pipeline
"""
from pathlib import Path
import pytest
import numpy as np
import pandas as pd
import joblib

import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from features import ScamFeatureExtractor, identify_scam_category, explain_message_signals


@pytest.fixture(scope="session")
def pipeline():
    model_path = PROJECT_ROOT / "models" / "scamshield_pipeline.joblib"
    assert model_path.exists(), "Model artifact not found. Run train_mlflow.py first."
    return joblib.load(model_path)


def test_feature_extractor_columns():
    extractor = ScamFeatureExtractor()
    sample = ["Test message with bit.ly link and Rs 500"]
    df_feat = extractor.transform(sample)

    assert isinstance(df_feat, pd.DataFrame)
    assert df_feat.shape[0] == 1
    assert "has_shortened_url" in df_feat.columns
    assert "urgency_score" in df_feat.columns
    assert "char_entropy" in df_feat.columns
    assert df_feat["has_shortened_url"].iloc[0] == 1.0


def test_feature_extractor_edge_cases():
    extractor = ScamFeatureExtractor()
    edge_cases = ["", " ", "!!!???", "1234567890", "http://legit.com"]
    df_feat = extractor.transform(edge_cases)
    assert df_feat.shape[0] == len(edge_cases)
    assert not df_feat.isna().any().any()


def test_pipeline_prediction_on_real_fake_order(pipeline):
    fake_order_msg = (
        "Your order #AMZ-99381 of Rs. 14,999 has been placed. "
        "Call fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now"
    )
    prob = pipeline.predict_proba([fake_order_msg])[0, 1]
    pred = pipeline.predict([fake_order_msg])[0]

    assert pred == 1, "The unsolicited fake order message should be flagged as Scam (1)"
    assert prob >= 0.80, f"Expected high risk probability, got {prob:.4f}"


def test_pipeline_prediction_on_legitimate_message(pipeline):
    legit_msg = "Hey Rahul, let's meet for lunch at the cafeteria around 1 PM tomorrow."
    prob = pipeline.predict_proba([legit_msg])[0, 1]
    assert prob < 0.35, f"Expected low risk probability for benign message, got {prob:.4f}"


def test_threat_categorization():
    fake_order = "Your Amazon order #402-991 has been confirmed and shipped."
    cat_order = identify_scam_category(fake_order, is_scam=True)
    assert cat_order == "Fake Order"

    kyc_msg = "Your SBI account is blocked due to incomplete KYC. Update PAN."
    cat_kyc = identify_scam_category(kyc_msg, is_scam=True)
    assert cat_kyc == "KYC / Identity Threat"

    benign = "Hello Mom, reaching home in 10 minutes."
    cat_benign = identify_scam_category(benign, is_scam=False)
    assert cat_benign == "Legitimate / Benign"


def test_signal_explanation_triggers():
    msg = "URGENT: Call +919876543210 immediately to claim Rs 50,000 lottery reward at bit.ly/prize"
    explanation = explain_message_signals(msg)

    assert explanation["trigger_count"] >= 3
    types = [t["type"] for t in explanation["triggers"]]
    assert "Shortened Link" in types
    assert "Phone Callback" in types
    assert "Urgency Trigger" in types
    assert len(explanation["safety_recommendations"]) > 0
