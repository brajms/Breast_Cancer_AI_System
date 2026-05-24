import streamlit as st

from streamlit_option_menu import option_menu

from modules.home import show_home
from modules.prediction import show_prediction
from modules.dashboard import show_dashboard

# PAGE CONFIG

st.set_page_config(

    page_title="Smart Cancer AI",

    page_icon="🧬",

    layout="wide"
)

# LOAD CSS

def load_css():

    with open("assets/style.css") as f:

        st.markdown(

            f"<style>{f.read()}</style>",

            unsafe_allow_html=True
        )

load_css()

# SIDEBAR

with st.sidebar:

    st.image(

        "https://cdn-icons-png.flaticon.com/512/2785/2785482.png",

        width=120
    )

    selected = option_menu(

        "Navigation",

        [

            "Home",
            "Prediction",
            "Dashboard"

        ],

        icons=[

            "house",

            "activity",

            "bar-chart"

        ],

        default_index=0
    )

# NAVIGATION

if selected == "Home":

    show_home()

elif selected == "Prediction":

    show_prediction()

elif selected == "Dashboard":

    show_dashboard()