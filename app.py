import streamlit as st
import requests
import pandas as pd

# Page Configuration
st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("🔍 SHL Assessment Recommendation System")
st.write("Enter a Job Description or Query to find the best SHL assessments.")

# User Input
query = st.text_area("Job Description / Query:", placeholder="e.g. Need a Java developer who is good at collaborating...")

# --- IMPORTANT: Hugging Face API URL ---
# Localhost hata kar apna naya Hugging Face link yahan daala hai
API_URL = "https://vpatidar7697-shl-assessment-system.hf.space/recommend"

if st.button("Get Recommendations"):
    if query:
        with st.spinner('Finding best matches from SHL database...'):
            try:
                # API ko request bhejna
                response = requests.post(API_URL, json={"query": query})
                
                if response.status_code == 200:
                    data = response.json().get("recommended_assessments", [])
                    
                    if data:
                        # Results ko Table format mein dikhana
                        df = pd.DataFrame(data)
                        
                        # Columns ko user-friendly banana
                        df.columns = ["URL", "Assessment Name", "Description", "Test Type"]
                        
                        # Results display
                        st.success(f"Found {len(df)} matching assessments!")
                        st.table(df) # Tabular format
                    else:
                        st.warning("No assessments found matching your query.")
                else:
                    st.error(f"API Error: Status {response.status_code}. Make sure Hugging Face Space is 'Running'.")
            
            except Exception as e:
                st.error(f"Connection Error: Could not connect to the Hugging Face API.")
                st.info("Check if your Hugging Face Space is active and 'Running'.")
    else:
        st.info("Please enter a query first.")

