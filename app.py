import streamlit as st
import requests

AZURE_API_URL = "https://priority-chatbot-app-hxcgddgfbvgzczay.israelcentral-01.azurewebsites.net/ask"

st.set_page_config(page_title="Yaniv AI", layout="centered")

# עיצוב נקי ללא שגיאות
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .logo-container { display: flex; justify-content: center; background-color: #000; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .stChatMessage { border-radius: 15px !important; border: 1px solid #eee !important; margin-bottom: 10px; }
    [data-testid="stChatMessageAssistant"] { border-right: 5px solid #8cc63f !important; background-color: #fdfdfd !important; }
    .stChatInput button { background-color: #8cc63f !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("LOGOY.gif", width=250)
except:
    st.header("YANIV GROUP")
st.markdown('</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("שאל אותי על נתוני 2026..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("מעבד נתונים..."):
            try:
                r = requests.post(AZURE_API_URL, json={"message": prompt}, timeout=60)
                res = r.json().get("response", "אין תשובה.")
            except:
                res = "שגיאת חיבור לשרת."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
