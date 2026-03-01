Project Title: SHL Assessment Recommendation System.


Tech Stack: Python, FastAPI, ChromaDB (Vector Search), aur Streamlit.



Core Logic:  RAG (Retrieval-Augmented Generation) 

How to Run:

pip install -r requirements.txt

python scraper.py

python vector_db.py

uvicorn main:app --reload

streamlit run app.py
