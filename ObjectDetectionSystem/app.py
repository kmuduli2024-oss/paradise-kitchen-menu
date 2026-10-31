import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2

# Load YOLOv8 pre-trained model
model = YOLO("yolov8n.pt")

# Page configuration
st.set_page_config(
    page_title="YOLOv8 Object Detection",
    layout="wide"
)

st.title("🎯 Real-Time Object Detection using YOLOv8")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Image Detection", "Webcam Detection"]
)

# IMAGE DETECTION

if mode == "Image Detection":

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")


        st.image(
            image,
            caption="Uploaded Image",
            use_container_width=True
        )

        img_array = np.array(image)

        results = model(img_array)

        output = results[0].plot()

        st.image(
            output,
            caption="Detection Result",
            use_container_width=True
        )

        st.subheader("Detected Objects")

        for box in results[0].boxes:

            cls = int(box.cls)
            conf = float(box.conf)

            label = model.names[cls]

            st.write(f"{label} : {conf:.2f}")

# WEBCAM DETECTION

if mode == "Webcam Detection":

    run = st.checkbox("Start Webcam")

    frame_window = st.image([])

    cap = cv2.VideoCapture(0)

    while run:

        success, frame = cap.read()

        if not success:
            st.error("Cannot access webcam")
            break

        results = model(frame)

        frame = results[0].plot()

        frame_window.image(
            frame,
            channels="BGR",
            use_container_width=True
        )

    cap.release()