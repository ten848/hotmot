import base64

# 画像をBase64文字列に変換
with open("images/UI/korokku.png", "rb") as f:
  encoded_str = base64.b64encode(f.read()).decode("utf-8")

# そのままテキストファイルとして保存する
with open("images/UI/korokku.txt", "w") as f:
  f.write(encoded_str)