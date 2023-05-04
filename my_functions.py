import streamlit as st
from streamlit_lottie import st_lottie
import plotly.io as pio
import plotly.graph_objects as go

import requests

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"]::before {
                content: "Main menu";
                font-family: "Brush Script MT", Cursive;
                margin-left: 20px;
                margin-top: 20px;
                font-size: 20px;
                font-weight: bold;
                position: relative;
                top: 80px;
            }
            .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                font-size:1.6rem; font-family: cursive;
            }
            div.css-184tjsw.p {
                font-weight: bold;
                font-size: medium;
            }
            div.css-1r6slb0.e1tzin5v2{
                margin: auto;
                color: #c22ad5;
                font-weight: bold;
            }
            div.css-1wivap2.e16fv1kl3{
                font-weight:bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def set_plotly_template():
    # Setting up the Colours
    dc_colors = ["#2B3A64", "#96aae3", "#C3681D", "#EFBD95", "#E73F74", "#80BA5A", "#E68310", "#008695", "#CF1C90", "#f97b72", "#4b4b8f", "#A5AA59"]

    # Setting up the Template
    pio.templates["dc"] = go.layout.Template(
        layout = dict(
            font = {"family": "Poppins, Sans-serif", "color": "#505050"},
            title = {"font": {"family": "Poppins, Sans-serif", "color": "black"}, "yanchor": "top", "y": 0.92, "xanchor": "left", "x": 0.025},
            plot_bgcolor = "white",
            paper_bgcolor = "white", 
            hoverlabel = dict(bgcolor = "white"),
            height = 500,
            width = 800,
            margin = dict(l = 100, r = 50, t = 75, b = 70),
            colorway = dc_colors, 
            xaxis = dict(showgrid = False), 
            yaxis = dict(showgrid = True, 
                        gridwidth = 0.1, 
                        gridcolor = "lightgrey",
                        showline = True, 
                        nticks = 10, 
                        linewidth = 1, 
                        linecolor = "black", 
                        rangemode = "tozero")
        )
    )

def get_lottie():
    url = requests.get('https://assets9.lottiefiles.com/packages/lf20_EUyLAK.json')
    url_json = dict()

    if url.status_code == 200:
        url_json = url.json()
    else:
        print("Oops! There is some error. Your animation cannot be generated at the moment.")
    st_lottie(url_json, height=400, width=350)

