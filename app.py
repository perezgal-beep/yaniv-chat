import streamlit as st
import requests

AZURE_API_URL = "https://priority-chatbot-app-hxcgddgfbvgzczay.israelcentral-01.azurewebsites.net/ask"

st.set_page_config(page_title="Yaniv AI", layout="centered")

# עיצוב CSS מתוקן (בתוך מחרוזת טקסט כדי למנוע SyntaxError)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #ffffff; }
    
    /* לוגו בקופסה שחורה */
    .logo-container {
        display: flex; justify-content: center; background-color: #000000;
        padding: 20px; border-radius: 15px; margin-bottom: 20px;
    }
    
    /* בועות צ'אט מעוצבות */
    .stChatMessage { border-radius: 20px !important; border: 1px solid #eee !important; }
    [data-testid="stChatMessageAssistant"] { border-right: 5px solid #8cc63f !important; background-color: #fafafa !important; }
    
    .stChatInput button { background-color: #8cc63f !important; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# תצוגת לוגו
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("LOGOY.gif", width=250)
except:
    st.header("YANIV GROUP")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<h2 style="text-align:center; color:#1e3a8a;">במה אוכל לעזור היום?</h2>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("שאל על הזמנות, פרויקטים או סכומים..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("מתחבר לפריוריטי..."):
            try:
                r = requests.post(AZURE_API_URL, json={"message": prompt}, timeout=60)
                res = r.json().get("response", "אין תשובה מהשרת.")
            except:
                res = "שגיאת חיבור לשרת. וודא שה-Azure פועל."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
