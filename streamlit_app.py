# Python In-built packages
from pathlib import Path
import PIL
# External packages
import streamlit as st
# Local Modules
#import settings
#import helper
# Setting page layout
st.set_page_config(
    page_title="Grupo 28",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Main page heading
st.title("Proyecto grupo 28")
# Sidebar
st.sidebar.header("Dashboard")
# Model type
# Load Pre-trained ML Model
st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", "lista")