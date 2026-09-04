import os
import streamlit.components.v1 as components

component_dir = os.path.join(os.path.dirname(__file__), "frontend")

simple_component = components.declare_component(
    "simple_component",
    path=component_dir
)

def get_event():
    return simple_component()

