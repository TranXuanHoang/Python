import streamlit as st


def remove_streamlit_default_header():
    # Apply custom CSS to hide Streamlit elements
    st.markdown("""
        <style>
            /* Hide the deploy button */
            /* Hide the menu icon (three dots) */
            .stAppToolbar {
                visibility: hidden;
                width: 0px;
                height: 0px;
            }
            
            /* Hide the header */
            .stAppHeader {
                visibility: hidden;
                height: 0px;
            }
            
            /* Adjust Top Header spacing */
            .stMainBlockContainer {
                padding: 0.5rem 2rem;
            }
        </style>
    """, unsafe_allow_html=True)