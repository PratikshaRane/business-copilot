import pandas as pd

def calculate_kpis(df):
    kpis = {}
    
    # Detect common column name variations
    col = df.columns.tolist()

    # Find sales/revenue column
    sales_col = next((c for c in col if any(x in c for x in ["sales", "revenue", "amount", "total"])), None)
    
    # Find date column
    date_col = next((c for c in col if any(x in c for x in ["date", "order_date", "month", "year"])), None)
    
    # Find category column
    cat_col = next((c for c in col if any(x in c for x in ["category", "segment", "product", "region"])), None)

    # KPI 1: Total Revenue
    if sales_col:
        kpis["Total Revenue"] = round(df[sales_col].sum(), 2)
        kpis["Average Order Value"] = round(df[sales_col].mean(), 2)
        kpis["Max Single Sale"] = round(df[sales_col].max(), 2)

    # KPI 2: Top Category
    if cat_col and sales_col:
        top_cat = df.groupby(cat_col)[sales_col].sum().idxmax()
        top_cat_val = df.groupby(cat_col)[sales_col].sum().max()
        kpis["Top Category"] = f"{top_cat} (${round(top_cat_val, 2)})"

    # KPI 3: Monthly trend (if date exists)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df["month"] = df[date_col].dt.to_period("M")
        
        if sales_col:
            monthly = df.groupby("month")[sales_col].sum()
            if len(monthly) >= 2:
                growth = ((monthly.iloc[-1] - monthly.iloc[0]) / monthly.iloc[0]) * 100
                kpis["Revenue Growth (First vs Last Month)"] = f"{round(growth, 2)}%"
            kpis["Best Month"] = str(monthly.idxmax())
            kpis["Worst Month"] = str(monthly.idxmin())

    # KPI 4: Total Orders
    kpis["Total Records"] = len(df)

    return kpis