import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. CSV file load karein [cite: 55]
df = pd.read_csv("shl_tests_data.csv")

# 2. Text data taiyar karein
# Hum Name aur Description dono ko milakar ek 'searchable text' banayenge
df['text_for_embedding'] = df['Name'] + " " + df['Description']

# 3. Embedding Model select karein (HuggingFace free hai)
# [cite: 96]
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 4. Vector Database (ChromaDB) mein data save karein
# [cite: 92]
vector_db = Chroma.from_texts(
    texts=df['text_for_embedding'].tolist(),
    metadatas=[{"url": u, "name": n} for u, n in zip(df['URL'], df['Name'])],
    embedding=embeddings,
    persist_directory="./shl_vector_db" # Ye folder aapke PC par ban jayega
)

print("Vector Database taiyar hai aur './shl_vector_db' mein save ho gaya hai!")