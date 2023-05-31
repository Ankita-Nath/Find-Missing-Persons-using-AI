import uuid

import PIL
import numpy as np
import streamlit as st
from st_pages import show_pages, Page

from face_encoding import FaceEncoding
from pages.helper import db_queries
from pages.helper.data_models import UserSubmission

show_pages([Page("mobile_streamlit.py", "User Submission", "User Submission")])


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
            st.image(image_obj)
            image_numpy = image_obj_to_numpy(image_obj)
            face_embedding = get_face_encoding(image_numpy)

if image_obj:
    with form_col.form(key="new_user_submission"):
        name = st.text_input("Name")
        mobile_number = st.text_input("Mobile Number")
        address = st.text_input("Address/Location")
        description = st.text_area("Description (optional)")

        submit_bt = st.form_submit_button("Submit")

        user_submission_details = UserSubmission(
            name=name,
            address=address,
            face_encoding=face_embedding,
            id=unique_id,
            mobile=mobile_number,
        )

        if submit_bt:
            result = db_queries.make_user_submission(user_submission_details)

            if result["status"]:
                save_flag = 1

    if save_flag == 1:
        st.success("Successfully Submitted")
