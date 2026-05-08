import pandas as pd

def clean_data(df):
    report = []

    # Step 1: Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    removed = before - after
    report.append(f"🗑️ Removed {removed} duplicate rows")

    # Step 2: Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    report.append("✅ Standardized column names (lowercase + underscores)")

    # Step 3: Handle missing values
    missing_before = df.isnull().sum().sum()
    for col in df.columns:
        if df[col].dtype in ["object", "string"]:
            df[col] = df[col].fillna("Unknown")
        elif df[col].dtype in ["float64", "int64", "Float64", "Int64"]:
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna("Unknown")
    report.append(f"🔧 Fixed {missing_before} missing values")

    # Step 4: Strip whitespace from text columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    report.append("✂️ Stripped whitespace from text columns")

    return df, report