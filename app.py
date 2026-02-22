import streamlit as st
import requests

AZURE_API_URL = "https://priority-chatbot-app-hxcgddgfbvgzczay.israelcentral-01.azurewebsites.net/ask"

st.set_page_config(page_title="Yaniv AI | Engineering Intelligence", layout="centered")

# עיצוב CSS מתקדם
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Assistant', sans-serif; direction: rtl; text-align: right; }
    
    .logo-container {
        display: flex; justify-content: center; background-color: #000000;
        padding: 20px; border-radius: 15px; margin-bottom: 25px;
    }
    
    .stChatMessage { border-radius: 15px !important; margin-bottom: 10px; }
    
    /* בועת המשתמש */
    [data-testid="stChatMessageUser"] {
        background-color: #f8fafc !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* בועת ה-AI */
    [data-testid="stChatMessageAssistant"] {
        background-color: #ffffff !important;
        border-right: 5px solid #8cc63f !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
    }

    .stChatInput button { background-color: #8cc63f !important; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# הצגת לוגו
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
try:
    st.image("LOGOY.gif", width=250)
except:
    st.write("### YANIV GROUP")
st.markdown('</div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("שאל אותי על פרויקטים או הזמנות..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("מעבד נתונים מהפריוריטי..."):
            try:
                r = requests.post(AZURE_API_URL, json={"message": prompt}, timeout=60)
                res = r.json().get("response", "לא התקבלה תשובה.")
            except:
                res = "שגיאת חיבור לשרת. אנא נסה שוב בעוד רגע."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
