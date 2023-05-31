import tempfile
import pathlib
import uuid
import streamlit as st

unique_id = str(uuid.uuid4())


image_obj = st.file_uploader("Image", type=["jpg", "jpeg", "png"])

if image_obj:
    uploaded_file_path = str(uuid.uuid4()) + ".jpg"
    with open(uploaded_file_path, "wb") as output_temporary_file:
        output_temporary_file.write(image_obj.read())
