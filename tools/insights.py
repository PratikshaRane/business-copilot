
import os
from groq import Groq

def generate_insights(kpis, df):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    col_names = df.columns.tolist()
    kpi_text = "\n".join([f"- {k}: {v}" for k, v in kpis.items()])
    sample = df.head(5).to_string()

    prompt = f"""
You are a senior business analyst. Analyze this business data and provide insights.

DATASET COLUMNS:
{col_names}

KEY METRICS:
{kpi_text}

SAMPLE DATA:
{sample}

Please provide:
1. 📊 Top 3 trends you notice in this data
2. ⚠️ 2 anomalies or red flags worth investigating
3. 🌱 3 growth opportunities based on the data
4. 💡 What is the single most important insight?

Be specific, use the actual numbers from the metrics above.
Keep each point to 2-3 sentences max.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content