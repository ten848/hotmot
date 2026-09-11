from google import genai
from PIL import Image
import urllib.parse
import webbrowser

# クライアントの初期化
# ※事前に環境変数などに GEMINI_API_KEY が設定されている必要があります
client = genai.Client()


def extract_generated_with_ai(cropped_img):
  prompt = (
      "この画像はあるゲームのプレイヤー名が表示されている領域です。"
      "プレイヤー名を正確に読み取り、"
      "余分な説明や記号を一切含めず、**プレイヤー名のテキスト文字列だけ**を1行に1人ずつの改行で返してください。"
  )

  try:
    # 最新の google-genai SDK を使ったリクエスト
    response = client.models.generate_content(
        model="gemini-3.5-flash", contents=[prompt, cropped_img]
    )

    generated = response.text.strip()
    generated = generated.replace("`", "").strip()
    # 改行ごとに分割してリストにする
    targets = [line.strip() for line in generated.splitlines() if line.strip()]
    return targets

  except Exception as e:
    st.error(f"Error: {e}")
    return None


def open_partial_match_page(target_name):
  # 1人分の名前をURLエンコードして開く
  encoded = urllib.parse.quote(target_name)
  url = f"https://uniteapi.dev/jp/search?q={encoded}"
  webbrowser.open(url)


# --- Streamlit 画面レイアウト ---
st.title("ゲームプレイヤー名 検索ツール")

# ファイルアップロード欄
uploaded = st.file_uploader(
    "フル画像をアップロードしてください", type=["png", "jpg", "jpeg"]
)

if uploaded:
  # アップロードされた画像を読み込み
  img = Image.open(uploaded)

  # 領域の切り出し処理（※ crop_target_generated_area関数が定義されている前提です）
  try:
    cropped = crop_target_generated_area(img)
  except NameError:
    # 関数が未定義の場合はそのまま全体を使用（テスト用）
    cropped = img

  # 切り抜いた画像を表示
  st.image(cropped, caption="抽出対象エリア", use_container_width=True)

  # AIによる解析
  with st.spinner("AIがプレイヤー名を解析中..."):
    targets = extract_generated_with_ai(cropped)

  # 結果の表示と検索処理
  if targets:
    st.success(f"解析終了: {len(targets)}人のプレイヤーを検出しました！")
    st.write(targets)

    # ユーザーが意図したタイミングで開けるようにボタンを設置
    if st.button("検出された全員分の検索ページをブラウザで開く"):
      for name in targets:
        open_partial_match_page(name)
  else:
    st.warning("こんなの…データにないぞ…（プレイヤー名が取得できませんでした）")