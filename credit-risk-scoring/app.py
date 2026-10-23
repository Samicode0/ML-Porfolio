import streamlit as st
import pandas as pd
import numpy as np
import joblib


st.set_page_config(page_title="Credit Risk Engine", layout="centered")


@st.cache_resource
def load_assets():
    xgb_model = joblib.load("models/xgboost.pkl")
    scaler = joblib.load("models/scaler.pkl")
    feature_names = joblib.load("models/feature_names.pkl")
    return xgb_model, scaler, feature_names

xgb, scaler, feature_names = load_assets()

# HEADER & SETTINGS 
st.title("🏦 Credit Risk Scoring Engine")
st.write("Predict loan default risk using an XGBoost Machine Learning model.")

# Business logic slider
st.sidebar.header("Bank Settings")
threshold = st.sidebar.slider("Approval Risk Threshold", min_value=10, max_value=50, value=25, step=1, help="Flag applicants as risky if their default probability exceeds this percentage.")

# -USER INPUTS
st.subheader("Applicant Details")
col1, col2 = st.columns(2)

with col1:
    loan_amnt = st.number_input("Loan Amount ($)", min_value=1000, max_value=50000, value=10000)
    annual_inc = st.number_input("Annual Income ($)", min_value=10000, max_value=200000, value=60000)
    term = st.selectbox("Loan Term (Months)", [36, 60])
    int_rate = st.slider("Interest Rate (%)", 5.0, 25.0, 10.5)

with col2:
    dti = st.slider("Debt-to-Income Ratio (DTI %)", 1.0, 50.0, 15.0)
    home_ownership = st.selectbox("Home Ownership", ["MORTGAGE", "RENT", "OWN"])
    purpose = st.selectbox("Loan Purpose", ["debt_consolidation", "credit_card", "home_improvement", "car", "other"])

# PREDICTION LOGIC
if st.button("Calculate Risk Score", type="primary"):
    
    # Dictionary of all 31 features
    input_data = {col: 0 for col in feature_names}
    
    # Fill in user inputs
    input_data["loan_amnt"] = loan_amnt
    input_data["annual_inc"] = annual_inc
    input_data["term"] = term
    input_data["int_rate"] = int_rate
    input_data["dti"] = dti
    
    # Baseline defaults for the hidden columns 
    input_data["emp_length"] = 5
    input_data["grade"] = 3
    input_data["delinq_2yrs"] = 0
    input_data["inq_last_6mths"] = 0
    input_data["open_acc"] = 10
    input_data["revol_util"] = 50.0
    input_data["total_acc"] = 20
    
    # Handle One-Hot Encoded variables
    if f"home_ownership_{home_ownership}" in input_data:
        input_data[f"home_ownership_{home_ownership}"] = 1
        
    if f"purpose_{purpose}" in input_data:
        input_data[f"purpose_{purpose}"] = 1

    # Convert to dataframe in the exact column order the model expects
    df_input = pd.DataFrame([input_data])[feature_names]
    
    # Scale and Predict
    scaled_input = scaler.transform(df_input)
    risk_prob = xgb.predict_proba(scaled_input)[0][1] * 100  # Convert to percentage
    
    #  DISPLAY RESULTS
    st.divider()
    st.subheader("Results")
    
    # Display the percentage
    st.metric(label="Calculated Default Risk", value=f"{risk_prob:.1f}%")
    
    # Business Decision Logic
    if risk_prob > threshold:
        st.error(f"🛑 **REJECTED:** Risk score exceeds the bank's maximum threshold of {threshold}%.")
    else:
        st.success(f"✅ **APPROVED:** Risk score is safely below the {threshold}% threshold.")