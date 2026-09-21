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

#region lanes & pokemon state initialization
if "pokemon" not in st.session_state:
    st.session_state["pokemon"] = [None] * 11

if "target" not in st.session_state:
    st.session_state["target"] = [1] * 11

if "lanes" not in st.session_state:
    st.session_state["lanes"] = [None] * 11

img_top = Image.open("images/UI/top_lane.png").convert("RGBA")
img_center = Image.open("images/UI/center_lane.png").convert("RGBA")
img_bottom = Image.open("images/UI/bottom_lane.png").convert("RGBA")

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
        # ポケモンとレーン情報をリセット（ポケモン=null, レーン=中央、スライダーのtarget初期値=1など）
        supabase.table("record").update({"pokemon": None, "lane": "中央"}).not_.is_("player_num", "null").execute()
        st.session_state["pokemon"] = [None] * 11
        st.session_state["lanes"] = [None] * 11
        st.session_state["target"] = [1] * 11
        
        for y in range(1, 11):
            key_name = f"select{y}"
            if key_name in st.session_state:
                del st.session_state[key_name]
            lane_key = f"select_lanes{y}"
            if lane_key in st.session_state:
                del st.session_state[lane_key]

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


def add_record(pokemon=None, lane=None, player_num=None):
    data = {"player_num": player_num}
    if pokemon is not None:
        data["pokemon"] = pokemon
    if lane is not None:
        data["lane"] = lane
    
    supabase.table("record").upsert(data, on_conflict="player_num").execute()

def load_records():
    res = supabase.table("record").select("*").execute()
    return res.data

# リモート（Supabase）のデータをロードして同期
url_dt = load_records()
for row in url_dt:
    player_num = row.get("player_num")
    if player_num is None:
        continue
    player_num = int(player_num)
    if 1 <= player_num <= 10:
        remote_poke = row.get("pokemon")
        remote_lane = row.get("lane")

        key_name = f"select{player_num}"
        if st.session_state["pokemon"][player_num] != remote_poke:
            st.session_state["pokemon"][player_num] = remote_poke
            st.session_state[key_name] = remote_poke  
            
        # レーンの同期
        if remote_lane and st.session_state["lanes"][player_num] != remote_lane:
            st.session_state["lanes"][player_num] = remote_lane
            if player_num <= 5:  
                st.session_state["target"][player_num] = remote_lane
                lane_key = f"select_lanes{player_num}"
                if lane_key in st.session_state:
                    st.session_state[lane_key] = remote_lane

#region 入力欄
for x in range(1,6):
    col1, col2, col3, col4, col5, col6= st.columns([1, 2, 1.5, 0.5, 2, 1])
    with col2:
        current_valueA = st.session_state["pokemon"][x]
        try:
            default_indexA = list(df["name"]).index(current_valueA)
        except (ValueError, TypeError):
            default_indexA = 0
            
        select_valueA = st.selectbox(
            f"味方{x}",
            df["name"],
            key=f"select{x}",
            index=default_indexA
        )

        if select_valueA != current_valueA:
            st.session_state["pokemon"][x] = select_valueA
            add_record(pokemon=select_valueA, player_num=x)
            
    with col1:
        poke_name = st.session_state["pokemon"][x]
        if poke_name and os.path.exists(f"images/pokemon/{poke_name.split('(')[0]}.png"):
            img_copy = Image.open(f"images/pokemon/{poke_name.split('(')[0]}.png").convert("RGBA").copy()
        else:
            img_copy = Image.open("images/UI/紫icon_unite.jpg").convert("RGBA").copy()

        img_copy = img_copy.resize((100,100))

        current_lane = st.session_state["lanes"][x]
        if current_lane == "上":
            img_copy.paste(img_top, (-10,-15), img_top)
        elif current_lane == "中央":
            img_copy.paste(img_center, (-10,-15), img_center)
        elif current_lane == "下":
            img_copy.paste(img_bottom, (-10,-15), img_bottom)

        st.image(img_copy)

    with col3:
        st.markdown(
            f"""
            <style>
            .st-key-select_lanes{x} {{transform: translate(-120px, -30px); margin-top: 0px; padding: 10px; border-radius: 8px; width: 200px}}
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        default_lane_val = st.session_state["lanes"][x] if st.session_state["lanes"][x] in ["上", "中央", "下"] else "中央"
        st.session_state["target"][x] = st.select_slider("", options=["上", "中央", "下"],
         value=default_lane_val, key=f"select_lanes{x}", label_visibility="collapsed")

    with col5:
        current_valueB = st.session_state["pokemon"][x+5]
        try:
            default_indexB = list(df["name"]).index(current_valueB)
        except (ValueError, TypeError):
            default_indexB = 0
            
        select_valueB = st.selectbox(
            f"敵{x}",
            df["name"],
            key=f"select{x+5}",
            index=default_indexB
        )
    
        if select_valueB != current_valueB:
            st.session_state["pokemon"][x+5] = select_valueB
            add_record(pokemon=select_valueB, player_num=x+5)

    with col6:
        poke_name_b = st.session_state["pokemon"][x+5]
        img_path = f"images/pokemon/{poke_name_b.split('(')[0]}.png" if poke_name_b else ""
        if poke_name_b and os.path.exists(img_path):
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
        for i in range(1, 6):
            declared_lane = st.session_state["target"][i]
            st.session_state["lanes"][i] = declared_lane
            add_record(lane=declared_lane, player_num=i)
            
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

status = ["role","PS","DPS","耐久","CC強度","射程","AoE","ラスヒ","対CC","回復","減速","移動技","LCC","特殊"]

DPS_df = [None] * 11
耐久_df = [None] * 11

if "DPS_sum" not in st.session_state:
    st.session_state["DPS_sum"] = [0] * 2
DPS_sum = st.session_state["DPS_sum"]

if "耐久_sum" not in st.session_state:
    st.session_state["耐久_sum"] = [0] * 2
耐久_sum = st.session_state["耐久_sum"]

def status_sum():
    for z in range(1,11):
        team = 0 if z <= 5 else 1

        poke = (df["name"] == st.session_state["pokemon"][z])
        DPS_df[z] = int(df[poke]["DPS"].iloc[0])
        耐久_df[z] = int(df[poke]["耐久"].iloc[0])
        DPS_sum [team] += DPS_df[z]
        耐久_sum [team] += 耐久_df[z]

status_sum()
st.write("DPS=", DPS_sum[0], DPS_sum[1])
st.write("耐久=", 耐久_sum[0], 耐久_sum[1])

