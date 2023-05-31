import uuid
import numpy as np
import streamlit as st
import PIL
import base64
import pathlib
import re

from face_encoding import FaceEncoding
from pages.helper.data_models import NewCaseDetails
from pages.helper import db_queries


st.set_page_config(page_title="Case New Form")


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


def image_to_base64(image):
    return base64.b64encode(image).decode("utf-8")

def validate_mobile_number(mobile_number):
    # Regular expression pattern for Indian mobile numbers
    pattern = r"^[6-9]\d{9}$"
    return re.match(pattern, mobile_number) is not None


def validate_aadhaar_number(aadhaar_number):
    # Regular expression pattern for Aadhaar card numbers
    pattern = r"^\d{12}$"
    return re.match(pattern, aadhaar_number) is not None



if st.session_state["login_status"]:
    user = st.session_state.user

    st.title("Register New Case")

    with st.spinner("Loading..."):
        face_encoding_obj = FaceEncoding("./face_encoding/models")

    image_col, form_col = st.columns(2)
    image_obj = None
    save_flag = 0

    with image_col:

        image_obj = st.file_uploader("Image", type=["jpg", "jpeg", "png"])

        if image_obj:
            unique_id = str(uuid.uuid4())
            uploaded_file_path = "./resources/" + unique_id + ".jpg"
            with open(uploaded_file_path, "wb") as output_temporary_file:
                output_temporary_file.write(image_obj.read())

            with st.spinner("Processing..."):
                st.image(image_obj)
                image_numpy = image_obj_to_numpy(image_obj)
                face_embedding = get_face_encoding(image_numpy)

    if image_obj:
        with form_col.form(key="new_case"):
            name = st.text_input("Name *")
            fathers_name = st.text_input("Father's Name *")
            age = st.number_input("Age", min_value=3, max_value=100, value=10, step=1)
            mobile_number = st.text_input("Mobile Number *")
            address = st.text_input("Address *")
            adhaar_card = st.text_input("Adhaar Card")
            birthmarks = st.text_input("Birth Mark")
            last_seen = st.text_input("Last Seen *")
            description = st.text_area("Description (optional)")
            
            complainant_name = st.text_input("Complainant Name")
            complainant_phone = st.text_input("Complainant Phone")

            submit_bt = st.form_submit_button("Save")
            
            # Validate mobile number
            if mobile_number and not validate_mobile_number(mobile_number):
                st.warning("Invalid mobile number. Please enter a valid Indian mobile number.")

            # Validate Aadhaar card number if provided
            if adhaar_card and not validate_aadhaar_number(adhaar_card):
                st.warning("Invalid Aadhaar card number. Please enter a valid 12-digit number.")
                
            if submit_bt:
                if not name or not fathers_name or not age or not mobile_number or not address or not last_seen:
                    st.warning("Please fill in all the required fields.")
                else:
                    # Process the form submission
                    new_case_details = NewCaseDetails(
                        id=unique_id,
                        name=name,
                        fathers_name=fathers_name,
                        age=age,
                        mobile_number=mobile_number,
                        description=description,
                        face_embedding=face_embedding,
                        submitted_by=user,
                        birth_marks=birthmarks,
                        adhaar_card=adhaar_card,
                        address=address,
                        last_seen=last_seen,
                        complainant_name=complainant_name,
                        complainant_mobile=complainant_phone,
                    )
                    db_queries.save_new_case(new_case_details)
                    save_flag = 1

        if save_flag:
            st.success("Case Registered")

else:
    st.write("You don't have access to this page")

            

