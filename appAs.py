import streamlit as st
import requests
import time
from streamlit_extras.add_vertical_space import add_vertical_space

# ✅ Set Streamlit Page Configuration
st.set_page_config(page_title="HR Assistant AI", page_icon="🤖", layout="centered")

# ✅ Custom CSS for Styling
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #2E86C1;
        }
        .stTextInput>div>div>input {
            font-size: 18px !important;
        }
        .stButton>button {
            background-color: #2E86C1 !important;
            color: white !important;
            font-size: 18px;
            border-radius: 10px;
            padding: 8px 16px;
        }
        .chat-container {
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ Title
st.markdown('<p class="title">💼 Infosys AI HR Assistant</p>', unsafe_allow_html=True)
add_vertical_space(2)

# ✅ Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# ✅ User Input
query = st.chat_input("🔍 Ask about Infosys HR policies...")
if query:
    # ✅ Save User Message
    st.session_state.messages.append({"role": "user", "text": query})

    # ✅ Display Bot Typing Animation
    with st.chat_message("assistant"):
        st.markdown("🤖 *Typing...*")
        time.sleep(2)

        # ✅ Get AI Response
        response = requests.get(f"https://hr-chatbot-fastapi.onrender.com/get_hr_policy/{query}").json()["answer"]

        # ✅ Show Response
        st.markdown(response)

    # ✅ Save Bot Response
    st.session_state.messages.append({"role": "assistant", "text": response})
