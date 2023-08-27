import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from scipy.stats import zscore

st.set_page_config(layout="wide")

# Function to fetch a list of stock symbols from a file or API
def get_stock_symbols():

    turkey_tickers = list(set([
        "---Turkey---",
        'AKBNK.IS', 'GARAN.IS', 'ISCTR.IS', 'KCHOL.IS', 'ASELS.IS',  # Turkey's banks and companies
        'TTKOM.IS', 'TCELL.IS', 'VESTL.IS', 'PETKM.IS', 'TKFEN.IS',  # Telecom, energy, and industrial companies
        'SAHOL.IS', 'ULKER.IS', 'KOZAL.IS', 'TATGD.IS', 'AYGAZ.IS',  # Food, mining, and retail companies in Turkey
        "EGSER.IS", "AFYON.IS", "BUCIM.IS", "EREGL.IS", "BSOKE.IS",
        "ADEL.IS",
        # Add more Turkish tickers as needed
    ]))
    turkey_tickers.sort()

    uk_tickers = list(set([
         "-----UK-----",
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',  # Example of non-UK tickers from previous list
        'HSBA.L', 'LLOY.L', 'BARC.L', 'RBS.L', 'RDSA.L',  # UK banks and energy companies
        'AZN.L', 'GSK.L', 'ASTRAZEN.L', 'BT-A.L', 'VOD.L',  # Pharmaceutical and telecom companies in the UK
        'TSCO.L', 'MKS.L', 'RR.L', 'IAG.L', 'CCL.L',  # Retail, airline, and consumer goods companies
        'BP.L', 'RDSB.L', 'STAN.L', 'NG.L', 'GLEN.L',  # UK energy and mining companies
        # Add more UK tickers as needed
    ]))
    uk_tickers.sort()


    stock_symbols = turkey_tickers + uk_tickers

    # stock_symbols.sort()
    return stock_symbols


def get_interval_list():
    interval_list = ["5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    return interval_list


# Function to fetch Yahoo Finance data
def fetch_yahoo_finance_data(stock_name, start_date, end_date, frequency):
    try:
        df = yf.download(stock_name, start=start_date, end=end_date, interval=frequency)
        if not df.empty:
            df = df[["Close", "Low", "High", "Volume"]]
            df['Return'] = df['Close'].pct_change()
            df['Z-Score'] = zscore(df['Return'].dropna())

        else:
            df = None
        return df
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return None

# Streamlit app
def main():


    col1, col2 = st.columns([2,1])


    with st.sidebar:
        st.title('Trading Dashboard')

        stock_symbols = get_stock_symbols()
        stock_name = st.selectbox('Select Stock Symbol:', stock_symbols)

        interval_list = get_interval_list()
        interval = st.selectbox('Select Interval:', interval_list)

        today = datetime.today()
        max_days = 1825
        if interval in ["1m", "5m", "15m", "30m", "60m", "90m"]:
            max_days = 60-1
        if interval in ["1h"]:
            max_days = 730-1
        default_start_date = today - timedelta(days=max_days)
        start_date = st.date_input('Start Date:', default_start_date)
        end_date = st.date_input('End Date:', today)

        fetch_button = st.button('Fetch Data')



    if fetch_button:
        df = fetch_yahoo_finance_data(stock_name, start_date, end_date, interval)
        
        if df is not None:
            
            # with st.sidebar:
            #     st.write(df)
            
            with col1:
                st.title('Close Prices')
                st.line_chart(df['Close'])

                st.title('Stationary Data')
                st.line_chart(df['Return'])

                st.title('Z-Score Data')
                st.line_chart(df['Z-Score'])

            with col2:
                ### Stationary DF
                st.title(' ')
                st.write(df)

                ## Return Histogram
                # st.title('Return Hist')
                fig = px.histogram(df['Return'].dropna())
                fig.update_layout(xaxis_title='Return %', yaxis_title='Frequency', showlegend=False)
                st.plotly_chart(fig)


                ### Z-Score Histogram
                # st.title('Z-Score Hist')
                bin_edges = [-3, -2.5, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 2.5, 3]
                hist_data, _ = np.histogram(df['Z-Score'].dropna(), bins=bin_edges)
                fig = go.Figure(data=[go.Bar(x=bin_edges[:-1], y=hist_data, marker_color='#9ac8fd')])
                fig.update_layout(xaxis_title='Z-Score', yaxis_title='Frequency', showlegend=False)
                st.plotly_chart(fig)

            

        else:
            st.write("No data available for the selected parameters.")

if __name__ == '__main__':
    main()
