# import streamlit as st
# st.write("8:50------7:20------5:50-----------4:20-----------2:50------------1:20")
# st.write("-----7:45------6:15------4:45-----------3:15------------1:45----------")
# st.write("---------------------------------4:30-----------3:00------------1:30------")
import streamlit as st
import base64
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from db import read_table
from supabase import create_client
import os
import time
import urllib.parse
# import webbrowser
from google import generativeai as genai

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
        
        default_lane_val = st.session_state["lanes"][x] if st.session_state["lanes"][x] in ["上", "中央", "下"] else "下"
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

# region def
data = [None] * 11
PS_df = [None] * 11
DPS_df = [None] * 11
耐久_df = [None] * 11
CC強度_df = [None] * 11
射程_df = [None] * 11
AoE_df = [None] * 11
ラスヒ_df = [None] * 11
対CC_df = [None] * 11
回復_df = [None] * 11
減速_df = [None] * 11
移動技_df = [None] * 11
LCC_df = [None] * 11
特殊_df = [None] * 11

PS_sum = [0] * 2
DPS_sum = [0] * 2
耐久_sum= [0] * 2
CC強度_sum= [0] * 2
射程_sum= [0] * 2
AoE_sum= [0] * 2
ラスヒ_sum= [0] * 2
対CC_sum= [0] * 2
回復_sum= [0] * 2
減速_sum= [0] * 2
移動技_sum= [0] * 2
LCC_sum= [0] * 2
特殊_sum= [0] * 2

if "poke_jp" not in st.session_state:
    st.session_state["poke_jp"] = [None] * 11
# endregion

import ast
df["カウンター"] = df["カウンター"].apply(ast.literal_eval)

# 自分が何番目か
me = 0
for z in range(1,6):
    if not st.session_state["pokemon"][z]:
        me = z
        break

done = [0, 0]
for z in range(1,11):
    team = 0 if z <= 5 else 1
    if st.session_state["pokemon"][z]:
        done[team] += 1

def status_sum():
    for z in range(1,11):
        team = 0 if z <= 5 else 1

        data[z] = (df["name"] == st.session_state["pokemon"][z])
        row = df.loc[data[z]].iloc[0]

        PS_df[z] = int(row["PS"])
        DPS_df[z] = int(row["DPS"])
        耐久_df[z] = int(row["耐久"])
        CC強度_df[z] = int(row["CC強度"])
        射程_df[z] = int(row["射程"])
        AoE_df[z] = int(row["AoE"])
        ラスヒ_df[z] = int(row["ラスヒ"])
        対CC_df[z] = int(row["対CC"])
        回復_df[z] = int(row["回復"])
        if "support" in row["role"] and row["回復"] == 1:
            耐久_df[z] += 2.0
        減速_df[z] = int(row["減速"])
        移動技_df[z] = int(row["移動技"])
        LCC_df[z] = int(row["LCC"])
        特殊_df[z] = int(row["特殊"])

        PS_sum [team] += PS_df[z]
        DPS_sum [team] += DPS_df[z]
        耐久_sum [team] += 耐久_df[z]
        # if "support" in row["role"] and row["回復"] == 1:
        #     耐久_sum [team] += 0.4 * done[team]
        CC強度_sum [team] += CC強度_df[z]
        射程_sum [team] += 射程_df[z]
        AoE_sum [team] += AoE_df[z]
        ラスヒ_sum [team] += ラスヒ_df[z]
        対CC_sum [team] += 対CC_df[z]
        回復_sum [team] += 回復_df[z]
        減速_sum [team] += 減速_df[z]
        移動技_sum [team] += 移動技_df[z]
        LCC_sum [team] += LCC_df[z]
        特殊_sum [team] += 特殊_df[z]

status_sum()

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

col1,col2,col3,col4 = st.columns(4)
with col1:
    target_area1 = st.container()
with col2:
    target_area2 = st.container()
with col3:
    target_area3 = st.container()
with col4:
    target_area4 = st.container()


if st.checkbox("サポタンなし"):
    no_trust = 1
else:
    no_trust = 0

from collections import defaultdict

def all_counter_dict():
    all_dict = defaultdict(int)

    for idx, row in df.iterrows():
        for i in row["カウンター"]:
            if i:
                all_dict[i] += 1

    return dict(all_dict)

all_dict = all_counter_dict()
counters = {0: defaultdict(int), 1: defaultdict(int)}

