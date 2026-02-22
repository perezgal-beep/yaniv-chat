import streamlit as st
import requests

# --- הגדרות בסיסיות ---
AZURE_API_URL = "https://priority-chatbot-app-hxcgddgfbvgzczay.israelcentral-01.azurewebsites.net/ask"

st.set_page_config(page_title="Yaniv AI", layout="centered")

# --- עיצוב CSS מתקדם להסרת הרקע השחור ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] { 
        font-family: 'Assistant', sans-serif; 
        direction: rtl; 
    }

    .stApp { background-color: #ffffff; }

    /* הקסם שמסיר את הרקע השחור מהלוגו */
    .logo-box {
        display: flex;
        justify-content: center;
        background-color: black; /* אנחנו שמים רקע שחור קטן כדי שהלוגו הלבן יבלוט */
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }

    .main-title { 
        color: #1e3a8a; 
        text-align: center; 
        font-weight: 700; 
        font-size: 2.2rem;
    }
    
    .stChatMessage { 
        background-color: #f1f5f9 !important; 
        border-radius: 15px !important; 
    }
    
    /* עיצוב כפתור ירוק */
    .stChatInput button { background-color: #8cc63f !important; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- תצוגת לוגו ---
# הצבת הלוגו בתוך תיבה כהה מעוצבת כדי שהלוגו הלבן יראה יוקרתי
st.markdown('<div class="logo-box">', unsafe_allow_html=True)
try:
    st.image("LOGOY.gif", width=250)
except:
    st.header("YANIV GROUP")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">במה אוכל לעזור היום?</h1>', unsafe_allow_html=True)

# --- לוגיקה של הצ'אט ---
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
                r = requests.post(AZURE_API_URL, json={"message": prompt}, timeout=30)
                res = r.json().get("response", "אין תשובה")
            except:
                res = "שגיאת חיבור לשרת."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})