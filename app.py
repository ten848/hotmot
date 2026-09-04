import streamlit as st
import pandas as pd

df = pd.read_csv("pokemon_data.csv")

theme = st.get_option("theme.base")
color = "black" if theme == "dark" else "white"

st.markdown(
    f"""
    <style>
        a.custom-link:link,
        a.custom-link:visited,
        a.custom-link:hover,
        a.custom-link:active {{
            color: {color} !important;
            text-decoration: none !important;
        }}
    </style>

    <p style="font-size:48px;">
        <a href="/" class="custom-link">
            unitexyz.com
        </a>
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<h2 style='text-align: right;'>about us</h2>", unsafe_allow_html=True)

col1,col2 = st.columns(2)
with col1:
	if st.button("点数記録"):
		st.write("ぬーん")
with col2:
	if st.button("勝敗記録"):
		st.write("うぱ")

selected_pokemon = st.selectbox("select",df["name"])
filtered_df = df[df["name"] == selected_pokemon]

st.write("### 詳細データ")
st.table(df[["name","type","role"]])