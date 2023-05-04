# python -m streamlit run Welcome.py
import streamlit as st
import my_functions

st.set_page_config(layout="wide", page_title="Cryptosaur")
my_functions.add_logo()

st.markdown("""<h1 style='text-align: center; font-family: cursive;'>
            Hey, You! It's Me, 
            <span style="color:#ff0066; margin: 0px 0px 0px -10px;">C</span>
            <span style="color:#ffcc00; margin: 0px 0px 0px -10px;">R</span>
            <span style="color:#00ffff; margin: 0px 0px 0px -10px;">Y</span>
            <span style="color:#6600ff; margin: 0px 0px 0px -10px;">P</span>
            <span style="color:#33cc33; margin: 0px 0px 0px -10px;">T</span>
            <span style="color:#663300; margin: 0px 0px 0px -10px;">O</span>
            <span style="color:#000066; margin: 0px 0px 0px -10px;">S</span>
            <span style="color:#ff3300; margin: 0px 0px 0px -10px;">A</span>
            <span style="color:#ffa500; margin: 0px 0px 0px -10px;">U</span>
            <span style="color:#FF0000; margin: 0px 0px 0px -10px;">R</span>
            ...</h1>""", 
    unsafe_allow_html=True)

# ------------------------------Centered Image-------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<h3 style='text-align: center; margin: 100px; font-family: cursive;'> GrrGrrr...Would you like to invest?</h3>", 
        unsafe_allow_html=True)
with col2:
    my_functions.get_lottie()
with col3:
    st.markdown("<h3 style='text-align: center; margin: 100px; font-family: cursive;'> I will help you pick your best crypto!</h3>",
        unsafe_allow_html=True)