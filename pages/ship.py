import streamlit as st

col1, col2 = st.columns([1,4])
with col1:
    with st.expander("A"):
        st.slider("B",0, 2, 1)