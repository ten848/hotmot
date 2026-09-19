import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from db import read_table
import os
df = read_table("pokemon")

#region unitexyz
# theme = st.get_option("theme.base")
# color = "black" if theme == "dark" else "white"
# st.markdown(
#     f"""
#     <style>
#         a.custom-link:link,
#         a.custom-link:visited,
#         a.custom-link:hover,
#         a.custom-link:active {{
#             color: {color} !important;
#             text-decoration: none !important;
#         }}
#     </style>

#     <p style="font-size:48px;">
#         <a href="/" target="_self" class="custom-link">
#             unitexyz.com
#         </a>
#     </p>
#     """,
#     unsafe_allow_html=True
# )
#endregion

#region teru
with st.sidebar:
    if "mode" not in st.session_state:
        st.session_state["mode"] = "ten"

    is_teru = (st.session_state["mode"] == "teru")

    checked = st.checkbox("私はteruです", value=is_teru, key="teru_checkbox")

    st.session_state["mode"] = "teru" if checked else "ten"
#endregion

#region lanes
selected_pokemon_A = {}
selected_pokemon_B = {}

if "select" not in st.session_state:
    st.session_state["select"] = [1] * 6

if "lanes" not in st.session_state:
    st.session_state["lanes"] = [None] * 6

img_top = Image.open(f"images/UI/top_lane.png").convert("RGBA")
img_center = Image.open(f"images/UI/center_lane.png").convert("RGBA")
img_bottom = Image.open(f"images/UI/bottom_lane.png").convert("RGBA")

img_top = img_top.resize((50,50))
img_center = img_center.resize((50,50))
img_bottom = img_bottom.resize((50,50))
#endregion

#region 入力欄
for x in range(1,6):
    col1, col2, col3, col4, col5,col6= st.columns([1, 2, 1.5, 0.5, 2, 1])
    with col2:
        selected_pokemon_A[x] = st.selectbox(f"味方{x}",df["name"])

    with col1:
        if os.path.exists(f"images/pokemon/{selected_pokemon_A[x].split("(")[0]}.png"):
            img_copy = Image.open(f"images/pokemon/{selected_pokemon_A[x].split("(")[0]}.png").convert("RGBA").copy()
        
        else:
            img_copy = Image.open("images/UI/紫icon_unite.jpg").convert("RGBA").copy()

        img_copy = img_copy.resize((100,100))

        if st.session_state["lanes"][x]:
            if st.session_state["lanes"] [x] == "上":
                img_copy.paste(img_top, (-10,-15), img_top)

            if st.session_state["lanes"] [x] == "中央":
                img_copy.paste(img_center, (-10,-15), img_center)

            if st.session_state["lanes"] [x] == "下":
                img_copy.paste(img_bottom, (-10,-15), img_bottom)

        st.image(img_copy)

    with col3:
        st.markdown(
            f"""
            <style>
            .st-key-select{x} {{transform: translate(-120px, -30px); margin-top: 0px; padding: 10px; border-radius: 8px; width: 200px}}
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.session_state["select"][x] = st.select_slider("",options = ["上", "中央", "下"], value = "中央", key=f"select{x}", label_visibility = "collapsed")

    with col5:
        selected_pokemon_B[x] = st.selectbox(f"敵{x}",df["name"])

    with col6:
        img_path = f"images/pokemon/{selected_pokemon_B[x].split("(")[0]}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=100)
        else:
            st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region Next
col1, col2, col3 = st.columns([1, 1.6, 1])
with col2:
    coords = streamlit_image_coordinates("images/UI/unite_start.png", key="img_click", width = 300)
    if coords is not None:
        st.switch_page("pages/map.py")
#endregion

st.markdown("""
    <style>
    div.stButton > button {position: absolute; top: -110px; left: 32px;
    width: 128px; height: 40px; min-height: 0px; margin-top: 0px}
    div.stButton > button * {font-size: 10px}
    div.stButton > button:hover,
    div.stButton > button:focus {opacity: 1 !important; background: #0E1117  !important;}
    </style>
    """,
    unsafe_allow_html= True)

if st.button("レーン宣告"):
    for i in range(1,6):
        if st.session_state["select"] [i] == "上":
            st.session_state["lanes"][i] = "上"

        if st.session_state["select"] [i] == "中央":
            st.session_state["lanes"][i] = "中央"
            
        if st.session_state["select"] [i] == "下":
            st.session_state["lanes"][i] = "下"
    st.rerun()

