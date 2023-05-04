import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statistics as sts

import my_functions
import extractor

from scipy.stats import pearsonr

st.set_page_config(layout="wide", page_title="Benchmark")
my_functions.add_logo()
my_functions.set_plotly_template()
currencies = pd.read_csv('names.csv', header=0)
currencies_codes = currencies.iloc[:, 1]

# --------------------------------- Functions --------------------------------------
def plot_graph(data):
    fig = px.line(data, 
                x = data.index,
                y = data.columns, 
                template = "dc",
                title=None
        )
    fig.update_layout(
            yaxis_title="Price ($)",
            legend_title="Category",
            height = 400,
            width = 500,
            legend=dict(
                yanchor="bottom",
                y=0.01,
                xanchor="left",
                x=0.01
            )
        )
    st.plotly_chart(fig)


def get_stats(data):
    
    mean = round(sts.mean(data[category]), 4)
    sd = round(sts.stdev(data[category]), 4)
    var = round(sts.variance(data[category]), 4)
    coeff_var = round((sd/mean)*100, 4)
        
    st.markdown(f"""
        <p style = "font-size: 18px; text-align: center;">Mean: <span style="font-weight: bold;">{mean}</span> <br>
        Standard Deviation: <span style="font-weight: bold;">{sd}</span> <br>
        Variance: <span style="font-weight: bold;">{var}</span> <br>
        Coefficient of Variation: <span style="font-weight: bold;">{coeff_var} %</span></p>
        """, unsafe_allow_html=True)
    
    return coeff_var


# ------------------------------- Comparison Section --------------------------------
st.markdown("# Get to know what's best for you...")
st.markdown("""
<p style="font-size:20px;">
Are you still doubtful about which stock is performing better? CryptoSaur can help you compare the 
performances of any two stocks side-by-side, and determine their key statistical measures and 
Variability. 
</p>
""", unsafe_allow_html=True)

option_1 = "ETH-USD"
option_2 = "DOGE-USD"
col1, col2 = st.columns(2)

# Default number of months
months = 12
optional_dates = [1, 3, 6, 9, 12, 18, 24, 36, 48, 60]
categories = ["Open", "High", "Low", "Close", "Volume"]

st.sidebar.markdown("""<h2>Select month-wise span </h2>""", unsafe_allow_html= True)
months = st.sidebar.selectbox(label="Sample", options=optional_dates, label_visibility="collapsed")

st.sidebar.markdown("""<h2>Choose Category </h2>""", unsafe_allow_html= True)
myCategories = st.sidebar.multiselect(label="Sample", options=categories, default = categories[0],
                                    label_visibility="collapsed")

with col1:
    st.markdown("""<h4 style="color:red;"> Stock 1</h4>""", unsafe_allow_html= True)
    option_1 = st.selectbox(label="Sample", options=currencies_codes, index=1,
                            label_visibility="collapsed")
    start, stop, data1 = extractor.get_data(stock=option_1, days=30*months)
    plot_graph(data1[myCategories])

with col2:
    st.markdown("""<h4 style="color:red;"> Stock 2 </h4>""", unsafe_allow_html= True)
    option_2 = st.selectbox(label="Sample", options=currencies_codes[:-1], index=5,
                            label_visibility="collapsed")
    start, stop, data2 = extractor.get_data(stock=option_2, days=30*months)
    plot_graph(data2[myCategories])


# ------------------------------ Partition -----------------------------------
st.markdown("\u2001")
st.markdown("## Summary")

color_code = {"Open": "#e6b800", "High": "#800000", "Low": "#800080", 
                "Close": "#003366", "Volume": "#006600"}

for category in myCategories:
    st.markdown(f"""<h4 
            style="color: {color_code[category]}; text-align:center;">
            -------- {category} Category ---------</h4>""", unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    with col3:
        coeff_var_1 = get_stats(data1[myCategories])
    with col4:
        coeff_var_2 = get_stats(data2[myCategories])

    if coeff_var_1>coeff_var_2:
        stable = option_2
    else:
        stable = option_1
    corr, _ = pearsonr(data1[category], data2[category])
    st.markdown(f""" <h4 style="text-align: center;">
        Trend Correlation Percentage: <span style="color:red;">{round(corr*100, 2)} %</span>
        <br>
        Looks like <span style="color:green;">{stable}</span> is more stable 🦖 
        </h4>
        """, unsafe_allow_html=True)

# --------------------------------- DATA SOURCE ---------------------------------
link = "https://finance.yahoo.com/"

with st.sidebar:
    st.markdown(f"""<br><br>
    <h4> Data Source: <br>
    {link}
    </h4>
    """, unsafe_allow_html=True)