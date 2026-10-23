# Credit Risk Scoring Engine

End-to-end credit risk scoring system built on ~268k historical loan records. Predicts borrower default risk using Logistic Regression and XGBoost, with an interactive Streamlit dashboard for real-time risk assessment.

## Key Results & Threshold Tuning

| Metric | Logistic Regression | XGBoost (Selected) |
|---|---|---|
| **ROC-AUC** | 0.7041 | **0.7105** |
| **Precision** | 55.67% | **59.11%** |
| **Accuracy** | 78.53% | **78.58%** |

### Decision Threshold Adjustment
At the default 50% probability cutoff, XGBoost missed 92.8% of actual defaults (7.2% Recall). Lowering the decision threshold to a **25% risk cutoff** increased **Recall to 58.1%**, capturing significantly more default risk and prioritizing loss prevention.

## Project Structure

```text
├── data/              # Raw dataset (git-ignored)
├── models/            # Saved artifacts (.pkl)
├── notebooks/
│   └── eda.ipynb      # EDA and cleaning logic
├── src/
│   ├── preprocess.py  # Data pipeline
│   ├── train.py       # Training script
│   └── evaluate.py    # Performance evaluation
├── app.py             # Streamlit web app
├── requirements.txt   # Dependencies
└── README.md
```

## Kickstart

1. Install dependencies: `pip install -r requirements.txt`
2. Run preprocessing: `python src/preprocess.py`
3. Train models: `python src/train.py`
4. Evaluate models: `python src/evaluate.py`
5. Launch the dashboard: `python -m streamlit run app.py`

## Tech Stack
Language: Python
Data & ML: Pandas, NumPy, Scikit-Learn, XGBoost
Deployment: Streamlit, Joblib