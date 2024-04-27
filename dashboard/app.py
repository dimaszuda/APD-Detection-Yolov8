import handler
import streamlit as st
from PIL import Image
from corpus import (
    MODEL_PATH,
    VIDEO_SOURCE,
    FILE_TYPE,
    IMAGE_TYPE,
    CONFIDENCE_THRESHOLD
)


st.set_page_config(
    page_title="APD Detection",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("APD Detection using Yolov8")
st.sidebar.header("File Type")
file_type = st.sidebar.radio(
    "Choose the file type", FILE_TYPE
)
try:
    model = handler.load_model(MODEL_PATH)
except Exception as e:
    st.sidebar.error(f"Error Loading AI Model: {e}")

if file_type == "Image":
    source_img_placeholder = st.empty()
    source_img = st.sidebar.file_uploader("Choose an image", type=IMAGE_TYPE)
    if source_img:
        col1, col2 = st.columns(2)
        with col1:
            handler.show_original_image(source_img)
        with col2:
            handler.detect_image(source_img,CONFIDENCE_THRESHOLD, model)
elif file_type == 'Video':
    with st.sidebar.expander("Video Source"):
        video_source = st.sidebar.radio(
            "Select Video Source:", VIDEO_SOURCE
        )
    handler.inference_video(video_source, CONFIDENCE_THRESHOLD, model)
        