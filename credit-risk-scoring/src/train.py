import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from preprocess import load_and_preprocess_data
def train_models():
    print("Loading and preprocessing data...")
    df = load_and_preprocess_data("data/loan.csv")
    
    print("Data loaded. Shape:", df.shape)

    # Separate Features (X) and Target (y)
    X = df.drop("loan_status", axis=1)
    y = df["loan_status"]
    print("Target distribution:")
    print(y.value_counts())
    
    # Split into Train (80%) and Test (20%)
    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape:  {X_test.shape}")

    # Scale features
    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save Scaler and Feature Names
    os.makedirs("models", exist_ok=True)
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(X.columns.tolist(), "models/feature_names.pkl")
    
    print("Scaler and feature list saved into models/ folder.")

    # Train Logistic Regression
    print("Training Logistic Regression...")
    log_reg = LogisticRegression(max_iter=1000, random_state=42)
    log_reg.fit(X_train_scaled, y_train)
    
    # Save trained Logistic Regression model
    joblib.dump(log_reg, "models/logistic_regression.pkl")
    print("Logistic Regression model saved.")

    # Train XGBoost
    print("Training XGBoost...")
    xgb = XGBClassifier(
        n_estimators=100,
        learning_rate=0.05,
        random_state=42,
        eval_metric="logloss"
    )
    xgb.fit(X_train_scaled, y_train)
    
    # Save trained XGBoost model
    joblib.dump(xgb, "models/xgboost.pkl")
    print("XGBoost model saved.")

    # Save test dataset for evaluation
    joblib.dump((X_test_scaled, y_test), "models/test_data.pkl")
    print("Test data saved for evaluation.")
    print("\nAll training complete!")
if __name__ == "__main__":
    train_models()