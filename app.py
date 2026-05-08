import streamlit as st
import pandas as pd
from tools.cleaner import clean_data
from tools.kpi import calculate_kpis
from tools.insights import generate_insights
from tools.summary import generate_summary
from tools.charts import generate_charts

st.set_page_config(
    page_title="Business Insights Copilot",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Business Insights Copilot")
st.markdown("Upload your sales or marketing data and let AI do the analysis.")

uploaded_file = st.file_uploader(
    "Upload your CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        raw = uploaded_file.read()
        for enc in ["utf-8", "latin-1", "cp1252", "iso-8859-1"]:
            try:
                import io
                df = pd.read_csv(io.BytesIO(raw), encoding=enc)
                break
            except:
                continue
    else:
        df = pd.read_excel(uploaded_file, encoding='utf-8', errors='replace')

    st.subheader("📋 Raw Data Preview")
    st.dataframe(df.head(10))

    st.divider()

    # Tool 1: Clean data
    st.subheader("🧹 Step 1: Data Cleaning")
    cleaned_df, cleaning_report = clean_data(df)
    for item in cleaning_report:
        st.write(item)

    st.subheader("✅ Cleaned Data Preview")
    st.dataframe(cleaned_df.head(10))

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", cleaned_df.shape[0])
    col2.metric("Total Columns", cleaned_df.shape[1])
    col3.metric("Missing Values", cleaned_df.isnull().sum().sum())

    st.divider()

    # Tool 2: KPI Dashboard
    st.subheader("📈 Step 2: KPI Dashboard")
    kpis = calculate_kpis(cleaned_df)

    if kpis:
        kpi_items = list(kpis.items())
        for i in range(0, len(kpi_items), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(kpi_items):
                    key, value = kpi_items[i + j]
                    col.metric(key, value)
    else:
        st.warning("⚠️ Could not detect standard columns.")
    
    st.divider()

    # Charts
    st.subheader("📊 Step 3: Visual Analytics")

    charts = generate_charts(cleaned_df)

    if charts:
        # Show first two charts side by side
        if len(charts) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(charts[0], use_container_width=True)
            with col2:
                st.plotly_chart(charts[1], use_container_width=True)

        # Show pie chart full width
        if len(charts) >= 3:
            st.plotly_chart(charts[2], use_container_width=True)
    else:
        st.warning("⚠️ Could not generate charts — check column names.")
    
    st.divider()
    # Tool 3: AI Insights
    st.subheader("🤖 Step 3: AI-Generated Insights")
    
    with st.spinner("AI is analyzing your data..."):
        insights = generate_insights(kpis, cleaned_df)
    
    st.markdown(insights)

    st.divider()

    # Tool 4: Executive Summary
    st.subheader("📝 Step 4: Executive Summary")

    with st.spinner("Generating executive summary..."):
        summary = generate_summary(kpis, insights)

    st.markdown(summary)
    # Download button
    st.download_button(
        label="📥 Download Summary as .txt",
        data=summary,
        file_name="executive_summary.txt",
        mime="text/plain"
    )