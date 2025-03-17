import streamlit as st
import requests

st.title("💼 Infosys AI HR Assistant")

query = st.text_input("Ask your HR question (e.g., 'What is the leave policy?')")

if st.button("Get Answer from HR FAQs"):
    response = requests.get(f"https://875b3a5e-0e96-4a0c-9fb5-f6b47d225401-00-3s2ykafqo0c9.pike.replit.dev/get_hr_policy/{query}")
    st.write(response.json()["answer"])