for z in range(1, 11):
    if not st.session_state["pokemon"][z]:
        continue

    team = 0 if z <= 5 else 1

    data[z] = (df["name"] == st.session_state["pokemon"][z])
    row = df.loc[data[z]].iloc[0]

    for i in row["カウンター"]:
        if i:
            counters[team][i] += 1

def average_status():
    numeric_df = df.select_dtypes(include=["int64", "float64"])
    return numeric_df.mean()


all = df[df["name"] != ""].copy()

def scores():
    for idx, row in all.iterrows():
        score = calculation(row)
    return all


pokemon_names = df["名前"].tolist()
scores_dict = dict.fromkeys(pokemon_names)
scores_dict = {name: 0 for name in df["名前"]}
count = len(scores_dict)

translate = dict(zip(df["name"], df["名前"]))
re_translate = dict(zip(df["名前"], df["name"]))

for z in range(0, 11):
    eng = st.session_state["pokemon"][z]
    st.session_state["poke_jp"][z] = translate.get(eng)

def calculation():
    for key in scores_dict:
        scores_dict[key] = 0.0
        
    no_bring = [None] * 2

    no_bring[0] = done[0] - 移動技_sum[0]
    no_bring[1] = done[1] - 移動技_sum[1]

    PS_border = 11
    DPS_border = 11
    耐久_border = 12
    CC強度_border = 11
    射程_border = 10
    AoE_border = 10

    roops = 5
    porker = 0
    ally_ADC = 0
    ally_fighter = 0
    ally_tank = 0
    ally_sapotan = 0

    enemy_ADC = 0
    enemy_fighter = 0

    assassin_power = 0

    for z in range(1,6):
        # region 定義
        ally_data = df[df["名前"] == st.session_state["poke_jp"][z]]
        ally_名前 = ally_data["名前"].values[0]
        ally_role = ally_data["role"].values[0]
        ally_DPS = ally_data["DPS"].values[0]
        ally_耐久 = ally_data["耐久"].values[0]
        ally_CC強度 = ally_data["CC強度"].values[0]
        ally_射程 = ally_data["射程"].values[0]
        ally_対CC = ally_data["対CC"].values[0]
        ally_回復 = ally_data["回復"].values[0]
        ally_移動技 = ally_data["移動技"].values[0]
        ally_特殊 = ally_data["特殊"].values[0]
        
        poke_jp = st.session_state["poke_jp"][z + 5]
        enemy_data = df[df["名前"] == poke_jp]
        enemy_名前 = enemy_data["名前"].values[0]
        enemy_role = enemy_data["role"].values[0]
        enemy_DPS = enemy_data["DPS"].values[0]
        enemy_耐久 = enemy_data["耐久"].values[0]
        enemy_CC強度 = enemy_data["CC強度"].values[0]
        enemy_射程 = enemy_data["射程"].values[0]
        enemy_対CC = enemy_data["対CC"].values[0]
        enemy_回復 = enemy_data["回復"].values[0]
        enemy_移動技 = enemy_data["移動技"].values[0]
        enemy_特殊 = enemy_data["特殊"].values[0]
        # endregion

        # 特定のスコアに直接干渉
        if (poke_jp == "リザX" or poke_jp == "リザY" or poke_jp == "ゲンガー（たたりめ）"
            or poke_jp == "メガギャラドス" or poke_jp == "メガルカリオ" or poke_jp == "ゾロアーク（だましうち）"
            or poke_jp == "ゾロアーク（つじぎり）" or poke_jp == "ウーラオス（連撃）"):
            for bind in ("リザX","リザY","ヤドラン","アマージョ","ミミッキュ（かげぽこ）","ミミッキュ（ルーム）","ミミッキュ（かげつめ）"):
                scores_dict[bind] += 0.4

        if enemy_対CC == 2 or poke_jp == "ガラルギャロップ":
            for through in ("カイリキー", "アマージョ", "マッシブーン"):
                scores_dict[through] += 0.4

        # スコアを全探索
        for nameart, degree in scores_dict.items():
            name = nameart.split('（')[0]   # scores_dictからキーを取り出し、技選択を消す
            target_datas = df[df["名前"] == nameart].to_dict(orient="records")[0]

            target_counter = target_datas["カウンター"]
            target_counter = [c for c in target_counter if c]
            target_role = target_datas["role"]

            target_PS = target_datas["PS"]
            target_DPS = target_datas["DPS"]
            target_耐久 = target_datas["耐久"]
            if target_role == "support" and target_回復 == 1:
                target_耐久 += 2.0
            target_CC強度 = target_datas["CC強度"]
            target_射程 = target_datas["射程"]
            target_AoE = target_datas["AoE"]
            target_対CC = target_datas["対CC"]
            target_回復 = target_datas["回復"]
            target_減速 = target_datas["減速"]
            target_移動技 = target_datas["移動技"]
            target_特殊 = target_datas["特殊"]

