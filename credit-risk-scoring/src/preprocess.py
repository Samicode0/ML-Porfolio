import pandas as pd
import numpy as np

def load_and_preprocess_data(filepath):
    """
    Loads raw credit data, filters columns, cleans target,
    encodes features, and handles missing values.
    """
    # Columns to keep
    keep_cols = [
        "loan_amnt", "term", "int_rate", "installment",
        "grade", "emp_length", "home_ownership", "annual_inc",
        "verification_status", "purpose", "dti",
        "delinq_2yrs", "inq_last_6mths", "open_acc",
        "revol_util", "total_acc", "pub_rec",
        "loan_status"
    ]
    
    # Load raw data
    df = pd.read_csv(filepath, usecols=keep_cols, low_memory=False)
    
    # Clean target variable
    good = ["Fully Paid", "Does not meet the credit policy. Status:Fully Paid"]
    bad = ["Charged Off", "Default", "Does not meet the credit policy. Status:Charged Off", "Late (31-120 days)"]
    
    df = df[df["loan_status"].isin(good + bad)].copy()
    df["loan_status"] = df["loan_status"].apply(lambda x: 1 if x in bad else 0)
    
    # Clean numeric features
    df["term"] = df["term"].str.replace(" months", "").astype(int)
    
    def clean_emp(val):
        if pd.isna(val): return 0
        val = str(val)
        if "10+" in val: return 10
        elif "< 1" in val: return 0
        else: return int(val.split()[0])
        
    df["emp_length"] = df["emp_length"].apply(clean_emp)
    
    grade_map = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}
    df["grade"] = df["grade"].map(grade_map)
    
    # Handle categorical features
    df = df[df["home_ownership"].isin(["MORTGAGE", "RENT", "OWN"])]
    df = pd.get_dummies(df, columns=["home_ownership", "purpose", "verification_status"], drop_first=True)
    
    # Handle missing values
    cols_with_missing = ["delinq_2yrs", "inq_last_6mths", "open_acc", "pub_rec", "total_acc", "revol_util"]
    for col in cols_with_missing:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
            
    return df

if __name__ == "__main__":
    # Test script standalone
    data = load_and_preprocess_data("data/loan.csv")
    print("Preprocessing successful! Processed shape:", data.shape)