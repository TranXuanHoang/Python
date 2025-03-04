import streamlit as st

from pages.page_utilities import remove_streamlit_default_header

st.set_page_config(
    page_title="Reports",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'http://localhost:8501/help',
        'Report a Bug': 'http://localhost:8501/bug'
    }
)

remove_streamlit_default_header()

st.title("Reports")

# Display celebratory balloons and snowflakes
st.balloons()
st.snow()