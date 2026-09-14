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

@st.cache_data
def create_pokemon_icon(pokemon_name, lane):
    clean_name = pokemon_name.split("(")[0]
    base_path = f"images/pokemon/{clean_name}.png"
    
    # ベース画像の読み込み
    if os.path.exists(base_path):
        img = Image.open(base_path).convert("RGBA")
    else:
        img = Image.open("images/UI/紫icon_unite.jpg").convert("RGBA")
        
    img = img.resize((100, 100))
    
    # レーンアイコンの合成
    if lane == "上":
        img.paste(img_top, (-10, -15), img_top)
    elif lane == "中央":
        img.paste(img_center, (-10, -15), img_center)
    elif lane == "下":
        img.paste(img_bottom, (-10, -15), img_bottom)
        
    return img

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
    col1, col2, col3, col4, col5,col6= st.columns([1, 2, 1.5, 0.5, 2, 1])
    with col2:
        selected_pokemon_A[x] = st.selectbox(f"味方{x}",df["name"])

    with col1:
        final_img = create_pokemon_icon(selected_pokemon_A[x], st.session_state["lanes"][x])
        st.image(final_img)


    with col3:
        st.markdown("""
        <style>
        div.stButton > button {position: absolute; top: -28px; left: 0px;
        width: 118px; height: 20px; min-height: 0px; margin-top: 0px}
        div.stButton > button * {font-size: 10px}
        div.stButton > button:hover,
        div.stButton > button:focus {opacity: 1 !important; background: #0E1117  !important;}
        
        </style>
        """,
        unsafe_allow_html= True)

        st.session_state["select"][x] = st.select_slider("",options=["上", "中央", "下"], key=f"select{x}", label_visibility="collapsed")

        if st.button("レーン宣告", key = f"button1_{x}"):
            if st.session_state["select"] [x] == "上":
                st.session_state["lanes"][x] = "上"
            if st.session_state["select"] [x] == "中央":
                st.session_state["lanes"][x] = "中央"
            if st.session_state["select"] [x] == "下":
                st.session_state["lanes"][x] = "下"
            st.rerun()

        # if st.session_state["lanes"] [x] == "中央":
        #     if st.button(f"中央エリアに行きます", key=f"button2_{x}"):
        #         st.session_state["waiting"] = [0] * 6
        #         st.session_state["waiting"][x] = 1
        #         st.rerun()

        #     else:
        #         if st.button(f"{st.session_state["lanes"] [x]}レーンに行きます", key=f"button3_{x}"):
        #             st.session_state["waiting"] = [0] * 6
        #             st.session_state["waiting"][x] = 1
        #             st.rerun()

    # with col4:
    #     if st.session_state["lanes"] [x] == "上" or st.session_state["lanes"] [x] == "下":
    #         st.markdown(f"""
    #             <div style ="ackground-color: #f0f2f6; border: 2px solid #4f46e5; 
    #             border-radius: 8px; padding: 15px; font-size: 14px">  <br>{st.session_state["lanes"] [x]} レーンに <br>行きます </div>
    #             """,
    #             unsafe_allow_html = True
    #         )


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



