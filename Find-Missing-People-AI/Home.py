import yaml
import base64
import streamlit as st
from yaml import SafeLoader
import streamlit_authenticator as stauth


from pages.helper import db_queries


import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


add_bg_from_local("background.jpg")


if "login_status" not in st.session_state:
    st.session_state["login_status"] = False

with open("login_config.yml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status:
    authenticator.logout("Logout", "sidebar")

    st.session_state["login_status"] = True
    
    add_bg_from_local("background.jpg")
    
    user_info = config["credentials"]["usernames"][username]
    st.session_state["user"] = user_info["name"]

    st.write(
            f'<p style="color:white; textAlign:left; fontSize :45px">{user_info["name"]}</p>',
            unsafe_allow_html=True,
        )

    st.write(
            f'<p style="color:white; textAlign:left; fontSize :20px">{user_info["area"]}, {user_info["city"]}</p>',
            unsafe_allow_html=True,
        )

    st.write(
            f'<p style="color:white; textAlign:left; fontSize :20px">{user_info["role"]}</p>',
            unsafe_allow_html=True,
        )

    st.write("---")

    found_cases = db_queries.get_confirmed_cases(user_info["name"])
    non_found_cases = db_queries.get_not_confirmed_cases(user_info["name"])
    frequent_location = db_queries.get_last_seen_areas(user_info["name"])

    found_cases_count = len(found_cases)
    not_found_cases_count = len(non_found_cases)

    found_col, not_found_col = st.columns(2)

    found_col.metric("Found Cases Count", value=found_cases_count)
    not_found_col.metric("Not Found Cases Count", value=not_found_cases_count)

elif authentication_status == False:
    st.error("Username/password is incorrect")
elif authentication_status == None:
    if st.session_state.get("login_status") is None and (not (name or username) or not st.form_submit_button("Submit")):
        st.warning("Please enter your username and password")
        st.session_state["login_status"] = False
