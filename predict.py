import pandas as pd
import requests

# 1. API URL (Ensure main.py is running)
API_URL = "http://127.0.0.1:8000/recommend"

# 2. Test-Set.csv se li gayi 9 queries
test_queries = [
    "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes.",
    "AI enthusiast Research Engineer for AI/ML models (NLP, computer vision, LLM) time limit less than 30 minutes.",
    "I am hiring for an analyst and wants applications to screen using Cognitive and personality tests, what options are available within 45 mins.",
    "Presales Specialist for custom client demos, RFPs, and high quality Statements of Work, test at least 30 mins long.",
    "I am new looking for new graduates in my sales team, suggest an 30 min long assessment.",
    "Marketing - Content Writer Position at ShopClues, Gurugram. Experience in SEO and unique Product Description.",
    "I want to hire a product manager with 3-4 years of work experience and expertise in SDLC, Jira and Confluence.",
    "Finance & Operations Analyst for insights, budgeting, and financial reporting. 1-2 years experience.",
    "Customer support executives for Product operations team in Mumbai. Fluent in English, 2-3 years experience."
]

all_results = []

for q in test_queries:
    print(f"Processing query...")
    # API ko POST request bhej rahe hain [cite: 164, 166]
    response = requests.post(API_URL, json={"query": q})
    
    if response.status_code == 200:
        data = response.json().get("recommended_assessments", [])
        # Har query ke liye URLs ko list mein daalna [cite: 174, 183]
        for item in data:
            all_results.append({
                "Query": q,
                "Assessment_url": item["url"]
            })

# 3. CSV mein save karna (Appendix 3 format) [cite: 208, 211, 213]
df = pd.DataFrame(all_results)
df.to_csv("submission_predictions.csv", index=False)
print("SUCCESS: submission_predictions.csv taiyar hai!")