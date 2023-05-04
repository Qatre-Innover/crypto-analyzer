import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import extractor
import my_functions

from datetime import timedelta
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima.model import ARIMA


st.set_page_config(layout="wide", page_title="My Watchlist")
my_functions.add_logo()
my_functions.set_plotly_template()


def plotly_figure_line():
    # Creating a Plotly Figure
    fig = px.line(data, 
                x = data.index,
                y = data.columns[:4], 
                template = "dc", 
                title = "Trends in Daily Historical Prices ($)")
    fig.update_layout(
        yaxis_title="Price ($)",
        legend_title="Category",
        title_font_size = 20
    )
    st.plotly_chart(fig)


def plotly_candlestick():
    # Create/Define the CandleStick Data
    candlestick = go.Candlestick(
        x=data.index, 
        open = data["Open"],
        high = data["High"],
        low = data["Low"],
        close = data["Close"]
    )

    # Creating a CandleStick Chart
    fig = go.Figure(data = candlestick)
    fig.update_layout(
        yaxis_title="Price ($)",
        legend_title="Category",
        title="Candlestick of Daily Historical Prices ($)",
        template="dc",
        title_font_size = 20
    )
    st.plotly_chart(fig)

def calculations(data):   
    c1, c2, c3 = st.columns(3)
    c1.metric(label = 'Current Value', value = round(data[-1], 2),
              delta=f"--%" 
            )
    c2.metric(label = '1 day ago', value = round(data[-2], 2),  
                delta = f"{round(((data[-1] - data[-2])/data[-1])*100, 4)}%"
            )
    c3.metric(label = '7 days ago', value = round(data[-8], 2), 
                delta = f"{round(((data[-1] - data[-8])/data[-1])*100, 4)}%"
            )
    
    c4, c5, c6 = st.columns(3)
    c4.metric(label = '14 days ago', value = round(data[-15], 2), 
                delta = f"{round(((data[-1] - data[-15])/data[-1])*100, 4)}%"
            )
    c5.metric(label = '28 days ago', value = round(data[-29], 2), 
                delta = f"{round(((data[-1] - data[-29])/data[-1])*100, 4)}%"
            )
    c6.write("\u2001")



def acf_plot(data, category='Open'):
    
    col1, col2 = st.columns([1, 3])
    list_categories = ["Open", "High", "Low", "Close"]

    with col1:
        st.markdown("""<p style="margin: 60px 0px 0px 0px; font-size:20px;"> 
                        Price Category </p> 
                    """, unsafe_allow_html=True)
        category = st.radio(label="Sample", options=list_categories, 
                            label_visibility="collapsed")
    
    with col2:
        acf_array = acf(data[category], nlags=15)

        # Generating an Area Plot
        fig = px.area(acf_array, template="dc")

        # Fix the range and layout
        fig.update_layout(
            title="Auto-Correlation (ACF) Plot",
            yaxis_title="Correlation Value",
            xaxis_title="Number of Lags",
            legend_title="Category",
            title_font_size = 15
        )

        fig.update_layout(showlegend = False, width=700)
        st.plotly_chart(fig)
    
    return category

def time_series_plot(data, category="Open"):

    index = pd.DatetimeIndex(data.index).to_period("B")
    new_index = pd.period_range(start=index[0], 
                                end=index[-1])
    data = data[data.index.isin(new_index.to_timestamp())]

    # Initialize an empty array
    bic = []

    # Loop through a range of AR models and get the BIC
    for i in range(1, 7):
        model = ARIMA(data.tail(28)[category], order=(i, 0, 0))
        result = model.fit()
        bic.append(result.bic)
    
    min_bic_lags = np.argmin(bic)+1 

    # Making predictions
    date_4_days_ago = data.index[-1] - timedelta(days=4)
    trunc_data = data[:date_4_days_ago]

    # Fit the AR(1) model
    model = ARIMA(trunc_data[category], order=(min_bic_lags, 0, 0))
    result = model.fit()

    # # Get the forecasts for the next 7 days
    preds = result.get_forecast(steps=7).summary_frame()
        
    # Creating a figure containing Real, Predicted, and CI values 
    fig = go.Figure([
        go.Scatter(
            name="True Value", 
            x=data.index,
            y=data[category], 
            mode='lines'
        ),
        go.Scatter(
            name="Predicted Value", 
            x=preds.index,
            y=preds["mean"], 
            mode='lines'
        ),
        go.Scatter(
            name="Upper Value", 
            x=preds.index,
            y=preds["mean_ci_upper"], 
            mode='lines',
            line=dict(color='lightblue', width=0)
        ),
        go.Scatter(
            name="Lower Value", 
            x=preds.index,
            y=preds["mean_ci_lower"], 
            mode='lines',
            line=dict(color='lightgrey', width=0),
            fill="tonexty"
        )
        
    ])
    fig.add_vline(x=data.index[-1], line_width=1.5, line_dash="dash", line_color="purple")
    fig.add_vline(x=trunc_data.index[-1], line_width=1.5, line_dash="dash", line_color="green")
    fig.update_layout(
        title="Actual vs. Forecasted Price overtime",
        yaxis_title="Price ($)",
        showlegend=False,
        template="dc",
        title_font_size = 20
    )

    st.plotly_chart(fig)

