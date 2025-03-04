import streamlit as st


st.set_page_config(
    page_title="Account",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="auto",
)

# Auth Action Possible Values
# 'Sign-Up' - User is signing up
# 'Sign-In' - User is signing in
# 'Sign-Out' - User is signing out
auth_action = st.radio("Sign-Up or Sign-In", ["Sign-Up", "Sign-In"])

# Auth Status Possible Values
# 'Not-Determined' - Initial state
# 'Sign-Up' - User is signing up
# 'Signed-Up' - User has just signed up
# 'Sign-In' - User is signing in
# 'Signed-In' - User has just signed in
# 'Sign-Out' - User is signing out
# 'Signed-Out' - User has just signed out
auth_status = 'Sign-Up'

if auth_action == 'Sign-Up':
    st.title("Sign-Up")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    auth_status = 'Sign-Up'
    if st.button("Sign-Up"):
        st.write("Signing-Up...")
        # Add sign-up logic here
        st.write("Sign-Up successful!")
        auth_status = 'Signed-Up'

elif auth_action == 'Sign-In':
    st.title("Sign-In")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    auth_status = 'Sign-In'
    if st.button("Sign-In"):
        st.write("Signing-In...")
        # Add sign-in logic here
        st.write("Sign-In successful!")
        auth_status = 'Signed-In'


st.write(f"Auth Status: {auth_status}")