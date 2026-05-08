import os
from groq import Groq

def generate_summary(kpis, insights):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    kpi_text = "\n".join([f"- {k}: {v}" for k, v in kpis.items()])

    prompt = f"""
You are a McKinsey consultant writing a board-level executive summary.

KEY METRICS:
{kpi_text}

ANALYST INSIGHTS:
{insights}

Write a professional executive summary with these exact sections:

## 📋 Executive Summary
2-3 sentences summarizing the overall business performance.

## ✅ What's Working
3 bullet points of positives backed by data.

## 🚨 Risk Areas
2 bullet points of concerns that need immediate attention.

## 🎯 Recommended Actions
3 specific, actionable recommendations with expected impact.

## 🏁 Conclusion
1 strong closing sentence about the business outlook.

Use professional business language. Be concise and specific.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content