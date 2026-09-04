import streamlit as st

theme = st.get_option("theme.base")
color = "black" if theme == "dark" else "white"

st.set_page_config(layout="wide")

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

from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# 1. 各画像の「表示状態」と「配置座標（x, y）」を管理
if "item_states" not in st.session_state:
    st.session_state.item_states = {
        "image_a": {"visible": True, "x": 50, "y": 50},
        "image_b": {"visible": True, "x": 500, "y": 50},
        "image_c": {"visible": True, "x": 1000, "y": 50},
    }

try:
    # 2. 背景（ベースとなる画像）の読み込み
    # ここでは image_a をベース（背景）として使っています
    bg_img = Image.open("images/UI/unite_map.png").convert("RGBA")
    bg_img = bg_img.resize((2500, 1500))
    
    # 3. 各パーツ画像の読み込み
    parts_img = {
        "image_a": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
        "image_b": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
        "image_c": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
    }

    # 4. 表示が「True」のものだけを背景に次々と貼り付ける（合成）
    canvas_img = bg_img.copy()
    for name, info in st.session_state.item_states.items():
        if info["visible"]:
            img = parts_img[name]
            canvas_img.paste(img, (info["x"], info["y"]), img)

    # 5. 合成された画像を表示し、クリック座標を取得
    state_key_str = str(st.session_state.item_states)
    coords = streamlit_image_coordinates(
        canvas_img, 
        width=800, 
        key=f"canvas_{state_key_str}"
    )

    # 6. クリックされた場所から「どの画像が選ばれたか」を判定
    if coords is not None:
        cx, cy = coords["x"], coords["y"]
        clicked_any = False

        # 手前（後から描画されたもの）から優先して判定するために reversed を使用
        for name, info in reversed(list(st.session_state.item_states.items())):
            if info["visible"]:
                img = parts_img[name]
                w, h = img.size
                x, y = info["x"], info["y"]

                # クリック座標がその画像の範囲内に入っているか
                if (x <= cx <= x + w) and (y <= cy <= y + h):
                    st.session_state.item_states[name]["visible"] = False
                    clicked_any = True
                    st.success(f" {name} がクリックされて消えました！")
                    st.rerun()

        if not clicked_any:
            st.info("画像の範囲外がクリックされました。")

except FileNotFoundError as e:
    st.error(f"ファイルが見つかりません。パスを確認してください: {e}")