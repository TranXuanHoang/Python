import streamlit as st
from pages.page_utilities import remove_streamlit_default_header


st.set_page_config(
    page_title="Todos Web App",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'http://localhost:8501/help',
        'Report a Bug': 'http://localhost:8501/bug'
    }
)

remove_streamlit_default_header()

with st.sidebar:
    dashboard_selectbox = st.selectbox(
        "Your Dashboards",
        ["Dashboard 1", "Dashboard 2", "Dashboard 3"]
    )

st.title(f"{dashboard_selectbox}")

# Display celebratory balloons and snowflakes
st.balloons()
st.snow()