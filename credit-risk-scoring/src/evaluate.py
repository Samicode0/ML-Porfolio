import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

def evaluate_models():
    # Load saved models and test dataset
    print("Loading models and test data...")
    log_reg = joblib.load("models/logistic_regression.pkl")
    xgb = joblib.load("models/xgboost.pkl")
    X_test_scaled, y_test = joblib.load("models/test_data.pkl")
    
    print(f"Loaded test dataset with {len(y_test)} rows.")

    # Predictions for Logistic Regression
    y_pred_log = log_reg.predict(X_test_scaled)
    y_prob_log = log_reg.predict_proba(X_test_scaled)[:, 1]

    # Predictions for XGBoost
    y_pred_xgb = xgb.predict(X_test_scaled)
    y_prob_xgb = xgb.predict_proba(X_test_scaled)[:, 1]

    # Metrics for both models
    results = pd.DataFrame({
        "Metric": ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"],
        "Logistic Regression": [
            accuracy_score(y_test, y_pred_log),
            precision_score(y_test, y_pred_log),
            recall_score(y_test, y_pred_log),
            f1_score(y_test, y_pred_log),
            roc_auc_score(y_test, y_prob_log)
        ],
        "XGBoost": [
            accuracy_score(y_test, y_pred_xgb),
            precision_score(y_test, y_pred_xgb),
            recall_score(y_test, y_pred_xgb),
            f1_score(y_test, y_pred_xgb),
            roc_auc_score(y_test, y_prob_xgb)
        ]
    })

    print("\n Model Comparison ")
    print(results.round(4).to_string(index=False))

    # Confusion Matrix for XGBoost
    print("\n XGBoost Confusion Matrix (at default 50% threshold) ")
    cm = confusion_matrix(y_test, y_pred_xgb)
    print(cm)
    
    #  Threshold Adjustment 
    print("\n Threshold Optimization (XGBoost at 25% Risk Cutoff) ")
    # Instead of default 0.5, flag anyone with > 25% risk probability
    y_pred_25 = (y_prob_xgb >= 0.25).astype(int)
    
    print(f"Recall at 25% threshold:    {recall_score(y_test, y_pred_25):.4f}")
    print(f"Precision at 25% threshold: {precision_score(y_test, y_pred_25):.4f}")

if __name__ == "__main__":
    evaluate_models()