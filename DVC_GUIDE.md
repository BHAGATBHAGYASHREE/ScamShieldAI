# ScamShield AI — DVC Data & Pipeline Guide

## 1. Why DVC for ScamShield AI?
Git is engineered for source code, not multi-gigabyte or rapidly evolving dataset snapshots. In cybersecurity and smishing detection:
- Scam tactics mutate rapidly (new domain registrars, new UPI handles, emerging APK malware).
- Training datasets grow with incoming victim reports.
- `DVC` (Data Version Control) connects Git commits to specific dataset versions and guarantees that our multi-stage pipeline is **100% reproducible**.

---

## 2. Pipeline Architecture (`dvc.yaml`)

```
+-----------------------------------+
|  Stage 1: prepare_data            |
|  python src/data_loader.py        |
+-----------------+-----------------+
                  |
                  | [Produces: train.csv, test.csv]
                  v
+-----------------------------------+
|  Stage 2: train_and_evaluate      |
|  python src/train_mlflow.py       |
+-----------------+-----------------+
                  |
                  | [Produces: scamshield_pipeline.joblib, metadata.json]
                  v
               Champion Model
```

---

## 3. Core DVC Workflow Commands

### Initialize DVC
```bash
cd "ScamShield AI"
dvc init
```

### Track the Raw Datasets
```bash
dvc add data/raw/
git add data/raw.dvc .gitignore
git commit -m "dvc: track raw smishing and scam datasets"
```

### Reproduce the Full Pipeline
```bash
dvc repro
```
*If inputs have not changed, DVC skips computation and reports `Data and pipelines are up to date`.*

### Visualize the Pipeline Graph
```bash
dvc dag
```
Output:
```
+------------------+
| prepare_data     |
+------------------+
         *
         *
         *
+--------------------+
| train_and_evaluate |
+--------------------+
```
