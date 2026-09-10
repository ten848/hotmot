import time
import urllib.parse
import webbrowser
from google import generativeai as genai
from PIL import Image
import streamlit as st

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


def extract_generated_with_ai(cropped_img):
  model = genai.GenerativeModel("gemini-3.5-flash-lite")

  img_to_send = cropped_img.copy()
  img_to_send.thumbnail(
      (1000, 1000), Image.Resampling.LANCZOS
  )

  prompt = (
      "画像内のプレイヤー名だけを1行につき1つ返して。"
    #   このゲーム画面の画像からプレイヤー名を正確に読み取り、
    #   余分な説明や記号を一切含めず、
    #   プレイヤー名のテキスト文字列だけを1行に1人ずつの改行で返してください。
    #   みつからなければなにも返さないで。
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


def open_partial_match_page(target_name):
  encoded = urllib.parse.quote(target_name)
  url = f"https://uniteapi.dev/jp/search?q={encoded}"

  webbrowser.open(url)

# st.write(
#     "<span style='color: white; font-size: 40px'><br>&emsp;&emsp;データ、とらせてもらうよ。</span>",
#     unsafe_allow_html=True,
# )
uploaded = st.file_uploader("データ、とらせてもらうよ。",type=["png", "jpg", "jpeg"])

if uploaded:
  img = Image.open(uploaded)

  cropped = crop_target_generated_area(img)

  with st.spinner("なるほどなるほど..."):
    targets = extract_generated_with_ai(cropped)

  st.write("解析終了:"
    # , targets if targets else "こんなの…データにないぞ…"
    )

#   st.image(cropped)

  if targets:
    for name in targets:
      encoded = urllib.parse.quote(name)
      url = f"https://uniteapi.dev/jp/search?q={encoded}"
      st.markdown(f"- [{name} ]({url})", unsafe_allow_html=True)

# with open("images/UI/korokku.txt", "r") as f:
#   korokku = f.read().strip()

# st.markdown(f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/jpeg;base64,{korokku}");
#             background-size: cover;          /* 画面全体にフィットさせる */
#             background-position: center;     /* 中央寄せ */
#             background-repeat: no-repeat;    /* 繰り返さない */
#             background-attachment: fixed;    /* スクロールしても固定 */
#         }}
#         </style>
#         """,
#         unsafe_allow_html = True
#         )