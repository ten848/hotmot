import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from streamlit_keypress import key_press_events
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
with st.sidebar:
    if "mode" not in st.session_state:
        st.session_state["mode"] = "ten"

    is_teru = (st.session_state["mode"] == "teru")

    checked = st.checkbox("私はteruです", value=is_teru, key="teru_checkbox")

    st.session_state["mode"] = "teru" if checked else "ten"
#endregion

#region lanes
if "selected_pokemon_A" not in st.session_state:
    st.session_state["selected_pokemon_A"] = {}

if "selected_pokemon_B" not in st.session_state:
    st.session_state["selected_pokemon_B"] = {}

if "waiting" not in st.session_state:
    st.session_state["waiting"] = [0] * 6

if "lanes_arrow" not in st.session_state:
    st.session_state["lanes_arrow"] = [None] * 6

if "lanes" not in st.session_state:
    st.session_state["lanes"] = [None] * 6


img_top = Image.open(f"images/UI/top_lane.png").convert("RGBA")
img_center = Image.open(f"images/UI/center_lane.png").convert("RGBA")
img_bottom = Image.open(f"images/UI/bottom_lane.png").convert("RGBA")

img_top = img_top.resize((50,50))
img_center = img_center.resize((50,50))
img_bottom = img_bottom.resize((50,50))

# st.markdown("""
#     <style>
#     [data-testid= "stToast"] {position: absolute; top: 0px; left: -500px; width: 150px; height: 100px; min-height: 0px; z-index: 10}
#     [data-testid= "stToast"] * {font-size: 10px}
#     </style>
#     """,
#     unsafe_allow_html= True)

# st.write("waiting:", st.session_state["waiting"][1:])
# st.write("lanes_arrow:", st.session_state["lanes_arrow"][1:])
#endregion

#region 入力欄
for x in range(1,6):
    col1, col2, col3, col4, col5= st.columns([1, 2, 2, 2, 1])
    with col2:
        st.session_state["selected_pokemon_A"][x] = st.selectbox(f"味方{x}",df["name"]).split("(")[0]

    with col1:
        if os.path.exists(f"images/pokemon/{st.session_state["selected_pokemon_A"][x]}.png"):
            img_copy = Image.open(f"images/pokemon/{st.session_state["selected_pokemon_A"][x]}.png").convert("RGBA").copy()
        
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
        st.markdown("""
        <style>
        div.stButton > button {position: absolute; top: -16px; left: -128px;
        width: 150px; height: 20px; min-height: 0px; margin-top: 0px}
        div.stButton > button * {font-size: 10px}
        </style>
        """,
        unsafe_allow_html= True)
        if st.session_state["lanes"] [x] == None:
            if st.button(f"レーン宣告", key=f"button1_{x}"):
                st.session_state["waiting"] = [0] * 6
                st.session_state["waiting"][x] = 1
                st.rerun()

        else:
            if st.session_state["lanes"] [x] == "中央":
                if st.button(f"中央エリアに行きます", key=f"button2_{x}"):
                    st.session_state["waiting"] = [0] * 6
                    st.session_state["waiting"][x] = 1
                    st.rerun()

            else:
                if st.button(f"{st.session_state["lanes"] [x]}レーンに行きます", key=f"button3_{x}"):
                    st.session_state["waiting"] = [0] * 6
                    st.session_state["waiting"][x] = 1
                    st.rerun()

    # with col4:
    #     if st.session_state["lanes"] [x] == "上" or st.session_state["lanes"] [x] == "下":
    #         st.markdown(f"""
    #             <div style ="ackground-color: #f0f2f6; border: 2px solid #4f46e5; 
    #             border-radius: 8px; padding: 15px; font-size: 14px">  <br>{st.session_state["lanes"] [x]} レーンに <br>行きます </div>
    #             """,
    #             unsafe_allow_html = True
    #         )


    with col4:
        st.session_state["selected_pokemon_B"][x] = st.selectbox(f"敵{x}",df["name"])

    with col5:
        img_path = f"images/pokemon/{st.session_state["selected_pokemon_B"][x]}.png"
        if os.path.exists(img_path):
            st.image(img_path, width=100)
        else:
            st.image("images/UI/橙icon_unite.jpg", width=100)
#endregion

#region Next
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    coords = streamlit_image_coordinates("images/UI/unite_start.png", key="img_click", width = 300)
    if coords is not None:
        st.switch_page("pages/map.py")
#endregion

events = key_press_events()

if 1 not in st.session_state["waiting"]:
    events = None

for y in range(1,6):
    if st.session_state["waiting"][y] == 1 and events:
        st.session_state["lanes_arrow"][y] = events
        if st.session_state["lanes_arrow"] [y] == "ArrowRight" or st.session_state["lanes_arrow"] [y] == "ArrowLeft":
            st.session_state["lanes"] [y] = "中央"
        if st.session_state["lanes_arrow"] [y] == "ArrowUp":
            st.session_state["lanes"] [y] = "上"
        if st.session_state["lanes_arrow"] [y] == "ArrowDown":
            st.session_state["lanes"] [y] = "下"
        
        # if st.session_state["lanes"][y] is not None:
        #     if st.session_state["lanes"] [y] == "中央":
        #         st.toast("中央エリアに行きます")

        #     else:
        #         st.toast(f"{st.session_state["lanes"][y]}ルートに行きます")
        
        st.session_state["waiting"][y] = 0
        st.rerun()

# st.write("lanes:", st.session_state["lanes"][1:])