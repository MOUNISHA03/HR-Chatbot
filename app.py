import streamlit as st
import requests

st.set_page_config(page_title="Infosys AI HR Assistant", page_icon="💼")

st.title("💼 Infosys AI HR Assistant")

# User input for chatbot
query = st.text_input("Ask your HR question (e.g., 'What is the leave policy?')")

# Fetch HR policy answer
if st.button("Get Answer"):
    if query.strip():
        response = requests.get(f"http://127.0.0.1:8000/get_policy/{query}")
        answer = response.json()["answer"]
        st.write(f"**💡 Answer:** {answer}")
    else:
        st.warning("⚠️ Please enter a valid question.")

# Fetch AI-generated answer using GPT-4
if st.button("Get AI Answer"):
    if query.strip():
        response = requests.get(f"http://127.0.0.1:8000/gpt_policy/{query}")
        answer = response.json()["answer"]
        st.write(f"**🤖 AI-Powered Answer:** {answer}")
    else:
        st.warning("⚠️ Please enter a valid question.")

# IT Support Button
if st.button("IT Support"):
    st.write("For IT asset requests, visit the Infosys IT portal.")
