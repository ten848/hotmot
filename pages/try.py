import streamlit as st
from streamlit_keypress import key_press_events
from streamlit_image_coordinates import streamlit_image_coordinates

if "active_target" not in st.session_state:
    st.session_state["active_target"] = None

if "inputs" not in st.session_state:
    st.session_state["inputs"] = [""] * 11

if "last_event" not in st.session_state:
    st.session_state["last_event"] = None

events = key_press_events()

if events and st.session_state["active_target"] is not None:
    key_name = events.get("key") if isinstance(events, dict) else str(events)
    
    if key_name and events != st.session_state["last_event"]:
        st.session_state["last_event"] = events
        st.session_state["inputs"][st.session_state["active_target"]] = key_name
        st.session_state["active_target"] = None
        st.rerun()

cols = st.columns(5)
for i in range(10):
    with cols[i % 5]:
        if st.button(f"ボタン {i}", key=f"btn_{i}"):
            st.session_state["active_target"] = i
            st.session_state["last_event"] = events
            st.rerun()

# if st.session_state["active_target"] is not None:
#     st.warning(f"現在の入力対象: 入力欄 {st.session_state['active_target']}")
# else:
#     st.info("待機中")

for i in range(10):
    if f"input_{i}" not in st.session_state:
        st.session_state[f"input_{i}"] = st.session_state["inputs"][i]

    if st.session_state[f"input_{i}"] != st.session_state["inputs"][i]:
        st.session_state[f"input_{i}"] = st.session_state["inputs"][i]

    st.text_input(f"入力欄 {i}", key=f"input_{i}")