# ///////////////////////////////////////////////////////////////////////////////////////////////

            # region カウンター欄から減点
            if target_counter and poke_jp.startswith(tuple(target_counter)):
                scores_dict[nameart] -= 0.4
                if nameart == "タイレーツ":
                    scores_dict[nameart] -= 10.0

            if enemy_role in target_counter:  
                scores_dict[nameart] -= 0.2

            if "射程4" in target_counter:
                if enemy_射程 == 4:
                    scores_dict[nameart] -= 0.4
                    if nameart == "アローラキュウコン（ふぶき）":
                        scores_dict[nameart] -= 0.4

            # ステータス和について
            if "高耐久" in target_counter and 耐久_sum[1] >= 2.4 * done[1]:
                scores_dict[nameart] -= 0.4 / roops

            if "高CC" in target_counter:
                if CC強度_sum[1] >= 2.4 * done[1]:
                    scores_dict[nameart] -= 0.2 / roops
                if enemy_CC強度 == 4 and enemy_射程 >= 3:
                    scores_dict[nameart] -= 0.4 / roops

            if "高AoE" in target_counter and AoE_sum[1] >= 2.4 * done[1]:
                scores_dict[nameart] -= 0.4 / roops
            #endregion

# ////////////////////////////////////////////////////////////////////////////////////////////

            # region カウンター欄から加点
            for enemy_counter, degree in counters[1].items():   # counters[1]から敵のカウンターと値を取り出す
                if name == enemy_counter:
                    scores_dict[nameart] += degree * 0.4 / roops
                    if name == "タイレーツ":
                        scores_dict[nameart] += degree * 0.5 / roops

                if target_role == enemy_counter:
                    scores_dict[nameart] += degree * 0.4 / roops

                if enemy_counter == "高耐久" and target_耐久 == 4:
                    scores_dict[nameart] += 0.2 / roops

                if enemy_counter == "高CC" and target_CC強度 == 3:
                    scores_dict[nameart] += 0.4 / roops
                
                if enemy_counter == "射程4" and target_射程 == 4:
                    scores_dict[nameart] += 0.4 / roops

                if enemy_counter == "高AoE" and target_AoE == 4:
                    scores_dict[nameart] += 0.4 / roops

            if name in counters[0]:
                scores_dict[nameart] += 0.2 * degree / roops
            # endregion

# /////////////////////////////////////////////////////////////////////////////////////////

            # region 基礎得点
            for i in range(0, 17):
                if i - 2 < abs((PS_sum[0] + target_PS) - (PS_border / 5) * (done[0] + 1)) < i + 2:
                    scores_dict[nameart] += (1.2 - i * 0.2) / roops

            for i in range(0, 17):
                if i - 1 < abs((DPS_sum[0] + target_DPS) - (DPS_border / 5) * (done[0] + 1)) < i + 1:
                    scores_dict[nameart] += (1.2 - i * 0.2) / roops

            for i in range(0, 17):
                if i - 1 < abs((耐久_sum[0] + target_耐久) - (耐久_border / 5) * (done[0] + 1)) < i + 1:
                    scores_dict[nameart] += (1.0 - i * 0.3) / roops

            for i in range(0, 17):
                if i - 1 < abs((CC強度_sum[0] + target_CC強度) - (CC強度_border / 5) * (done[0] + 1)) < i + 1:
                    scores_dict[nameart] += (0.8- i * 0.1) / roops
                    
            for i in range(0, 17):
                if i - 1 < abs((射程_sum[0] + target_射程) - (射程_border / 5) * (done[0] + 1)) < i + 1:
                    scores_dict[nameart] += (1.2 - i * 0.1) / roops

            for i in range(0, 17):
                if i - 1 < abs((AoE_sum[0] + target_AoE) - (AoE_border / 5) * (done[0] + 1)) < i + 1:
                    scores_dict[nameart] += (0.8 - i * 0.1) / roops
            # endregion

