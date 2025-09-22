# AI-Research-Agent
An AI-powered agent that takes a user query, finds sources online, extracts content, summarizes it with an LLM, and saves the results into a database for later viewing.

## Architecture
  flowchart TD
    A[User enters query] --> B[Web Search API (SerpAPI)]
    B --> C[Extract content (Trafilatura / pypdf)]
    C --> D[Summarizer (HuggingFace T5-small)]
    D --> E[Store report in SQLite DB]
    E --> F[Streamlit Web UI: history + saved reports]
  -User inputs a query (e.g., “Latest research on AI in education”).
  -Web search is done using SerpAPI (Google engine).
  -Content extraction is done using Trafilatura (for web pages).
  -Summarization is done using a HuggingFace model (t5-small).
  -Results saved in SQLite (query, summary, sources, timestamp).
  -Streamlit UI shows new + past reports.

## Setup & Run Instructions
1. Clone Repo
   git clone https://github.com/AdhyasGowda/ai-research-agent.git
   cd ai-research-agent

2. Set Your API Key
   SERPAPI_KEY = "your_serpapi_key_here"

3. Run App
streamlit run app.py

## Example Queries & Reports
1. Example 1:
Query: Latest research on AI in education
Summary:AI is a rapidly growing technology … AI+Education Summit hosted four experts …
-Sources:
-NEA – AI in Education
-ED Report PDF
-Stanford Accelerate Learning

3. Example 2:
Query: Impact of Mediterranean diet on heart health
Summary:Research consistently shows that the Mediterranean diet reduces cardiovascular risks by …
Sources:
-Harvard Health – Mediterranean Diet
-NIH – Diet & Heart Health
-AHA Journal

## Demo
https://drive.google.com/file/d/1-3jjoibOy1lqeP7QoZXdFsA86zh-KdNU/view?usp=sharing
