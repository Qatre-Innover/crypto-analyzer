# python -m streamlit run Home.py
import streamlit as st
import numpy as np
import pandas as pd
import random

import extractor
import my_functions
import time

st.set_page_config(layout="wide", page_title="Crypto Analyzer")
my_functions.add_logo()

st.markdown("# What's in the Crypto-bank🦖")
st.markdown("""
<p style="font-size:20px;">As the world of digital assets continues to grow and evolve, it can be challenging to stay on 
top of all the changes and fluctuations. That's where our <strong style="color:green;">data analytics project</strong> comes in. 
We provide you with a powerful tool to analyze and visualize cryptocurrency data, helping you 
make informed decisions about your investments. <br><br> Our project is designed for anyone interested in the cryptocurrency market, whether you're a 
seasoned trader or just getting started. With our user-friendly interface and robust data analysis 
capabilities, you can easily explore trends, identify patterns, and gain insights into the 
performance of various cryptocurrencies.
</p> <br>
""", unsafe_allow_html=True)

c_names = pd.read_csv('names.csv')
ids = np.array(c_names.iloc[:, 1])
choice = random.choice(ids)

checked = st.checkbox("Show my bucket of currencies")
if checked:
    st.table(c_names)


st.markdown(f"""<br>
<h4 style="text-align:left;">Do you know how {choice} is trending?</h4>
""", unsafe_allow_html=True)

start, stop, data = extractor.get_data(stock=choice, days=180)

status_text = st.sidebar.empty()
chart = st.line_chart(data.iloc[0:2, 0:4])

for i in range(2, data.shape[0]-1, 2):
    new_rows = data.iloc[i:i+2, 0:4]

    # Update the status text
    status_text.text("{:.2f}% Complete!".format(i/(data.shape[0])*100))

    # Append data to the chart.
    chart.add_rows(new_rows)
    
    # Pretend we're doing some computation that takes time.
    time.sleep(0.1)

status_text.text("100.00% Complete")
st.button("Preview Next")

# --------------------------------- DATA SOURCE ---------------------------
link = "https://finance.yahoo.com/"

with st.sidebar:
    st.markdown(f"""<br><br><br><br><br><br><br><br><br>
    <h4> Data Source: <br>
    {link}
    </h4>
    """, unsafe_allow_html=True)
