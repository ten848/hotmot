import sqlite3
import pandas as pd

DB_PATH = "C:/unitexyz/roles/pokemon_datas.db"

def get_conn():
    return sqlite3.connect(DB_PATH)   # DB に接続して Connection オブジェクトを返す

def read_table(table_name: str):
    conn = get_conn()                 # DB 接続
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)  # テーブルを DataFrame として読み込む
    conn.close()                      # 接続を閉じる
    return df                         # DataFrame を返す

def update_checked(name: str, value: int):
    conn = get_conn()                 # DB 接続
    cursor = conn.cursor()            # SQL を実行するための Cursor オブジェクトを作成
    cursor.execute(
        "UPDATE pokemon SET is_checked = ? WHERE name = ?",  # SQL 文
        (value, name)                                        # プレースホルダに渡す値
    )
    conn.commit()                     # 変更を確定する（トランザクション終了）
    conn.close()                      # 接続を閉じる
