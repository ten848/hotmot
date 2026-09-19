import streamlit as st
import time


@st.fragment(run_every=1)  # 5秒ごとにこの中だけが自動再実行される
def live_data():
  st.write(
      "現在の時刻:", time.strftime("%H:%M:%S")
  )  # 5秒ごとに時刻が更新される


live_data()
st.write(st.time_input(label = "a"))

selected_label = st.pills(
    "",
    options=["上", "中央", "下"],
    default="中央",
    key=f"select",
    label_visibility="collapsed"
)

# horizontal=True にすることで、縦並びから横並びにできます
select_label = st.radio(
    "",
    options=["上", "中央", "下"],
    index=1,
    key=f"select_",
    label_visibility="collapsed",
    horizontal=True
)
theta = "no"
pi = st.selectbox("",options=["","上", "中央", "下"],key = "A")
if pi:
  theta = pi
st.write(theta)

A = []
label = st.pills(
    "",
    options=[1, 2, 3],
    default="中央",
    key=f"select",
    label_visibility="collapsed"
)

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

st.write("KEY is None:", st.secrets.get("SUPABASE_KEY") is None)
st.write("URL:", st.secrets["SUPABASE_URL"])



