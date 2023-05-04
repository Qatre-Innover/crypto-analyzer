import streamlit as st
import my_functions 

from PIL import Image

st.set_page_config(layout="wide", page_title="About Us")
my_functions.add_logo()


st.markdown("# About Us")
st.markdown("""
<p style="font-size:20px;">
Hello, We are a team of aspiring data analysts with a passion for analyzing data and deriving 
meaningful insights. We are curious individuals who enjoy learning and exploring new approaches to data analysis. 
<br><br>
Our belief is that data analysis can help businesses make informed decisions.
We are further looking forward to collaborating with other professionals and utilizing our skills to 
make a positive impact. Oh, and don't forget about our CRYPTOSAUR 🦖 .
</p>
""", unsafe_allow_html=True)

st.markdown("""
<h4>Reach Out to Us!</h4>
""", unsafe_allow_html=True)

male = Image.open("male.jpg")
female = Image.open("female.jpg")

col1, col2 = st.columns(2)

with col1:
    st.image(male, use_column_width="auto")

    st.markdown("""
    <p style="font-size:20px; text-align:center;"> <strong>Eshaan Saraf</strong>
    <br>
    <a href="mailto:eshaan428@gmail.com"><i>eshaan428@gmail.com</i></a>
    </p>
    """, unsafe_allow_html=True)

with col2:
    st.image(female, use_column_width="auto")
    st.markdown("""
    <p style="font-size:20px; text-align:center;"> <strong>Snehal Pradhan</strong>
    <br>
    <a href="mailto:snehalpradhan11@gmail.com"><i>snehalpradhan11@gmail.com</i></a>
    </p>
    """, unsafe_allow_html=True)