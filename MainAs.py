from fastapi import FastAPI
import pandas as pd
import openai
import os
import numpy as np
import faiss

app = FastAPI()

# ✅ Step 1: Load HR FAQs dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "hr_faqs.csv")
df = pd.read_csv(file_path)

# ✅ Step 2: Set OpenAI API Key
openai.api_key = "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"

# ✅ Step 3: Generate embeddings for HR questions
def generate_embeddings(text_list):
    response = openai.Embedding.create(input=text_list, model="text-embedding-ada-002")
    return [embedding["embedding"] for embedding in response["data"]]

df["embedding"] = generate_embeddings(df["question"].tolist())

# ✅ Step 4: Convert embeddings to NumPy array
embedding_array = np.array(df["embedding"].tolist()).astype('float32')

# ✅ Step 5: Create FAISS index for similarity search
index = faiss.IndexFlatL2(embedding_array.shape[1])
index.add(embedding_array)

@app.get("/get_hr_policy/{query}")
def get_hr_policy(query: str):
    """
    Searches for an HR policy using semantic embeddings.
    If no relevant answer is found, calls GPT-4.
    """
    query_embedding = generate_embeddings([query])[0]
    query_embedding = np.array(query_embedding).reshape(1, -1).astype('float32')

    # ✅ Step 6: Find the most similar question using FAISS
    _, index_results = index.search(query_embedding, 1)
    best_match = df.iloc[index_results[0][0]]

    if best_match is not None:
        return {"answer": best_match["answer"]}

    # ✅ Step 7: If no answer is found, call GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI HR Assistant. Answer HR-related queries professionally."},
            {"role": "user", "content": query}
        ]
    )
    return {"answer": response["choices"][0]["message"]["content"]}
