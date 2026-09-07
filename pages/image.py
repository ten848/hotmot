import streamlit as st
from PIL import Image
import google.generativeai as genai
import urllib.parse
import webbrowser
import time

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("APIキーが設定されていません。.streamlit/secrets.toml")

def crop_target_generated_area(img):
    w, h = img.size
    
    # left = int(w * 0.08)
    # right = int(w * 0.18)
    # top = int(h * 0.64)
    # bottom = int(h * 0.67)

    # left = int(w * 0.08)
    # right = int(w * 0.18)
    # top = int(h * 0.50)
    # bottom = int(h * 0.53)
    # 0.14間隔

    left = int(w * 0)
    right = int(w * 1)
    top = int(h * 0)
    bottom = int(h * 1)

    box = (max(0, left), max(0, top), min(w, right), min(h, bottom))
    return img.crop(box)

def extract_generated_with_ai(cropped_img):
    model = genai.GenerativeModel('gemini-3.5-flash')
    
    prompt = (
        "この画像はあるゲームのプレイヤー名が表示されている領域です。"
        "プレイヤー名を正確に読み取り、"
        "余分な説明や記号を一切含めず、**プレイヤー名のテキスト文字列だけ**を1行に1人ずつの改行で返してください。"
    )
    
    try:
        start_time = time.time()
        response = model.generate_content([prompt, cropped_img])
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

def open_partial_match_page(targets):
    encoded = urllib.parse.quote(targets)
    url = f"https://uniteapi.dev/jp/search?q={encoded}"
    webbrowser.open(url)

st.title("UniteAPI")

uploaded = st.file_uploader("フル画像をアップロードしてください", type=["png", "jpg", "jpeg"])

if uploaded:
    img = Image.open(uploaded)
    
    cropped = crop_target_generated_area(img)
    
    with st.spinner("なるほどなるほど..."):
        targets = extract_generated_with_ai(cropped)
    
    st.write("解析終了:", targets if targets else "こんなの…データにないぞ…")

    st.image(cropped)

    if targets:
        for name in targets:
            open_partial_match_page(name)