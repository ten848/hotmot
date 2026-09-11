import streamlit as st
import pandas as pd
import sqlite3
from db import read_table

def main():
    top_page = st.Page(
        page="main.py",title="Top"
    )
    sub = st.Page(
        page="pages/sub.py",title="sub"
    )
    subsub = st.Page(
        page="pages/subsub.py",title="subsub"
    )

conn = sqlite3.connect("pokemon_datas.db")
df = read_table("pokemon")

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
        <a href="/" target="_self" class="custom-link">
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
	if st.button("pick"):
		st.switch_page("pages/2_sub.py")
with col2:
	if st.button("分析開始..."):
		st.switch_page("pages/image.py")

# import base64

# video_path = "images/UI/azlite.mp4"

# with open(video_path, "rb") as f:
#     video_bytes = f.read()

# encoded = base64.b64encode(video_bytes).decode()

# video_html = f"""
# <video width="25%" autoplay loop muted playsinline>
#     <source src="data:video/mp4;base64,{encoded}" type="video/mp4">
# </video>
# """

# st.markdown(video_html, unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,2,1])
with col2:
	st.image("images/UI/Oudou_RPG.png", width = 400)


selected_pokemon = st.selectbox("select",df["name"])
filtered_df = df[df["name"] == selected_pokemon]

st.write("### 詳細データ")
st.table(df[df["name"] != " "][["name", "type", "role", "パワースパイク", "とくしゅ"]])
