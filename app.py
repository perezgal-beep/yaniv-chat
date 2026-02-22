import streamlit as st
import requests

# --- הגדרות בסיסיות ---
AZURE_API_URL = "https://priority-chatbot-app-hxcgddgfbvgzczay.israelcentral-01.azurewebsites.net/ask"

st.set_page_config(page_title="Yaniv AI", layout="centered")

# --- עיצוב CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; }
    .stApp { background-color: #ffffff; }
    .logo-box {
        display: flex;
        justify-content: center;
        background-color: #000000;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .main-title { color: #1e3a8a; text-align: center; font-weight: 700; font-size: 2.2rem; }
    .stChatMessage { background-color: #f1f5f9 !important; border-radius: 15px !important; }
    .stChatInput button { background-color: #8cc63f !important; }
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- תצוגת לוגו ---
st.markdown('<div class="logo-box">', unsafe_allow_html=True)
try:
    st.image("LOGOY.gif", width=250)
except:
    st.header("YANIV GROUP")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">במה אוכל לעזור היום?</h1>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("שאל אותי משהו..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("בודק בפריוריטי..."):
            try:
                # הגדלנו את ה-timeout ל-60 שניות כי פריוריטי לפעמים איטית
                r = requests.post(AZURE_API_URL, json={"message": prompt}, timeout=60)
                if r.status_code == 200:
                    res = r.json().get("response", "התקבלה תשובה ריקה מהשרת.")
                else:
                    res = f"שגיאה מהשרת ב-Azure (קוד: {r.status_code})"
            except Exception as e:
                res = f"שגיאת חיבור לשרת: {str(e)}"
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
