import numpy as np
import streamlit as st

from pages.helper import db_queries, match_algo, train_model


def case_viewer(case_id: str, submitted_case_id: str) -> None:
    case_details = db_queries.get_case_details(case_id)[0]

    data_col, image_col = st.columns(2)

    for text, value in zip(
        ["Name", "Mobile", "Age", "Last Seen", "Birth marks"], case_details
    ):
        data_col.write(f"{text}: {value}")

    result = db_queries.change_found_status(matched_id, submitted_case_id)
    if result["status"]:
        st.success(
            "Status Changed. Next time it will be only visible in confirmed cases page"
        )
    image_col.image(
        "./resources/" + case_id + ".jpg",
        width=80,
        use_column_width="never",
    )


if st.session_state["login_status"]:
    user = st.session_state.user

    st.title("View Submitted Cases")

    col1, col2 = st.columns(2)

    refresh_model_bt = col1.button("Refresh Model")
    check_for_match_bt = col2.button("Check for Match")
    st.write("---")

    if refresh_model_bt:
        with st.spinner("Fetching Data and Training Model..."):
            result = train_model.train(user)

        if not result["status"]:
            st.warning(result["message"])
        else:
            st.success("Training Done")

    matched_ids = {"status": False}

    if check_for_match_bt:
        with st.spinner():
            matched_ids = match_algo.match()

    if matched_ids["status"]:
        for matched_id, submitted_case_id in matched_ids["result"].items():
            case_viewer(matched_id, submitted_case_id)

        st.write("---")

    train_model.train(user)

else:
    st.write("You don't have access to this page")
