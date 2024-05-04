import yfinance as yf
import pandas as pd 
import streamlit as st
from datetime import datetime

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

st.title('Stock Price')

st.write(
    """
### Simple stock price app tracking **dividends**, **lowest**, **closing price** and **volume**

"""
)


st.write(
    """
#### 1- tracking the **dividends**

   e.g. DFN.TO,  ZWB.TO,  ENB.TO,  TRP.TO,  BNS.TO,  LB.TO,  BCE.TO,  SBLK,  DVN,  F,  VZ,  TLT,  PFE

"""
)

divd_ticker = st.text_input("What's the ticker?", "DFN.TO")

date = st.date_input("Choose a date", datetime.now().date())

st.write(f"#### Dividend Stock {divd_ticker}\n#### The date is {date.strftime('%Y-%m-%d')}")

(yf
     .Ticker(divd_ticker)
     .dividends
)

st.write(
    """
#### 2- tracking **stocks** 

   e.g. NVDA, TSLA, AAPL, AMZN

"""
)

ticker = st.text_input("What's the ticker?", "TSLA")

st.markdown(f"#### Stock {ticker}\n#### The date is {date.strftime('%Y-%m-%d')}")

ticker = yf.Ticker(ticker).history(period='1y')

st.write("""
##### closing price
""")

st.line_chart(ticker.Close)

st.write("""
##### low price
""")

st.line_chart(ticker.Low)

st.write('''
#### volume
''')

st.bar_chart(ticker.Volume)