import streamlit as st
import requests

# --- הגדרות בסיסיות ---
AZURE_API_URL = "https://priority-chatbot-app-hxcgddgfbvgzczay.israelcentral-01.azurewebsites.net/ask"

st.set_page_config(page_title="Yaniv AI", layout="centered")

# --- עיצוב CSS ---
<style>
    .stChatMessage {
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        max-width: 85% !important;
    }
    
    /* הודעת משתמש - יישור לשמאל וצבע אפור בהיר */
    [data-testid="stChatMessageUser"] {
        background-color: #f1f5f9 !important;
        margin-right: auto !important;
        border-bottom-left-radius: 2px !important;
    }

    /* הודעת AI - יישור לימין וצבע כחול-לבן עם פס ירוק */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff !important;
        border-right: 4px solid #8cc63f !important;
        margin-left: auto !important;
        border-bottom-right-radius: 2px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
    }
    
    /* העלמת האייקונים הגנריים */
    [data-testid="stChatIconAssistant"], [data-testid="stChatIconUser"] {
        display: none;
    }
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


