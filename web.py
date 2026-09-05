import urllib.parse
import requests
import re
import webbrowser

# ★ 実行時に cf_clearance を入力する
cf_clearance = input("cf_clearance を貼り付けてください: ").strip()

cookies = {
    "cf_clearance": cf_clearance
}

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/116.0.0.0 Safari/537.36"
    )
}

def get_top_player_id(name):
    encoded = urllib.parse.quote(name)
    search_url = f"https://uniteapi.dev/jp/search?q={encoded}"

    html = requests.get(search_url, headers=headers, cookies=cookies).text

    ids = re.findall(r"/jp/p/(\d+)", html)
    if ids:
        return ids[0]
    return None

def open_player_page(pid):
    url = f"https://uniteapi.dev/jp/p/{pid}"
    webbrowser.open(url)

names = input("プレイヤー名をスペース区切りで入力してください: ").split()

for name in names:
    pid = get_top_player_id(name)
    if pid:
        print(f"{name} → {pid} を開きます")
        open_player_page(pid)
    else:
        print(f"{name} の候補が見つかりませんでした")
