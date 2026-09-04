import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
from db import read_table
import os
df = read_table("pokemon")

theme = st.get_option("theme.base")
color = "black" if theme == "dark" else "white"

#region unitexyz
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
#endregion

#region teru
col1, col2 = st.columns(2)
with col1:
    pass
with col2:
    if "mode" not in st.session_state:
        st.session_state["mode"] = "ten"

    # チェックボックスの状態を session_state["mode"] から構築
    is_teru = (st.session_state["mode"] == "teru")

    # 状態変化を受け取る
    checked = st.checkbox("私はteruです", value=is_teru, key="teru_checkbox")

    # 状態の同期
    st.session_state["mode"] = "teru" if checked else "ten"
#endregion

#region 1行目
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
with col2:
    selected_pokemon11 = st.selectbox("味方1",df["name"])
    filtered_df = df[df["name"] == selected_pokemon11]

with col1:
    img_path = f"images/pokemon/{selected_pokemon11}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/紫icon_unite.jpg", width=100)

with col4:
    selected_pokemon12 = st.selectbox("敵1",df["name"])
    filtered_df = df[df["name"] == selected_pokemon12]

with col5:
    img_path = f"images/pokemon/{selected_pokemon12}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region 2行目
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
with col2:
    selected_pokemon21 = st.selectbox("味方2",df["name"])
    filtered_df = df[df["name"] == selected_pokemon21]

with col1:
    img_path = f"images/pokemon/{selected_pokemon21}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/紫icon_unite.jpg", width=100)

with col4:
    selected_pokemon22 = st.selectbox("敵2",df["name"])
    filtered_df = df[df["name"] == selected_pokemon22]

with col5:
    img_path = f"images/pokemon/{selected_pokemon22}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region 3行目
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
with col2:
    selected_pokemon31 = st.selectbox("味方3",df["name"])
    filtered_df = df[df["name"] == selected_pokemon31]

with col1:
    img_path = f"images/pokemon/{selected_pokemon31}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/紫icon_unite.jpg", width=100)

with col4:
    selected_pokemon32 = st.selectbox("敵3",df["name"])
    filtered_df = df[df["name"] == selected_pokemon32]

with col5:
    img_path = f"images/pokemon/{selected_pokemon32}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region 4行目
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
with col2:
    selected_pokemon41 = st.selectbox("味方4",df["name"])
    filtered_df = df[df["name"] == selected_pokemon41]

with col1:
    img_path = f"images/pokemon/{selected_pokemon41}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/紫icon_unite.jpg", width=100)

with col4:
    selected_pokemon42 = st.selectbox("敵4",df["name"])
    filtered_df = df[df["name"] == selected_pokemon42]

with col5:
    img_path = f"images/pokemon/{selected_pokemon42}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region 5行目
col1, col2, col3, col4, col5 = st.columns([1, 2, 1, 2, 1])
with col2:
    selected_pokemon51 = st.selectbox("味方5",df["name"])
    filtered_df = df[df["name"] == selected_pokemon51]

with col1:
    img_path = f"images/pokemon/{selected_pokemon51}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/紫icon_unite.jpg", width=100)

with col4:
    selected_pokemon52 = st.selectbox("敵5",df["name"])
    filtered_df = df[df["name"] == selected_pokemon52]

with col5:
    img_path = f"images/pokemon/{selected_pokemon52}.png"
    if os.path.exists(img_path):
        st.image(img_path, width=100)
    else:
        st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region Next
col1, col2, col3 = st.columns([1,1.5,1])
with col2:
    coords = streamlit_image_coordinates("images/UI/unite_start.png", key="img_click" , width = 300)
    if coords is not None:
        st.switch_page("pages/map.py")
#endregion