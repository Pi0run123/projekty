import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import plotly.express as px

st.title('Stock Dashboard')
ticker = st.sidebar.text_input('Ticker')
start_date = st.sidebar.text_input('Start Date')
end_date = st.sidebar.text_input('End Date') 

data = yf.download(ticker, start=start_date, end=end_date) 
fig = px.line(data, x=data.index, y=data['Adj Close'], title=ticker)
st.plotly_chart(fig)

pricing_data, fundamental_data, news = st.tabs (['Pricing Data', 'Fundamental Data', 'Top 10 News'])

with pricing_data:
    st.header('Pricing Movements')
    data2 = data
    data2['% Change'] = data2['Adj Close'] / data2['Adj Close'].shift(1) - 1
    st.write(data2) 
    annual_returns = data2['% Change'].mean()*252*100
    st.write('Annual Return is ',annual_returns,'%')
    stdev = np.std(data2['% Change'])*np.sqrt(252)
    st.write('Standard Deviation is ',stdev*100,'%')


with fundamental_data:
    st.header('Fundamental Data')
    st.write('Fundamental')

from stocknews import StockNews
with news:
    st.header(f'News of {ticker}')
    sn = StockNews(ticker, save_news=False)
    df_news = sn.read_rss()
    for i in range(10):
        st.subheader(f'News {i+1}')
        st.write(df_news['published'][i])    
        st.write(df_news['title'][i])  
        st.write(df_news['summary'][i])  
        title_sentiment = df_news['sentiment_title'][i]
        st.write(f'Title sentiment {title_sentiment}')
        news_sentiment = df_news['sentiment_summary'][i]
        st.write(f'News sentiment {news_sentiment}')