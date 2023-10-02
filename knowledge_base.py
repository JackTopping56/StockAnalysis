# Stock Analysis - Knowledge Base
# This is the knowledge base for my system, this gets the data that is used by the inference engine
# The knowledge base within my system is known as knowledge_base.py

import yfinance as yf


# Function to fetch stock data to the Knowledge Base from Yahoo Finance API
def fetch_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data
