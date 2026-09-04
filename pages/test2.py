import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
import pandas as pd
from db import read_table
import os
from streamlit_keypress import key_press_events

if "coords" not in st.session_state:
    st.session_state["coords"] = [None,None,None,None,None,None,None,None,None,None]

event = key_press_events()

img_path = f"images/pokemon/altaria.png"
if os.path.exists(img_path):
    st.session_state["coords"][9] = streamlit_image_coordinates(img_path, key ="pokemon51", width = 85)

if st.session_state["coords"][9] is not None:
            st.session_state["selected_player"] = 4

st.write(st.session_state["coords"])
st.write(current_id)
st.write(event)