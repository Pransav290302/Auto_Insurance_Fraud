# Which CSV to use for training – best accuracy

Your project can use different CSV files for training. Here's how they compare and which to use for the **best fraud prediction accuracy**.

---

## Option 1: **insurance_claims_fraud.csv** (recommended for best accuracy)

**Location:** Project root or `uploads/insurance_claims_fraud.csv`

| | |
|---|---|
| **Rows** | ~10,200 |
| **Fraud balance** | ~50% fraud / 50% legit (balanced) |
| **Columns** | **39** (many useful features) |

**Why it gives the best results:**
- **Balanced classes** – The model sees similar numbers of fraud and legit claims, so it learns both patterns well.
- **Rich features** – Includes injury_claim, property_claim, vehicle_claim, auto_make, demographics, policy details, etc. More signal = better accuracy and F1.
- **Standard dataset** – The pipeline is tuned for this structure.

**Use this when:** You want the **highest accuracy and best fraud detection (F1/recall)**.

---

## Option 2: **claims_data.csv** (uploaded data)

**Location:** `uploads/claims_data.csv` (created when you upload a file)

| | |
|---|---|
| **Rows** | 30,000 (in your case) |
| **Fraud balance** | ~11.5% fraud (imbalanced) |
| **Columns** | 24 (fewer than Option 1) |

**Pros:** More rows; realistic imbalance.  
**Cons:** Fewer columns and heavy imbalance; the model may predict "not fraud" often and accuracy can look high only because most claims are legit.

**Use this when:** You want to train on **your own uploaded data**.

---

## How the app chooses the file

1. **uploads/claims_data.csv** (if it exists)
2. **uploads/insurance_claims_fraud.csv**
3. **insurance_claims_fraud.csv** (project root)

To get **best accuracy** with the standard dataset: use **insurance_claims_fraud.csv**. If `uploads/claims_data.csv` exists and you want the standard file instead, delete or rename `uploads/claims_data.csv`, then retrain (delete `fraud_severity_models.pkl` and open Dashboard).

---

## Summary

| Goal | Use this file |
|------|----------------|
| **Best accuracy / best fraud detection** | **insurance_claims_fraud.csv** (root or uploads), no claims_data.csv |
| **Your own data** | Upload your CSV → **uploads/claims_data.csv** |

After changing the dataset, delete **fraud_severity_models.pkl** and open the Dashboard to retrain.
