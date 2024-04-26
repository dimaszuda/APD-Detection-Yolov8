import os
import cv2
import ssl
from PIL import Image
import streamlit as st
from pathlib import Path
from pytube import YouTube
from ultralytics import YOLO
from corpus import SAMPLE_VIDEO
from tempfile import NamedTemporaryFile

def load_model(model_path: Path):
    model = YOLO(model_path)
    return model

def show_tracker():
    display_tracker = st.radio("Display Tracker", ("Yes", "No"))
    is_dipslay_tracker = True if display_tracker == 'Yes' else False
    if is_dipslay_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_dipslay_tracker, tracker_type
    else:
        return is_dipslay_tracker, None

def display_detected_frames(
        model,
        st_frame, 
        image, 
        width: int,
        height: int,
        is_display_tracking: bool, 
        tracker
) -> None:
    image = cv2.resize(image, (width, height))
    if is_display_tracking:
        res = model.track(image, persist=True, tracker=tracker)
    else:
        res = model.predict(image)

    res_plotted = res[0].plot()
    st_frame.image(
        res_plotted,
        caption='Detected Video',
        channels="BGR",
        use_column_width=True
    )
def show_original_image(source_img: Path) -> None:
    try:
        uploaded_image = Image.open(source_img)
        st.image(
            source_img, 
            caption="Original Image",
            use_column_width=True
        )
    except Exception as e:
        st.error(f"Error Opening Image: \n {e}")

def detect_image(upload_image: Path, model) -> None: # check if this function is worked or not
    try:
        if upload_image:
            if st.sidebar.button("Detect Objects"):
                image = Image.open(upload_image)
                results = model.predict(image)
                for i, result in enumerate(results):
                    im_bgr = result.plot()
                    im_rgb = Image.fromarray(im_bgr[..., ::-1])
                    st.image(
                        im_rgb, 
                        caption="Detected Image", 
                        use_column_width=True
                    )
                    ## add function to detect if the person is safe or not
    except Exception as e:
        st.sidebar.error(f"Unexpected Error: {e}")
    
def detect_video(video_source: str, model) -> None:
    try:
        if video_source:
            is_display_tracker, tracker = show_tracker()
            if st.button("Detect Objects"):
                video_cap = cv2.VideoCapture(
                    str(video_source)
                )
                width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                st_frame = st.empty()
                while (video_cap.isOpened()):
                    success, image = video_cap.read()
                    if success:
                        display_detected_frames(
                            model,
                            st_frame=st_frame,
                            image=image,
                            width=width,
                            height=height,
                            is_display_tracking=is_display_tracker,
                            tracker=tracker
                        )
                    else:
                        video_cap.release()
                        os.unlink(video_source)
                        break
    except Exception as e:
        st.sidebar.error(f"Error Detecting Video: {e}")

def inference_video(video_source: str, model) -> None:
    try:
        if video_source == 'Sample':
            sample_video = st.selectbox(
                "Choose a sample video", SAMPLE_VIDEO.keys()
            )
            detect_video(SAMPLE_VIDEO.get(sample_video), model)
        elif video_source == 'Local':
            upload_video = st.file_uploader("Upload your video")
            if upload_video:
                temp_video_file = NamedTemporaryFile(delete=False)
                temp_video_file.write(upload_video.read())
                video_name = temp_video_file.name
                detect_video(video_name, model)
        elif video_source == 'Youtube':
            youtube_url = st.sidebar.text_input("Input Youtube URL")
            if youtube_url:
                ssl._create_default_https_context = ssl._create_unverified_context
                youtube_video = YouTube(youtube_url)
                stream = youtube_video.streams.filter(
                    progressive=True,
                    file_extension="mp4"
                ).first().download()
                detect_video(stream, model)
                os.remove(stream)
    except Exception as e:
        st.sidebar.error(f"Error Loading Video \n {e}")