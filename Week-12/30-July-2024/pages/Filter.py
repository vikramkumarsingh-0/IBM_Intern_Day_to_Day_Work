import streamlit as st
import yfinance as yf

# Function to get stock data
def get_stock_data(ticker, period='1y'):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        return data
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

# Title
st.title("Stock Data Selector")

# Selectbox for Exchange
exchange = st.selectbox("Select Exchange", ["BSE", "NSE"])

# Input for stock ticker
stock_ticker = st.text_input(f"Enter {exchange} stock ticker (e.g., RELIANCE.NS for NSE or RELIANCE.BO for BSE):", value="RELIANCE.NS")

# Selectbox for data category
category = st.selectbox("Select Data Category", ["Historical Data", "Recent Data"])

# Set the period based on category selection
if category == "Historical Data":
    period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "3y", "5y", "max"]
    period = st.selectbox("Select Period for Historical Data", period_options)
else:
    period = '1d'  # For recent data, we'll just fetch the most recent data

# Fetch and display stock data
if stock_ticker:
    stock_data = get_stock_data(stock_ticker, period)
    if stock_data is not None:
        st.write(f"Data for {stock_ticker} ({category} - {period}):")
        st.write(stock_data.tail() if category == "Recent Data" else stock_data)  # Display the last few rows or entire data based on category
