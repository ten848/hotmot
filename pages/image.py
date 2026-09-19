import streamlit as st
import time
import urllib.parse
# import webbrowser
from google import generativeai as genai
from PIL import Image
from supabase import create_client

#region unitexyz
theme = st.get_option("theme.base")
color = "black" if theme == "dark" else "white"

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

def add_record(player_name, url, type):
    data = {"player_name": player_name, "url": url, "type":type}
    res = supabase.table("record").insert(data).execute()
    return res.data

uploaded = st.file_uploader("データ、とらせてもらうよ。",type=["png", "jpg", "jpeg"])

if uploaded:
  img = Image.open(uploaded)

  cropped = crop_target_generated_area(img)

  with st.spinner("なるほどなるほど..."):
    targets = extract_generated(cropped)

  st.write("解析終了:"
    # , targets if targets else "こんなの…データにないぞ…"
    )

  supabase.table("record").delete().not_.is_("url", "null").execute()

  for i, player_name in enumerate(targets):
      encoded = urllib.parse.quote(player_name)
      url = f"https://uniteapi.dev/jp/search?q={encoded}"

      type = 1 if i < 5 else 2

      if player_name and url and type:
        add_record(player_name, url, type)


def load_url():
    res = supabase.table("record").select("*").not_.is_("url", "null").execute()
    return res.data

url_dt = load_url()
col1, col2 = st.columns(2)
for row in url_dt:
    name = row.get("player_name")
    url = row.get("url")
    type = row.get("type")
    
    if type == "1":
        col1.markdown(f"- [{name}]({url})", unsafe_allow_html=True)
    elif type == "2":
        col2.markdown(f"- [{name}]({url})", unsafe_allow_html=True)
