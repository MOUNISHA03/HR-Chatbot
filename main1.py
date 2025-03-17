from fastapi import FastAPI
import pandas as pd
import openai

app = FastAPI()

# Load HR Policies from CSV
df = pd.read_csv("hr_faqs.csv")

# Set OpenAI API Key
openai.api_key = "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"

@app.get("/get_policy/{query}")
def get_hr_policy(query: str):
    """
    Searches HR policy database for an answer.
    If no match is found, uses GPT-4 for AI-generated responses.
    """
    result = df[df['question'].str.contains(query, case=False, na=False)]

    if not result.empty:
        return {"answer": result.iloc[0]['answer']}

    # If no policy answer is found, call GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an Infosys HR Assistant. Answer HR-related questions professionally."},
            {"role": "user", "content": query}
        ]
    )
    return {"answer": response["choices"][0]["message"]["content"]}

# Run the server using:
# uvicorn backend:app --reload
