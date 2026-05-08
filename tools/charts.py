import plotly.express as px
import pandas as pd

def generate_charts(df):
    charts = []

    col = df.columns.tolist()

    # Find key columns
    sales_col = next((c for c in col if any(x in c for x in ["sales", "revenue", "amount", "total"])), None)
    date_col = next((c for c in col if any(x in c for x in ["date", "order_date", "month", "year"])), None)
    cat_col = next((c for c in col if any(x in c for x in ["category", "segment", "product", "region"])), None)

    # Chart 1: Revenue by Category (Bar Chart)
    if cat_col and sales_col:
        cat_data = df.groupby(cat_col)[sales_col].sum().reset_index()
        cat_data = cat_data.sort_values(sales_col, ascending=False)

        fig1 = px.bar(
            cat_data,
            x=cat_col,
            y=sales_col,
            title="💰 Revenue by Category",
            color=sales_col,
            color_continuous_scale="Blues"
        )
        charts.append(fig1)

    # Chart 2: Revenue Over Time (Line Chart)
    if date_col and sales_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        monthly = df.groupby(df[date_col].dt.to_period("M"))[sales_col].sum().reset_index()
        monthly[date_col] = monthly[date_col].astype(str)

        fig2 = px.line(
            monthly,
            x=date_col,
            y=sales_col,
            title="📈 Revenue Trend Over Time",
            markers=True
        )
        charts.append(fig2)

    # Chart 3: Category Share (Pie Chart)
    if cat_col and sales_col:
        fig3 = px.pie(
            cat_data,
            names=cat_col,
            values=sales_col,
            title="🥧 Revenue Share by Category"
        )
        charts.append(fig3)

    return charts