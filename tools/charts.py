import plotly.express as px
import pandas as pd

def generate_charts(df):
    charts = []

    # Dynamically find numeric and categorical columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "string"]).columns.tolist()
    date_cols = [c for c in df.columns if any(x in c.lower() for x in ["date", "time", "month", "year"])]

    if not numeric_cols:
        return charts

    main_num = numeric_cols[0]  # First numeric column as main metric

    # Chart 1: Bar chart — top categorical column vs main numeric
    if categorical_cols:
        main_cat = categorical_cols[0]
        cat_data = df.groupby(main_cat)[main_num].sum().reset_index()
        cat_data = cat_data.sort_values(main_num, ascending=False).head(10)
        fig1 = px.bar(
            cat_data,
            x=main_cat,
            y=main_num,
            title=f"📊 {main_num} by {main_cat}",
            color=main_num,
            color_continuous_scale="Blues"
        )
        charts.append(fig1)

    # Chart 2: Line chart — date trend if date column exists
    if date_cols:
        date_col = date_cols[0]
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
            monthly = df.groupby(df[date_col].dt.to_period("M"))[main_num].sum().reset_index()
            monthly[date_col] = monthly[date_col].astype(str)
            fig2 = px.line(
                monthly,
                x=date_col,
                y=main_num,
                title=f"📈 {main_num} Trend Over Time",
                markers=True
            )
            charts.append(fig2)
        except:
            pass

    # Chart 3: Pie chart — if categorical exists
    if categorical_cols:
        main_cat = categorical_cols[0]
        cat_data = df.groupby(main_cat)[main_num].sum().reset_index()
        cat_data = cat_data.sort_values(main_num, ascending=False).head(8)
        fig3 = px.pie(
            cat_data,
            names=main_cat,
            values=main_num,
            title=f"🥧 {main_num} Share by {main_cat}"
        )
        charts.append(fig3)

    # Chart 4: Histogram — distribution of main numeric column
    fig4 = px.histogram(
        df,
        x=main_num,
        title=f"📉 Distribution of {main_num}",
        nbins=30
    )
    charts.append(fig4)

    return charts