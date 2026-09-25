import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(
    page_title="MegaQash Writers · Translation Task Platform",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header, footer, and sidebar elements completely for a native web experience
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none !important;
        width: 100% !important;
        height: 100vh !important;
    }
</style>
""", unsafe_allow_html=True)

def load_app():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: index.html file not found.</h3>"

html_content = load_app()
components.html(html_content, height=1000, scrolling=True)
