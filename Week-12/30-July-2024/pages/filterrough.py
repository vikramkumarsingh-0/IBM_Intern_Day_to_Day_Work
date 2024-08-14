import streamlit as st
import yfinance as yf

ticker = input("Enter the stock symbol: ")
ticker = ticker.ns
stock = yf.Ticker(ticker)
print(stock.head())