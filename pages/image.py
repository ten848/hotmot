import streamlit as st
from PIL import Image
import google.generativeai as genai
import urllib.parse
import webbrowser

# -----------------------------
# Gemini API の設定（secretsから安全に読み込み）
# -----------------------------
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("APIキーが設定されていません。.streamlit/secrets.toml を確認してください。")

# -----------------------------
# 領域切り出し（ご指定の完璧な座標）
# -----------------------------
def crop_target_name_area(img):
    w, h = img.size
    
    left = int(w * 0.05)
    right = int(w * 0.18)
    top = int(h * 0.55)
    bottom = int(h * 0.65)
    
    if top >= bottom:
        bottom = top + 20
        
    box = (max(0, left), max(0, top), min(w, right), min(h, bottom))
    return img.crop(box)

# -----------------------------
# Gemini APIに画像を投げて名前を抽出
# -----------------------------
def extract_name_with_ai(cropped_img):
    # 軽量かつ高性能なモデルを使用
    model = genai.GenerativeModel('gemini-3.6-flash')
    
    prompt = (
        "この画像はポケモンユナイトのプレイヤー名が表示されている領域です。"
        "ここに書かれているプレイヤー名（例: 神速三段Yt など）を正確に読み取り、"
        "余分な説明や記号、改行を一切含めず、**プレイヤー名のテキスト文字列だけ**を返してください。"
    )
    
    try:
        response = model.generate_content([prompt, cropped_img])
        name = response.text.strip()
        name = name.replace("\n", "").replace("`", "").strip()
        return name
    except Exception as e:
        st.error(f"AI抽出エラー: {e}")
        return None

# -----------------------------
# URL生成
# -----------------------------
def open_partial_match_page(name):
    encoded = urllib.parse.quote(name)
    url = f"https://uniteapi.dev/jp/search?q={encoded}"
    webbrowser.open(url)

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("ポケモンユナイト: AI高精度抽出 ＆ UniteAPI検索")

uploaded = st.file_uploader("フル画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    
    # 1. 座標で切り出し
    cropped = crop_target_name_area(img)
    
    # 2. AIで文字抽出
    with st.spinner("AIがプレイヤー名を解析中..."):
        name = extract_name_with_ai(cropped)
    
    st.write("抽出された名前:", name if name else "（検出失敗）")

    st.write("切り出された領域（デバッグ用）:")
    st.image(cropped)

    if name:
        st.write(f"{name} の部分一致ページを開きます")
        open_partial_match_page(name)