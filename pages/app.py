import streamlit as st
import os
from supabase import create_client

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_url():
    res = supabase.table("record").select("*").not_.is_("url", "null").execute()
    return res.data

def add_record(player_name, url):
    data = {"player_name": player_name, "url": url}
    res = supabase.table("record").insert(data).execute()
    return res.data

def delete_record(record_id):
    supabase.table("record").delete().eq("id", record_id).execute()

def delete_record(record_all_id):
    supabase.table("record").delete().eq("id", record_all_id).execute()

player_name = st.text_input("プレイヤー名")
url = st.text_input("URL")

if st.button("保存"):
    if player_name and url:
        add_record(player_name, url)
    else:
        st.error("era-")

st.subheader("保存済み一覧")

url_dt = load_url()
for r in url_dt:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(f"**{r['player_name']}** → {r['url']}")
    with col2:
        if st.button("削除", key=f"del_{r['id']}"):
            delete_record(r["id"])
            st.rerun()

if st.button("全削除", key=f"del_all_{['id']}"):
    # urlが NULL（None）ではないレコードを一括で削除する
    supabase.table("record").delete().not_.is_("url", "null").execute()
    st.rerun()