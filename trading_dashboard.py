import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta

# Function to fetch a list of stock symbols from a file or API
def get_stock_symbols():
    stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', "ARCLK.IS"]
    stock_symbols.sort()
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
        else:
            df = None
        return df
    except Exception as e:
        st.write(f"An error occurred: {e}")
        return None

# Streamlit app
def main():
    st.title('Trading Dashboard')

    stock_symbols = get_stock_symbols()
    stock_name = st.selectbox('Select Stock Symbol:', stock_symbols)


    interval_list = get_interval_list()
    interval = st.selectbox('Select Interval:', interval_list)



    # frequency_key = 'frequency_selection'
    # frequency = st.radio('Select Frequency:', ('Daily', 'Weekly'), key=frequency_key)
    # frequency_df = "1d" if frequency == "Daily" else "1wk"

    today = datetime.today()
    max_days = 10000
    if interval in ["1m", "5m", "15m", "30m", "60m", "90m"]:
        max_days = 60-1
    if interval in ["1h"]:
        max_days = 730-1
    default_start_date = today - timedelta(days=max_days)
    start_date = st.date_input('Start Date:', default_start_date)
    end_date = st.date_input('End Date:', today)

    if st.button('Fetch Data'):
        df = fetch_yahoo_finance_data(stock_name, start_date, end_date, interval)
        
        if df is not None:
            st.write(df)

            st.title('Close Prices')
            st.line_chart(df['Close'])

            # Add a button to toggle between 'Close' and 'Volume' charts
            chart_type = st.radio("Select Chart Type:", ('Close', 'Volume'))
            if chart_type == 'Close':
                st.line_chart(df['Close'])
            else:
                st.line_chart(df['Volume'])

        else:
            st.write("No data available for the selected parameters.")

if __name__ == '__main__':
    main()
