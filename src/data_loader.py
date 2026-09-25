"""
data_loader.py - ScamShield AI Unified Data Ingestion & Leakage-Safe Splitting

WHY this design?
  1. LEAKAGE PREVENTION:
     Data split MUST happen before any vectorizer or preprocessor is fitted.
     Otherwise, test set vocabulary leaks into the TF-IDF vocabulary (Section 12 of course).
  2. STRATIFICATION:
     We stratify by label to preserve the ~71% benign / ~29% scam ratio in both train and test.
  3. MULTI-SOURCE SYNERGY:
     Integrates 4 specialized datasets:
       - dataset_v3_for_deberta.csv (core linguistic corpus)
       - sample_10k.csv (OTP and phishing intent)
       - Financial scams detection dataset.csv (banking fraud patterns)
       - scam_hum_india.csv (Indian regional context, UPI, telecom)
"""
from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_raw_datasets(deberta_sample_size: int = 25000) -> pd.DataFrame:
    """Load and unify all 4 raw datasets into a single standardized schema."""
    frames = []

    # 1. Financial scams detection dataset
    fin_path = RAW_DIR / "Financial scams detection dataset.csv"
    if fin_path.exists():
        df_fin = pd.read_csv(fin_path)[["message", "label"]].dropna()
        df_fin["label"] = df_fin["label"].astype(str).str.lower().map({"scam": 1, "ham": 0}).fillna(0).astype(int)
        df_fin["source"] = "financial_scams"
        frames.append(df_fin)

    # 2. Indian scam/spam dataset
    ind_path = RAW_DIR / "scam_hum_india.csv"
    if ind_path.exists():
        df_ind = pd.read_csv(ind_path)
        col_text = "text" if "text" in df_ind.columns else df_ind.columns[0]
        col_label = "label" if "label" in df_ind.columns else df_ind.columns[1]
        df_ind = df_ind.rename(columns={col_text: "message", col_label: "label"})[["message", "label"]].dropna()
        df_ind["label"] = df_ind["label"].astype(str).str.lower().map({"spam": 1, "ham": 0}).fillna(0).astype(int)
        df_ind["source"] = "scam_hum_india"
        frames.append(df_ind)

    # 3. OTP & Phishing 10k dataset
    otp_path = RAW_DIR / "sample_10k.csv"
    if otp_path.exists():
        df_otp = pd.read_csv(otp_path)
        col_msg = "sms_text" if "sms_text" in df_otp.columns else "message"
        df_otp = df_otp.rename(columns={col_msg: "message"})
        if "is_phishing_original" in df_otp.columns:
            df_otp["label"] = df_otp["is_phishing_original"].map({True: 1, False: 0, "True": 1, "False": 0}).fillna(0).astype(int)
        else:
            df_otp["label"] = 0
        df_otp = df_otp[["message", "label"]].dropna()
        df_otp["source"] = "sample_10k"
        frames.append(df_otp)

    # 4. DeBERTa v3 large corpus (sampled for computational efficiency & speed)
    deb_path = RAW_DIR / "dataset_v3_for_deberta.csv"
    if deb_path.exists():
        df_deb = pd.read_csv(deb_path, usecols=["message", "label"], nrows=deberta_sample_size)
        df_deb["label"] = df_deb["label"].astype(int)
        df_deb = df_deb.dropna()
        df_deb["source"] = "deberta_v3_sample"
        frames.append(df_deb)

    if not frames:
        raise FileNotFoundError(f"No datasets found in {RAW_DIR}")

    combined = pd.concat(frames, ignore_index=True)
    combined["message"] = combined["message"].astype(str).str.strip()
    # Remove empty or whitespace-only messages
    combined = combined[combined["message"].str.len() > 3].drop_duplicates(subset=["message"]).reset_index(drop=True)

    print(f"Total Unified Messages: {len(combined):,}")
    print(f"Label Counts:\n{combined['label'].value_counts(normalize=True)}")
    return combined


def split_and_save_data(
    test_size: float = 0.2, random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Perform leakage-safe stratified split and write to processed directory."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = load_raw_datasets()

    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df["label"],
    )

    train_path = PROCESSED_DIR / "train.csv"
    test_path = PROCESSED_DIR / "test.csv"

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    print(f"Saved Train Set: {len(train_df):,} rows -> {train_path}")
    print(f"Saved Test Set:  {len(test_df):,} rows -> {test_path}")
    return train_df, test_df


if __name__ == "__main__":
    split_and_save_data()