# ---------------------- Streamlit Layout and features --------------------
st.markdown("# Know what your next crypto would be?") 
st.markdown("""
<p style="font-size:20px;">Welcome to your Watchlist!<br>Select a cryptocurrency of your
choice from the menu bar, and the month-wise span. And, I will create a daily historical analysis
for you. I have five different options that will help you know your stock better, the opening price, 
highest price, lowest price, closing price, and the volume.</p>
""", unsafe_allow_html=True)

currencies = pd.read_csv('names.csv', header=0)
currencies_codes = currencies.iloc[:, 1]

# Default Cryptocurrency and number of months
myOption = 'BTC-USD'
months = 12
optional_dates = [1, 3, 6, 9, 12, 18, 24, 36, 48, 60]

with st.sidebar:
    st.markdown("""<h2> Select the currency </h2>""", unsafe_allow_html= True)
    myOption = st.selectbox(label="Sample", options=currencies_codes, label_visibility="collapsed")

    st.markdown("""<h2> Select month-wise span </h2>""", unsafe_allow_html= True)
    months = st.selectbox(label="Sample", options=optional_dates, label_visibility="collapsed")


start, stop, data = extractor.get_data(stock=myOption, days=30*months)
plotly_figure_line()
plotly_candlestick()

#------------------------------ TABS --------------------------
list_tabs = ["Open", "High", "Low", "Close", "Volume"]

whitespace = 9
tabs = st.tabs([s.center(whitespace,"\u2001") for s in list_tabs])

with tabs[0]:
   calculations(data.iloc[:, 0])

with tabs[1]:
   calculations(data.iloc[:, 1])

with tabs[2]:
   calculations(data.iloc[:, 2])

with tabs[3]:
   calculations(data.iloc[:, 3])

with tabs[4]:
   calculations(data.iloc[:, 5])

# ------------------ Statistics Section -------------------------
# st.markdown("## Data Statistics")
st.markdown(f"""<br><br>
<p style="font-size:20px;"> Here is a comprehensive overview of the key statistical measures 
for different attributes of <strong style="color:red;">{myOption}</strong>. These measures can provide you with valuable insights into the distribution and variability of 
cryptocurrency data, helping you make correct decisions about your investments based on statistics.
</p><br>
""", unsafe_allow_html=True)
statistics = data.describe()
st.table(statistics)

# ------------------- Forecast Section ---------------------------
st.markdown("## This is what I predicted for you!🦖")
st.markdown(f"""
<p style="font-size:20px;">Autocorrelation, also known as serial correlation, is a measure of the degree to which a 
time series is correlated with itself at different time lags. In other words, it is a 
correlation between a time series and a delayed version of itself. <br> <br> Autocorrelation is important in time series analysis because it helps identify patterns or 
trends in the data that can be used to make predictions about future values. A time series 
with high autocorrelation indicates that there is a strong relationship between past and 
future values, while a time series with low autocorrelation indicates that there is little 
or no relationship between past and future values. <br><br>Here is the ACF plot that I prepared for <strong>{myOption}</strong>.
</p>
""", unsafe_allow_html=True)
category = acf_plot(data.tail(28))

st.markdown(f"""<br>
<p style="font-size:20px;">I have used an <strong style="color:red;">Auto-Regressive model</strong> 
to predict the next 4 day prices of <strong>{myOption}</strong> for you 🦖 . <br><br>
<strong>Auto-Regression: </strong>It is a statistical 
method used in time series forecasting that models the relationship between the current 
observation and one or more past observations of a time series. The basic idea behind AR is 
that the current value of a time series can be predicted based on its past values.
</p>
""", unsafe_allow_html=True)
time_series_plot(data, category)

# --------------------------------- DATA SOURCE ---------------------------------
link = "https://finance.yahoo.com/"

with st.sidebar:
    st.markdown(f"""<br><br>
    <h4> Data Source: <br>
    {link}
    </h4>
    """, unsafe_allow_html=True)