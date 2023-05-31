import base64
import io

import numpy as np
import streamlit as st
from PIL import Image

from pages.helper import db_queries


def case_viewer(case: list) -> None:
    case = list(case)
    case_id = case.pop(0)
    matched_with = case.pop(-1)
    matched_with_details = None

    try:
        matched_with = matched_with.replace("{", "").replace("}", "")
    except:
        matched_with = None

    if matched_with:
        matched_with_details = db_queries.user_submission_details(matched_with)

    data_col, image_col, matched_with_col = st.columns(3)
    for text, value in zip(["Name", "Age", "Status", "Last Seen", "Phone"], case):
        if value == 'F':
            value = 'Found'

        elif value == 'NF':
            value = 'Not Found'

        data_col.write(f"{text}: {value}")

    image_col.image(
        "./resources/" + case_id + ".jpg",
        width=120,
        use_column_width="never",
    )

    if matched_with_details:
        matched_with_col.write(f"Location: {matched_with_details[0][0]}")
        matched_with_col.write(f"Submitted By: {matched_with_details[0][1]}")
        matched_with_col.write(f"Mobile: {matched_with_details[0][2]}")
        matched_with_col.write(f"Birth Marks: {matched_with_details[0][3]}")

    st.write("---")


if st.session_state["login_status"]:
    user = st.session_state.user

    st.title("View Submitted Cases")

    status_col, date_col = st.columns(2)
    status = status_col.selectbox(
        "Filter", options=["All", "Not Found", "Found", "Closed"]
    )
    date = date_col.date_input("Date")

    cases_count, cases_data = db_queries.fetch_submitted_cases(user, status)

    st.write("\n\n")
    st.write("---")
    for case in cases_data:
        case_viewer(case)

else:
    st.write("You don't have access to this page")
