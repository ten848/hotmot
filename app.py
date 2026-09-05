import urllib.parse
import webbrowser

names = input("プレイヤー名をスペース区切りで入力してください: ").split()

for name in names:
    encoded = urllib.parse.quote(name)
    url = f"https://uniteapi.dev/jp/search?q={encoded}"
    print(f"{name} の検索ページを開きます")
    webbrowser.open(url)