# //////////////////////////////////////////////////////////////////////////////////////////////
            # region 細かい調整
            if (nameart == "カメックス" or nameart == "ガブリアス") and AoE_sum[0] > 2 * done[0]:
                scores_dict[nameart] += 0.2 / roops
            if (nameart == "カメックス" or nameart == "ガブリアス") and target_AoE > 2:
                scores_dict[nameart] += 0.05

            if nameart == "ゲンガー（たたりめ）" and enemy_耐久 == 4:
                scores_dict[nameart] += 2.0
            
            if nameart == "イワパレス" and no_bring[1] >= 3:
                scores_dict[nameart] += 0.8 / roops
            if no_bring[0] >= 2 and target_移動技 == 1: # イワパレス対策
                scores_dict[nameart] += 0.2 / roops

            if nameart.startswith("ラティオス") and enemy_role == "tank" and enemy_移動技 == 0:
                scores_dict[nameart] += 0.2
            if poke_jp.startswith("ラティオス") and target_role == "tank" and target_移動技 == 0:
                scores_dict[nameart] -= 0.2
            
            if nameart == "ソウブレイズ" and enemy_対CC == 1:
                scores_dict[nameart] -= 0.2
            if poke_jp == "ソウブレイズ" and target_対CC == 1:
                scores_dict[nameart] += 0.2
            
            if nameart == "ストリンダー" and enemy_耐久 == 4:
                scores_dict[nameart] += 0.2
            if poke_jp == "ストリンダー" and target_耐久 == 4:
                scores_dict[nameart] -= 0.2
            if nameart == "ストリンダー" and 耐久_sum[1] >= 13:
                scores_dict[nameart] += 0.3 / roops

            if nameart == "ウーラオス（いちげき）" and enemy_対CC == 1: # なおしNG
                scores_dict[nameart] -= 0.4
            if poke_jp == "ウーラオス（いちげき）" and target_対CC == 1:
                scores_dict[nameart] += 0.4

            if nameart == "ハッサム" and enemy_特殊 == 1 and enemy_DPS >= 2: # 特殊かつ高火力
                scores_dict[nameart] -= 0.2
            if poke_jp == "ハッサム" and target_特殊 == 1 and target_DPS >= 2:
                scores_dict[nameart] += 0.2
            
            if (nameart == "ギャラドス" or nameart == "メガギャラドス") and PS_sum[1] > 2.6 * done[1]:
                scores_dict[nameart] += 0.2 / roops
            if (nameart == "ギャラドス" or nameart == "メガギャラドス") and enemy_role == "support" and enemy_回復 == 0:
                scores_dict[nameart] -= 1.0
            if (poke_jp == "ギャラドス" or poke_jp == "メガギャラドス") and target_role == "support" and target_回復 == 0:
                scores_dict[nameart] += 1.0

            if nameart == "ドードリオ" and enemy_CC強度 == 4:
                scores_dict[nameart] -= 0.4
            if poke_jp == "ドードリオ" and target_CC強度 == 4:
                scores_dict[nameart] += 0.4
            if nameart == "ドードリオ" and 減速_sum[1] >= 3: # 減速NG
                scores_dict[nameart] -= 0.8 / roops
            if nameart == "ドードリオ" and done[1] == 5 and 減速_sum[1] == 0:
                scores_dict[nameart] += 0.4 / roops
            if poke_jp == "ドードリオ" and target_減速 == 1: # 減速推奨
                scores_dict[nameart] += 0.4
            
            if (nameart == "ダークライ（シャドクロ）" or nameart == "エーフィ（バラマキ）") and enemy_role == "support":
                if enemy_回復 == 0: # ノーヒール
                    scores_dict[nameart] += 0.4
                else:
                    scores_dict[nameart] -= 2.0
            if poke_jp == "ダークライ（シャドクロ）" and target_role == "support" and target_回復 == 1:
                scores_dict[nameart] += 0.4

            if (nameart == "カイリキー" or nameart == "アマージョ" or nameart == "マッシブーン") and enemy_対CC == 2: # 妨害耐性
                scores_dict[nameart] += 0.4
            if (poke_jp == "カイリキー" or poke_jp == "アマージョ" or poke_jp == "マッシブーン") and target_対CC == 2: # 妨害耐性
                scores_dict[nameart] -= 0.4

            if nameart == "スイクン" and enemy_role == "ADC":
                scores_dict[nameart] += 0.4
            if poke_jp == "スイクン" and target_role == "ADC":
                scores_dict[nameart] -= 0.4

            if (nameart == "ブラッキー（くろまな）" and enemy_射程 <= 2 and enemy_対CC != 1
                and enemy_role == "ADC" or enemy_role == "assassin" or enemy_role == "fighter"): 
                scores_dict[nameart] += 0.4
            if (poke_jp == "ブラッキー（くろまな）" and target_射程 <= 2 and target_対CC != 1
                and (target_role == "ADC" or target_role == "assassin" or target_role == "fighter")): 
                scores_dict[nameart] -= 0.4
            
            if nameart == "ピクシー（じゅうりょく）":
                if enemy_射程 <= 2 and enemy_移動技 == 1:
                    scores_dict[nameart] += 0.4
                for i in range(1,5):
                    if enemy_射程 == i:
                        scores_dict[nameart] -= i * 0.1
            if poke_jp == "ピクシー（じゅうりょく）":
                if target_射程 <= 2 and target_移動技 == 1:
                    scores_dict[nameart] -= 0.4
                for i in range(1,5):
                    if target_射程 == i:
                        scores_dict[nameart] += i * 0.1
            
            if ally_射程 == 4:
                porker += 1
            if target_射程 == 4 and porker > 0:
                scores_dict[nameart] -= 0.4 / roops
            if target_射程 == 4 and CC強度_sum[1] > 2.0 * done[1]:
                scores_dict[nameart] += 0.4 / roops

            if enemy_CC強度 > 3:
                if target_対CC > 0:
                    scores_dict[nameart] += 0.05
                    if target_対CC >= 2:
                        scores_dict[nameart] += 0.05
                        if target_対CC == 4:
                                scores_dict[nameart] += 0.1
                elif (target_role == "assassin" or target_role == "fighter") and nameart != "ゲンガー（たたりめ）":
                    scores_dict[nameart] -= 0.4

            if target_CC強度 >= 3 and enemy_対CC >= 2:
                scores_dict[nameart] -= 2.0
            if enemy_CC強度 >= 3 and target_対CC >= 2:
                scores_dict[nameart] += 0.4

            if target_role == "ADC":
                ally_ADC += 1
            if enemy_role == "ADC":
                enemy_ADC += 1
    
            if nameart == "ラプラス" or nameart == "ヤドラン" or nameart == "フリーザー" or nameart == "ヌメルゴン":
                if enemy_ADC == 0:
                    scores_dict[nameart] += 0.8 / roops
            elif target_role == "tank":
                if enemy_ADC != 0:
                    scores_dict[nameart] += 0.1 / roops
            if poke_jp == "ラプラス" or poke_jp == "ヤドラン" or poke_jp == "フリーザー" or poke_jp == "ヌメルゴン":
                if target_role == "ADC" and ally_ADC == 0:
                    scores_dict[nameart] += 0.4 / roops

            if target_role == "fighter":
                ally_fighter += 1
            if enemy_role == "fighter":
                enemy_fighter += 1

            if ally_fighter >= 2 and target_role == "support" and target_回復 == 1:
                scores_dict[nameart] += 0.4 / roops

            if (nameart == "マフォクシー（ニトチャ）" or nameart == "アローラキュウコン（ふぶき）") and enemy_fighter >= 2:
                scores_dict[nameart] += 0.4
            if (poke_jp == "マフォクシー（ニトチャ）" or poke_jp == "アローラキュウコン（ふぶき）") and target_role == "fighter":
                scores_dict[nameart] -= 0.4

            if target_role == "fighter" and target_対CC == 0 and enemy_CC強度 == 4:
                scores_dict[nameart] -= 0.8
            if enemy_role == "fighter" and enemy_対CC == 0 and target_CC強度 == 4:
                scores_dict[nameart] += 0.8
            
            if ally_role == "tank":
                ally_tank += 1 / count

            if ally_role == "support" or ally_role == "tank" or ally_role == "kyuwawa-":
                ally_sapotan += 1 / count
 
            if target_role == "tank" and ally_tank > 0:
                scores_dict[nameart] -= 0.4

            if (target_role == "support" or target_role == "tank") and ally_sapotan > 1.9:
                scores_dict[nameart] = -100

            ally_assassin = 0
            if ally_role == "assassin":
                ally_assassin += 1
            if target_role == "assassin" and ally_assassin > 0:
                scores_dict[nameart] -= 1.6 / roops
            
            if (target_role == "assassin" or target_role == "ADC") and CC強度_sum[1] > 2.0 * done[1]:
                scores_dict[nameart] -= 0.4 / roops
            if (target_role == "assassin" or target_射程 == 4) and enemy_射程 == 4: # 射程4が敵にいると 射程4とアサシンを加点
                scores_dict[nameart] += 0.2

            if ((enemy_role =="mage" or enemy_role =="ADC"
                 or nameart == "イベルタル" or nameart == "ストリンダー"
                or nameart == "エーフィ（バラマキ）" or nameart.startswith("ラティアス")) # やわらかい敵が多いとスピード加点
                and poke_jp != "エースバーン（きっく）" and poke_jp != "エースバーン（かえん）"):
                assassin_power += 1 / count
            
                if assassin_power >= 2 and target_role == "assassin": # やわらかい敵が2体か、3体以上か
                    scores_dict[nameart] += 0.4 / roops
                if assassin_power >= 3:
                    scores_dict[nameart] += 0.6 / roops

            if ((target_role =="mage" or target_role =="ADC"
                 or nameart == "イベルタル" or nameart == "ストリンダー"
                 or nameart == "エーフィ（バラマキ）" or nameart.startswith("ラティアス")) # 敵にスピードがいたらやわらかいポケモン減点
                 and nameart != "エースバーン（きっく）" and nameart != "エースバーン（かえん）"
                 and enemy_role == "assassin"):
                    scores_dict[nameart] -= 1.5


            if not (target_role == "support" or nameart == "ミュウ1" or nameart == "パルキア" or nameart == "イベルタル" or nameart == "ストリンダー"
                 or nameart.startswith("エーフィ") or nameart.startswith("ミュウツーX")):
                if done[0] == 0:
                    scores_dict[nameart] -= 0.5 / roops
            # endregion

