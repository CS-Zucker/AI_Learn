import streamlit as st
from ui.sidebar import render_sidebar
from ui.chat_area import render_chat_area
from utils.session_manager import generate_session_time


st.set_page_config(
    page_title="AI技术文档助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

st.title("AI技术文档助手")
st.logo(r"resource\img\ai_logo2.jpeg")


if 'messages' not in st.session_state:
    st.session_state.messages = []
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_time()
if 'model' not in st.session_state:
    st.session_state.model = "deepseek-chat"
if 'max_tokens' not in st.session_state:
    st.session_state.max_tokens = 4096
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7
if 'domin' not in st.session_state:
    st.session_state.domin = "软件开发"
if 'deep_thinking' not in st.session_state:
    st.session_state.deep_thinking = True


render_chat_area()
render_sidebar()