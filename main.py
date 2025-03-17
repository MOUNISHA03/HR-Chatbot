from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI()

# Get absolute path of the file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, "hr_faqs.csv")

# Load HR FAQs dataset
try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    df = None  # Prevents app crash if file is missing

@app.get("/")
def read_root():
    return {"message": "FastAPI HR Chatbot is running!"}

@app.get("/get_hr_policy/{query}")
def get_hr_policy(query: str):
    """
    Searches for an HR policy in the dataset based on the user's query.
    Returns the answer if found, otherwise prompts to contact HR.
    """
    if df is None:
        return {"answer": "HR FAQ database is currently unavailable. Please try again later."}

    result = df[df['question'].str.contains(query, case=False, na=False)]

    if not result.empty:
        return {"answer": result.iloc[0]['answer']}

    return {"answer": "Sorry, I don’t have an answer for that. Please contact HR."}

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