# ///////////////////////////////////////////////////////////////////////////

    # ネタキャラを除外
    scores_dict[""] = 0
    scores_dict["バニリッチ"] = 0
    scores_dict["フェン"] = 0

    for nameart, degree in scores_dict.items():
        name = nameart.split('（')[0]
        target_datas = df[df["名前"] == nameart].to_dict(orient="records")[0]
        target_role = target_datas["role"]
        if no_trust == 1 and (target_role == "support" or target_role == "tank"): # サポタンを除外
            scores_dict[nameart] = 0
        if (done[0] == 0 and done[1] == 0) or done[0] == 5:
            scores_dict[nameart] = 0
        for z in range(1,11):
            if st.session_state["poke_jp"][z] != "":
                if st.session_state["poke_jp"][z].startswith(name): # 使えないキャラを削除
                    scores_dict[nameart] = 0

calculation()

scores_dict = {k: round(v, 1) for k, v in scores_dict.items()}
plus_scores_dict = dict(sorted({k: v for k, v in scores_dict.items() if v > 0}.items(),
    key=lambda x: x[1], reverse=True))

max = 0
max_key = {}
teruru_keys = ["フシギバナ（レーザー）","ピカチュウ（ボルテ）","ピカチュウ（十万V）","ピクシー（ゆびふり）",
               "ピクシー（じゅうりょく）","アローラキュウコン（ふぶき）","ギャラドス","ラプラス","シャワーズ（aqua）",
               "カビゴン（ヘビボン）","エーフィ（サイコショック）","ブラッキー（イカサマ）","ブラッキー（くろまな）",
               "ハッサム","ラティアス（ミスト）","スイクン","メガルカリオ","リーフィア","パルキア","ダークライ（シャドクロ）",
               "イワパレス","レシラム","マフォクシー（うず）","ゲッコウガ（手裏剣）","ギルガルド","ニンフィア（ボイス）",
               "オーロット","イベルタル","ダダリン","エースバーン（かえん）","ワタシラガ（かふんだんご）","モルペコ",
               "パーモット","グレンアルマ（キャノン）","グレンアルマ（うず）","ミライドン（ぎゅいーん）","ミライドン（いなどら）"
               ]

