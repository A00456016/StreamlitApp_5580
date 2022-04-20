import streamlit as st
import pandas as pd
import requests


st.title("Bitcoin Prices - By Harsh Panchal")

days = st.slider('Please select number of days', 1, 365, 90)

currency = st.radio(
     "Please select your preferred currency",
     ('cad', 'usd', 'inr'))
     
payload = {'vs_currency': currency, 'days': days, 'interval': 'daily'}
r = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin/market_chart', params=payload)

#print(r.url)

data = r.json()

df = pd.json_normalize(data, record_path =['prices'])
average = df[1].mean()
df.rename(columns={1:currency}, inplace=True)

df[0] = pd.to_datetime(df[0],unit='ms')

#print(df)
#df.plot.line(x=0, y=1)
df = df.rename(columns={0:'index'}).set_index('index')

st.line_chart(df)
st.write('Average price during this time was ', average, currency)