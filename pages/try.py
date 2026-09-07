import streamlit as st
import time


@st.fragment(run_every=1)  # 5秒ごとにこの中だけが自動再実行される
def live_data():
  st.write(
      "現在の時刻:", time.strftime("%H:%M:%S")
  )  # 5秒ごとに時刻が更新される


live_data()
st.write(st.time_input(label = "a"))