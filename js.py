import streamlit as st
import cv2
import numpy as np
import tempfile

st.set_page_config(page_title="Vegil AI", page_icon="🚨")

st.title("🚨 Vegil AI - Simple Surveillance Demo")
st.write("Upload a video to detect motion (Demo Version)")

uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi"])

if uploaded_file:

    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    cap = cv2.VideoCapture(tfile.name)

    stframe = st.empty()

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    motion_detected = False

    while ret:
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )

        for contour in contours:
            if cv2.contourArea(contour) > 2000:
                motion_detected = True
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame1, (x, y),
                              (x + w, y + h),
                              (0, 0, 255), 2)

        frame_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        stframe.image(frame_rgb)

        frame1 = frame2
        ret, frame2 = cap.read()

    cap.release()

    if motion_detected:
        st.error("🚨 ALERT: Motion Detected!")
    else:
        st.success("✅ No Motion Detected")
