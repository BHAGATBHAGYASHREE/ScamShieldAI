"""
schemas.py - Pydantic Request & Response Data Contracts for ScamShield AI
"""
from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="The SMS, WhatsApp, or email message text to analyze for fraud.",
        json_schema_extra={"example": "Your order #AMZ-99381 of Rs. 14,999 has been placed. Call fraud desk immediately at +919876543210 or cancel at bit.ly/cancel-order-now"}
    )


class BatchAnalyzeRequest(BaseModel):
    messages: List[str] = Field(
        ...,
        min_length=1,
        max_length=100,
        description="List of raw messages to analyze in batch."
    )


class TriggerDetail(BaseModel):
    type: str
    token: str
    severity: str
    description: str


class AnalyzeResponse(BaseModel):
    message: str
    is_scam: bool
    risk_score: float = Field(..., ge=0.0, le=100.0, description="Calibrated threat score from 0 (Safe) to 100 (Extreme Danger)")
    risk_level: str = Field(..., description="Risk category: SAFE, SUSPICIOUS, HIGH RISK, CRITICAL RISK")
    category: str = Field(..., description="Identified threat category")
    explanation: str = Field(..., description="High-level human explanation of the risk verdict")
    triggers: List[TriggerDetail]
    trigger_count: int
    safety_recommendations: List[str]
    latency_ms: float


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_version: str
    model_name: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
