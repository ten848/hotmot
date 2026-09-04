# import streamlit as st
# from PIL import Image
# from streamlit_image_coordinates import streamlit_image_coordinates
# import copy

# st.set_page_config(layout="wide")

# object_states = {
#     "image_a": {"visible": True, "x": 335, "y": 190, "w": 30, "h": 30},
#     "image_b": {"visible": True, "x": 200, "y": 100, "w": 30, "h": 30},
#     "image_c": {"visible": True, "x": 400, "y": 200, "w": 30, "h": 30},
#     "image_d": {"visible": False, "x": 400, "y": 200, "w": 30, "h": 30},
#     }

# if "object_states" not in st.session_state:
#     st.session_state.object_states = copy.deepcopy(object_states)

# canvas = Image.open("images/UI/unite_map.png").convert("RGBA")
# canvas = canvas.resize((700, 452))

# objects = {
#     "image_a": Image.open("images/pokemon/altaria.png").convert("RGBA"),
#     "image_b": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
#     "image_c": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
#     "image_d": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
# }

# canvas_img = canvas.copy()
# for name, info in st.session_state.object_states.items():
#     if info["visible"]:
#         img = objects[name]
#         img = img.resize((info["w"], info["h"]))
#         canvas_img.paste(img, (info["x"], info["y"]), img)


# #if "reset_count" not in st.session_state:
# #    st.session_state.reset_count = 0

# coords = streamlit_image_coordinates(canvas_img, width=1100, key="canvas")

# if coords is not None:
#     rate = canvas_img.width / 1100 #縮小率
#     cx = coords["x"] * rate
#     cy = coords["y"] * rate

#     for name, info in st.session_state.object_states.items():
#         if info["visible"]:
#             img = objects[name]
#             w, h = info["w"], info["h"]
#             x, y = info["x"], info["y"]

#             if x <= cx <= x + w and y <= cy <= y + h:
#                 st.session_state.object_states[name]["visible"] = False
#                 st.success(f"{name} クリック済み")
#                 st.rerun()

# coords = streamlit_image_coordinates("images/UI/unite_start.png", key="img_click" , width = 300)
# if coords is not None:
#    st.session_state.object_states = copy.deepcopy(object_states)
# #   x, y, w, z = (0, 0, 0, 0)
#    if "canvas" in st.session_state:
#          del st.session_state["canvas"]
#    st.rerun()

import copy
from PIL import Image
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(layout="wide")

object_states = {
    "image_a": {"visible": True, "x": 335, "y": 60, "w": 30, "h": 30},
    "image_b": {"visible": True, "x": 335, "y": 190, "w": 30, "h": 30},
    "image_c": {"visible": True, "x": 335, "y": 330, "w": 30, "h": 30},
    "image_d": {"visible": False, "x": 400, "y": 200, "w": 30, "h": 30},
}

if "object_states" not in st.session_state:
  st.session_state.object_states = copy.deepcopy(object_states)

if "reset_count" not in st.session_state:
  st.session_state.reset_count = 0

canvas = Image.open("images/UI/unite_map.png").convert("RGBA")
canvas = canvas.resize((700, 452))

objects = {
    "image_a": Image.open("images/pokemon/altaria.png").convert("RGBA"),
    "image_b": Image.open("images/pokemon/altaria.png").convert("RGBA"),
    "image_c": Image.open("images/pokemon/altaria.png").convert("RGBA"),
    "image_d": Image.open("images/pokemon/pikachuu.png").convert("RGBA"),
}

canvas_img = canvas.copy()
for name, info in st.session_state.object_states.items():
  if info["visible"]:
    img = objects[name]
    img = img.resize((info["w"], info["h"]))
    canvas_img.paste(img, (info["x"], info["y"]), img)

coords = streamlit_image_coordinates(
  canvas_img, width=1100, key=f"canvas_{st.session_state.reset_count}"
  )

if coords is not None:
  rate = canvas_img.width / 1100  # 拡大率
  cx = coords["x"] * rate
  cy = coords["y"] * rate

  for name, info in st.session_state.object_states.items():
    if info["visible"]:
      img = objects[name]
      w, h = info["w"], info["h"]
      x, y = info["x"], info["y"]

      if x <= cx <= x + w and y <= cy <= y + h:
        st.session_state.object_states[name]["visible"] = False
        st.success(f"{name} クリック済み")
        st.rerun()

coords_reset = streamlit_image_coordinates(
    "images/UI/unite_start.png", key=f"img_click_{st.session_state.reset_count}", width=300
)

if coords_reset is not None:
  st.session_state.object_states = copy.deepcopy(object_states)
  st.session_state.reset_count += 1
  st.rerun()

if "count" not in st.session_state:
    st.session_state.count = 0

st.write("count:", st.session_state.count)

if st.button("増やす"):
    st.session_state.count += 1