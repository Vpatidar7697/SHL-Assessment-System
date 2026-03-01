import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("🔍 SHL Assessment Recommendation System")
st.write("Enter a Job Description or Query to find the best SHL assessments.")

# User Input
query = st.text_area("Job Description / Query:", placeholder="e.g. Need a Java developer who is good at collaborating...")

if st.button("Get Recommendations"):
    if query:
        # Aapke FastAPI server ko request bhejna
        with st.spinner('Finding best matches...'):
            try:
                response = requests.post("http://127.0.0.1:8000/recommend", json={"query": query})
                
                if response.status_code == 200:
                    data = response.json().get("recommended_assessments", [])
                    
                    if data:
                        # Dataframe banakar table dikhana [cite: 45]
                        df = pd.DataFrame(data)
                        # Column names sundar banana
                        df.columns = ["URL", "Assessment Name", "Description", "Test Type"]
                        st.table(df) # Tabular format [cite: 45]
                    else:
                        st.warning("No assessments found matching your query.")
                else:
                    st.error(f"Error: API returned status {response.status_code}")
            except Exception as e:
                st.error(f"Could not connect to the backend server. Make sure main.py is running.")
    else:
        st.info("Please enter a query first.")