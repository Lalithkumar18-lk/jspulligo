import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile

st.set_page_config(page_title="Vegil AI", page_icon="🚨")

st.title("🚨 Vegil AI - Intelligent Surveillance System")
st.write("Upload a video to detect suspicious activity (Demo Version)")

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

uploaded_file = st.file_uploader("Upload CCTV Video", type=["mp4", "avi"])

if uploaded_file:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)

    stframe = st.empty()

    threat_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                label = model.names[cls]

                # If person detected
                if label == "person":
                    threat_detected = True

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, label, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0,255,0), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        stframe.image(frame, channels="RGB")

    cap.release()

    if threat_detected:
        st.error("🚨 ALERT: Suspicious Activity Detected!")
    else:
        st.success("✅ No Threat Detected")
