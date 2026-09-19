import streamlit as st
import urllib.parse
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from db import read_table
from supabase import create_client
import os

df = read_table("pokemon")

#region teru
with st.sidebar:
    if "mode" not in st.session_state:
        st.session_state["mode"] = "ten"

    is_teru = (st.session_state["mode"] == "teru")

    checked = st.checkbox("私はteruです", value=is_teru, key="teru_checkbox")

    st.session_state["mode"] = "teru" if checked else "ten"
#endregion

#region lanes
if "pokemon" not in st.session_state:
    st.session_state["pokemon"] = [None] * 11

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

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

container1 = st.container(key="container1")
with container1:
    if st.button("リセット"):
        supabase.table("record").delete().not_.is_("pokemon", "null").execute()
        st.session_state["pokemon"] = [None] * 11
        for y in range(11):
            key_name = f"select_A{y}"
            if key_name in st.session_state:
                del st.session_state[key_name]
            key_name = f"select_B{y}"
            if key_name in st.session_state:
                del st.session_state[key_name]

st.markdown("""
    <style>
    .st-key-container1 div.stButton > button {position: absolute; top: 519px; left: 535px;
    width: 169px; height: 64px; min-height: 0px; margin-top: 0px}
    .st-key-container1 div.stButton > button * {font-size: 16px}
    .st-key-container1 div.stButton > button:hover,
    .st-key-container1 div.stButton > button:focus {opacity: 1 !important; background: #0E1117  !important;}
    </style>
    """,
    unsafe_allow_html= True)


def add_record(pokemon, player_num):
    data = {"pokemon": pokemon, "player_num":player_num}
    res = supabase.table("record").upsert(data, on_conflict="player_num").execute()
    return res.data

def load_player_num():
    res = supabase.table("record").select("*").not_.is_("pokemon", "null").execute()
    return res.data

url_dt = load_player_num()
for row in url_dt:
    player_num = row.get("player_num")
    player_num = int(player_num)
    st.session_state["pokemon"][player_num] = row.get("pokemon")

#region 入力欄
for x in range(1,6):
    col1, col2, col3, col4, col5, col6= st.columns([1, 2, 1.5, 0.5, 2, 1])
    with col2:
        try:
            default_index = list(df["name"]).index(st.session_state["pokemon"][x])
        except (ValueError, TypeError):
            default_index = 0
        st.session_state["pokemon"][x] = st.selectbox(f"味方{x}",df["name"],
            key = f"select_A{x}", index=default_index
        )

        player_num = x
        if st.session_state["pokemon"] [player_num] and player_num:
            add_record(st.session_state["pokemon"][player_num], player_num)
            res = supabase.table("record").upsert({"pokemon": "test", "player_num": 1}).execute()
            st.write(res)

    with col1:
        if os.path.exists(f"images/pokemon/{st.session_state["pokemon"][x].split("(")[0]}.png"):
            img_copy = Image.open(f"images/pokemon/{st.session_state["pokemon"][x].split("(")[0]}.png").convert("RGBA").copy()
        
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
        try:
            default_index = list(df["name"]).index(st.session_state["pokemon"][x+5])
        except (ValueError, TypeError):
            default_index = 0
        st.session_state["pokemon"][x+5] = st.selectbox(f"味方{x}",df["name"],
            key = f"select_B{x}", index=default_index
        )
        
        player_num = x
        if st.session_state["pokemon"] [player_num] and player_num:
            add_record(st.session_state["pokemon"][player_num], player_num)

    with col6:
        img_path = f"images/pokemon/{st.session_state["pokemon"][x+5].split("(")[0]}.png"
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

container2 = st.container(key="container2")
with container2:
    if st.button("レーン宣告"):
        for i in range(1,6):
            if st.session_state["select"] [i] == "上":
                st.session_state["lanes"][i] = "上"

            if st.session_state["select"] [i] == "中央":
                st.session_state["lanes"][i] = "中央"
                    
            if st.session_state["select"] [i] == "下":
                st.session_state["lanes"][i] = "下"
            st.rerun()

st.markdown("""
    <style>
    .st-key-container2 div.stButton > button {position: absolute; top: -104px; left: 0px;
    width: 169px; height: 64px; min-height: 0px; margin-top: 0px}
    .st-key-container2 div.stButton > button * {font-size: 16px}
    .st-key-container2 div.stButton > button:hover,
    .st-key-container2 div.stButton > button:focus {opacity: 1 !important; background: #0E1117  !important;}
    </style>
    """,
    unsafe_allow_html= True)

st.write(st.session_state["pokemon"])

