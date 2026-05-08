import pandas as pd

def calculate_kpis(df):
    kpis = {}

    # Dynamically detect column types
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    date_cols = [c for c in df.columns if any(x in c.lower() for x in ["date", "time", "month", "year"])]

    # KPI 1: Stats for each numeric column
    for col in numeric_cols[:3]:  # Max 3 numeric columns
        kpis[f"Total {col}"] = round(df[col].sum(), 2)
        kpis[f"Avg {col}"] = round(df[col].mean(), 2)

    # KPI 2: Top category for first categorical + first numeric
    if categorical_cols and numeric_cols:
        cat = categorical_cols[0]
        num = numeric_cols[0]
        top = df.groupby(cat)[num].sum().idxmax()
        top_val = df.groupby(cat)[num].sum().max()
        kpis[f"Top {cat}"] = f"{top} ({round(top_val, 2)})"

    # KPI 3: Date trend if available
    if date_cols and numeric_cols:
        try:
            date_col = date_cols[0]
            num = numeric_cols[0]
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            monthly = df.groupby(df[date_col].dt.to_period("M"))[num].sum()
            if len(monthly) >= 2:
                growth = ((monthly.iloc[-1] - monthly.iloc[0]) / monthly.iloc[0]) * 100
                kpis["Growth (First vs Last Period)"] = f"{round(growth, 2)}%"
            kpis["Best Period"] = str(monthly.idxmax())
        except:
            pass

    # KPI 4: Always show
    kpis["Total Records"] = len(df)
    kpis["Total Columns"] = len(df.columns)

    return kpis