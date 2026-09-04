import streamlit as st
st.markdown(
    """
    <style>
    .parent-container {
        position: relative; /* 基準となる親要素 */
        background-color: black;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 20px;
        margin-top: 15px;
    }
    .absolute-badge {
        position: absolute; /* 絶対配置の指定 */
        top: -10px;         /* 親要素の上の枠線に少し重ねる */
        right: 15px;        /* 右端から15pxの距離 */
        background-color: #ef4444;
        color: white;
        padding: 2px 8px;
        font-size: 12px;
        border-radius: 4px;
    }
    </style>
    
    <div class="parent-container">
        <div class="absolute-badge">NEW</div>
        ボックスの中身のテキストです。絶対配置を使うと、このようにパーツを自由な位置に重ねることができます。
    </div>
    """,
    unsafe_allow_html=True
)

import streamlit as st
 
st.markdown(
    """
    <style>
    .custom-button button {
        background: linear-gradient(135deg, #005bbb, #00bcd4);
        color: white;
        border: 0;
        padding: 0.6rem 1.5rem;
        border-radius: 999px;
        transition: transform 0.1s ease-in-out;
    }
    .custom-button button:hover {
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
 
with st.container():
    st.markdown('<div class="custom-button">', unsafe_allow_html=True)
    st.button("グラデーションボタン", key="custom")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* Streamlitのボタン要素を直接指定する例 */
    div.stButton > button {
        height: 10rem !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.button(f"レーン", key=f"button_{0}"):
  st.session_state["waiting"] = [0] * 6
  st.session_state["waiting"][0] = 1
  st.rerun()

if st.button("alpha"):
   st.toast("ypaa")