teruru_dict = {k: plus_scores_dict[k] for k in teruru_keys if k in plus_scores_dict}
teruru_dict = dict(sorted({k: v for k, v in teruru_dict.items()}.items(), key = lambda x: x[1], reverse = True))
# top3_teruru = dict(sorted(teruru_dict.items(), key = lambda x: x[1],reverse = True)[:3])
# top3_ten = dict(sorted(plus_scores_dict.items(), key = lambda x: x[1],reverse = True)[:3])

recommend_list = []
for recommend in plus_scores_dict.keys():
    recommend = re_translate.get(recommend)
    recommend = recommend.split('(')[0]
    with open(f"images/pokemon/{recommend}.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        recommend_list.append(encoded)

sapotan_scores_dict = {}
non_sapotan_scores_dict = {}
for key, value in plus_scores_dict.items():
    data = df[df["名前"] == key]
    role = data["role"].values[0]
    if role == "tank" or role == "support":
        sapotan_scores_dict[key] = value
    else:
        non_sapotan_scores_dict[key] = value

sapotan_recommend_list = []
non_sapotan_recommend_list = []
for recommend in sapotan_scores_dict.keys():
    recommend = re_translate.get(recommend)
    recommend = recommend.split('(')[0]
    with open(f"images/pokemon/{recommend}.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        sapotan_recommend_list.append(encoded)
for recommend in non_sapotan_scores_dict.keys():
    recommend = re_translate.get(recommend)
    recommend = recommend.split('(')[0]
    with open(f"images/pokemon/{recommend}.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        non_sapotan_recommend_list.append(encoded)

teru_recommend_list = []
for recommend in teruru_dict.keys():
    recommend = re_translate.get(recommend)
    recommend = recommend.split('(')[0]
    with open(f"images/pokemon/{recommend}.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        teru_recommend_list.append(encoded)

teru_sapotan_scores_dict = {}
teru_non_sapotan_scores_dict = {}
for key, value in teruru_dict.items():
    data = df[df["名前"] == key]
    role = data["role"].values[0]
    if role == "tank" or role == "support":
        teru_sapotan_scores_dict[key] = value
    else:
        teru_non_sapotan_scores_dict[key] = value

teru_sapotan_recommend_list = []
teru_non_sapotan_recommend_list = []
for recommend in teru_sapotan_scores_dict.keys():
    recommend = re_translate.get(recommend)
    recommend = recommend.split('(')[0]
    with open(f"images/pokemon/{recommend}.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        teru_sapotan_recommend_list.append(encoded)
for recommend in teru_non_sapotan_scores_dict.keys():
    recommend = re_translate.get(recommend)
    recommend = recommend.split('(')[0]
    with open(f"images/pokemon/{recommend}.png", "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        teru_non_sapotan_recommend_list.append(encoded)

x = len(non_sapotan_recommend_list)
if x > 3:
    x = 3
for i in range(0, x):
    html = f"""
    <div style="position: relative; height: 0px;">
        <img src="data:image/png;base64,{non_sapotan_recommend_list[i]}" 
            width="50" height="50"
            style="position: absolute; top: calc(-680px - {16 * i}px); right: calc(100px - {50 * i}px);">
        </div>
    </div>
    """
    target_area1.markdown(html, unsafe_allow_html=True)

x = len(teru_non_sapotan_recommend_list)
if x > 3:
    x = 3
for i in range(0, x):
    html = f"""
    <div style="position: relative; height: 0px;">
        <img src="data:image/png;base64,{teru_non_sapotan_recommend_list[i]}" 
            width="50" height="50"
            style="position: absolute; top: calc(-680px - {16 * i}px); right: calc(-200px - {50 * i}px);">
        </div>
    </div>
    """
    target_area2.markdown(html, unsafe_allow_html=True)

x = len(sapotan_recommend_list)
if x > 3:
    x = 3
for i in range(0, x):
    html = f"""
        <div style="position: relative; height: 0px;">
            <img src="data:image/png;base64,{sapotan_recommend_list[i]}" 
                width="50" height="50"
                style="position: absolute; top: calc(-680px - {16 * i}px); right: calc(300px - {50 * i}px);">
            </div>
        </div>
        """
    target_area3.markdown(html, unsafe_allow_html=True)

x = len(teru_sapotan_recommend_list)
if x > 3:
    x = 3
for i in range(0, x):
    html = f"""
        <div style="position: relative; height: 0px;">
            <img src="data:image/png;base64,{teru_sapotan_recommend_list[i]}" 
                width="50" height="50"
                style="position: absolute; top: calc(-680px - {16 * i}px); right: calc(0px - {50 * i}px);">
        </div>
        """
    target_area4.markdown(html, unsafe_allow_html=True)

selected_eng = st.selectbox("select",df["name"])
selected_jp = translate.get(selected_eng)

selected_data = plus_scores_dict.get(selected_jp,0)
st.write(selected_data)

# st.write(top3_teruru)
st.write(plus_scores_dict)

#region gemini
if "GEMINI_API_KEY" in st.secrets:
  genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
  st.error("APIキーが設定されていません。.streamlit/secrets.toml")

def crop_target_generated_area(img):
  w, h = img.size

  left = int(w * 0)
  right = int(w * 1)
  top = int(h * 0)
  bottom = int(h * 1)

  box = (max(0, left), max(0, top), min(w, right), min(h, bottom))
  return img.crop(box)

def extract_generated(cropped_img):
  model = genai.GenerativeModel("gemini-3.5-flash-lite")

  img_to_send = cropped_img.copy()
  img_to_send.thumbnail(
      (1000, 1000), Image.Resampling.LANCZOS
  )

  prompt = (
      "画像内のUnicodeの文字コードや正確な特殊文字を使用し、計10人のプレイヤー名「だけ」を1行につき1つ返して"
  )

  try:
    start_time = time.time()
    response = model.generate_content([prompt, img_to_send])
    end_time = time.time()
    elapsed_time = end_time - start_time
    st.write(f"【Gemini APIの処理時間】: {elapsed_time:.2f}秒")

    generated = response.text.strip()
    generated = generated.replace("`", "").strip()
    targets = [line.strip() for line in generated.splitlines() if line.strip()]
    return targets
  except Exception as e:
    st.error(f"Error: {e}")
    return None

# def open_page(target_player_name):
#   encoded = urllib.parse.quote(target_player_name)
#   url = f"https://uniteapi.dev/jp/search?q={encoded}"
#   webbrowser.open(url)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_record(player_name, url, tag):
    data = {"player_name": player_name, "url": url, "tag":tag}
    res = supabase.table("record").insert(data).execute()
    return res.data

uploaded = st.file_uploader("データ、とらせてもらうよ。",type =["png", "jpg", "jpeg"])

if uploaded:
  img = Image.open(uploaded)

  cropped = crop_target_generated_area(img)

  with st.spinner("なるほどなるほど..."):
    targets = extract_generated(cropped)

  st.write("解析終了:")

  supabase.table("record").delete().not_.is_("url", "null").execute()

  for i, player_name in enumerate(targets):
      encoded = urllib.parse.quote(player_name)
      url = f"https://uniteapi.dev/jp/search?q={encoded}"

      tag = 1 if i < 5 else 2

      if player_name and url and tag:
        add_record(player_name, url, tag)

def load_url():
    res = supabase.table("record").select("*").not_.is_("url", "null").execute()
    return res.data

url_dt = load_url()
col1, col2 = st.columns(2)
for row in url_dt:
    name = row.get("player_name")
    url = row.get("url")
    tag = row.get("tag")
    
    if tag == "1":
        col1.markdown(f"- [{name}]({url})", unsafe_allow_html=True)
    elif tag == "2":
        target_area4.markdown(
    f"""
    <div style="position: absolute; top: 0px; left: 0px;">
        <a href="{url}" target="_blank">{name}</a>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)
with col1:
    st.write("PS=", PS_sum[0], PS_sum[1])
    st.write("DPS=", DPS_sum[0], DPS_sum[1])
    st.write("耐久=", 耐久_sum[0], 耐久_sum[1])
    st.write("CC強度=", CC強度_sum[0], CC強度_sum[1])

with col2:
    st.write("射程=", 射程_sum[0], 射程_sum[1])
    st.write("AoE=", AoE_sum[0], AoE_sum[1])
    st.write("ラスヒ=", ラスヒ_sum[0], ラスヒ_sum[1])
    st.write("対CC=", 対CC_sum[0], 対CC_sum[1])

with col3:
    st.write("回復=", 回復_sum[0], 回復_sum[1])
    st.write("減速=", 減速_sum[0], 減速_sum[1])
    st.write("移動技=", 移動技_sum[0], 移動技_sum[1])
    st.write("LCC=", LCC_sum[0], LCC_sum[1])
    st.write("特殊=", 特殊_sum[0], 特殊_sum[1])

with st.expander("カウンターされやすさ"):
    st.write(all_dict)

average = average_status()
with st.expander("average"):
    st.write(average)

with st.expander("counters"):
    st.write(counters)