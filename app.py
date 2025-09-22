import streamlit as st
import sqlite3
import requests
import trafilatura
from transformers import pipeline
import pandas as pd


conn = sqlite3.connect("reports.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS reports")
c.execute("""
CREATE TABLE reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    summary TEXT,
    sources TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Add missing columns safely
for col in ["summary", "sources"]:
    try:
        c.execute(f"ALTER TABLE reports ADD COLUMN {col} TEXT")
    except sqlite3.OperationalError:
        pass


conn.commit()

# Summarizer (local LLM)
summarizer = pipeline("summarization", model="t5-small")  # free model

# Helper: Web search using SerpAPI
def search_sources(query, api_key, num_results=3):
    url = "https://serpapi.com/search.json"
    params = {"q": query, "engine": "google", "num": num_results, "api_key": api_key}
    res = requests.get(url, params=params).json()
    sources = []
    for r in res.get("organic_results", [])[:num_results]:
        link = r.get("link")
        if link:
            sources.append(link)
    return sources

# Helper: Extract content
def extract_text(url):
    downloaded = trafilatura.fetch_url(url)
    if downloaded:
        text = trafilatura.extract(downloaded)
        return text
    return ""

# Generate report
def generate_report(query, api_key):
    sources = search_sources(query, api_key)
    combined_text = ""
    for url in sources:
        content = extract_text(url)
        if content:
            combined_text += content[:2000] + " "  # limit to 2000 chars for summarizer
    if combined_text:
        summary = summarizer(combined_text, max_length=200, min_length=50, do_sample=False)[0]['summary_text']
    else:
        summary = "No content could be extracted from sources."
    return summary, sources

# Streamlit UI
st.title("AI Research Agent")
query = st.text_input("Enter your query:")

SERPAPI_KEY = ""  # replace with your key

if st.button("Generate Report"):
    if query:
        summary, sources = generate_report(query, SERPAPI_KEY)
        st.subheader("Summary:")
        st.write(summary)
        st.subheader("Sources:")
        for s in sources:
            st.write(s)
        # Save to DB
        c.execute("INSERT INTO reports (query, summary, sources) VALUES (?,?,?)",
                  (query, summary, ", ".join(sources)))
        conn.commit()
        st.success("Report saved successfully!")

# Show previous reports
st.subheader("Previous Reports")
df = pd.read_sql_query("SELECT query, summary, sources, created_at FROM reports ORDER BY created_at DESC", conn)
for idx, row in df.iterrows():
    st.markdown(f"**Query:** {row['query']}")
    st.text(row['summary'])
    st.markdown(f"**Sources:** {row['sources']}")
    st.caption(f"Created at: {row['created_at']}")
    st.markdown("---")
