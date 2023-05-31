import uuid

import PIL
import numpy as np
import streamlit as st
import re

from face_encoding import FaceEncoding
from pages.helper import db_queries
from pages.helper.data_models import UserSubmission


st.set_page_config("Mobile UI")
face_encoding_obj = FaceEncoding("./face_encoding/models")


def get_face_encoding(image: np.array):
    try:
        embedding = face_encoding_obj.predict(image)
        st.success("Keypoints generated")
        return embedding
    except IndexError:
        st.error("Couldn't find keypoints in image. Please try another image")
    except Exception:
        st.error("Unknown error occured. Please check with Admin")


def image_obj_to_numpy(image_obj):
    image = PIL.Image.open(image_obj)
    img_array = np.array(image)
    return img_array

def validate_mobile_number(mobile_number):
    # Regular expression pattern for Indian mobile numbers
    pattern = r"^[6-9]\d{9}$"
    return re.match(pattern, mobile_number) is not None


st.title("Make a submission")


image_col, form_col = st.columns(2)
image_obj = None
save_flag = 0

with image_col:

    image_obj = st.file_uploader("Image", type=["jpg", "jpeg", "png"])
    if image_obj:
        with st.spinner("Processing..."):

            unique_id = str(uuid.uuid4())
            uploaded_file_path = "./resources/" + unique_id + ".jpg"

            with open(uploaded_file_path, "wb") as output_temporary_file:
                output_temporary_file.write(image_obj.read())
            st.image(image_obj, width=200)
            image_numpy = image_obj_to_numpy(image_obj)
            face_embedding = get_face_encoding(image_numpy)

if image_obj:
    with form_col.form(key="new_user_submission"):
        name = st.text_input("Name *")
        mobile_number = st.text_input("Mobile Number *")
        address = st.text_input("Address/Location *")
        birth_marks = st.text_input("Birth Marks")

        submit_bt = st.form_submit_button("Submit")
        
        # Validate mobile number
        if mobile_number and not validate_mobile_number(mobile_number):
            st.warning("Invalid mobile number. Please enter a valid Indian mobile number.")
            
        if submit_bt:
            if not name or not mobile_number or not address:
                st.warning("Please fill in all the required fields.")

        user_submission_details = UserSubmission(
            name=name,
            address=address,
            face_encoding=face_embedding,
            id=unique_id,
            mobile=mobile_number,
            birth_marks=birth_marks,
        )

        if submit_bt:
            result = db_queries.make_user_submission(user_submission_details)

            if result["status"]:
                save_flag = 1

    if save_flag == 1:
        st.success("Successfully Submitted")
