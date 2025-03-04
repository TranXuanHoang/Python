import streamlit as st


pages = st.navigation({
    "Apps" : [
        st.Page("./pages/todos.py", title="Todos", icon="📝"),
        st.Page("./pages/reports.py", title="Reports", icon="📊"),
    ],
    "Account" : [
        st.Page("./pages/auth.py", title="Sign-Up/Sign-In", icon="🔒"),
    ]
})

pages.run()