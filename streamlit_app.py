# coding=utf-8

# Time series forecasting to predict sea surface temperatures at equitorial Pacific
 
# Dataset: https://www.kaggle.com/uciml/el-nino-dataset
# 
# Dataset used here contains surface sea temperature readings 
# taken daily from a series of buoys positioned at the equatorial Pacific. 
# All readings were taken at the same time of the day.
# This data is used to understand and predict seasonal-to-inter annual 
# climate variations originating in the tropics.
# The data under observation covers a span of 4 years — 
# from 1 January, 1993 to 31 December, 1996. 
# There are missing values in the data which are treated by linear interpolation. 

import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import time, math, os, re
import pickle
import warnings
from math import sqrt
import matplotlib.pyplot as plt

import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima

import datetime
from sklearn.metrics import mean_squared_error

warnings.filterwarnings("ignore") # specify to ignore warning messages

st.set_page_config(
page_title="Forecast Pacific",
page_icon="🧊",
layout="wide",
initial_sidebar_state="expanded",
)


st.write("""
# Forecasting Sea Surface Temperatures
Time series forecasting to predict sea surface temperatures at 
equitorial Pacific.
""")

input_weeks = st.slider('Number of weeks ahead to forecast:', 1, 156, 52, 1)
chart = st.empty()

# Reading Excel data into dataframe
cols = ['obs', 'year', 'month', 'day', 'date', 'sea_surface_temp']
df = pd.read_excel("./data/elnino.xlsx", header=0, skiprows=0, names=cols)
df = df.dropna()

# Converting `date` field to `datetime` object
df['date'] = pd.to_datetime(df['date'], format='%y%m%d')

# Drop irrelevant fields from dataframe
df.drop(['obs', 'year', 'month', 'day'], axis=1, inplace=True)

# Setting index for time-series data
df = df.set_index('date')

# Let's see how many non-valid values are there
null_count=0
for value in df['sea_surface_temp']:
    if value == '.':
        null_count += 1

# Making them `nan`
df.loc[df['sea_surface_temp'] == '.', 'sea_surface_temp'] = np.nan

df = df.apply(pd.to_numeric, errors='coerce').astype('float64')
df['sea_surface_temp'].interpolate(method='linear', inplace=True)
# Now there are no null

# Weekly series 
series = df.resample('W').mean()
 
series_df = pd.DataFrame({'Date':series.index.to_list(), 
                          'Temperature (Celsius)':series.sea_surface_temp.to_list()})
history = alt.Chart(series_df, title='Forecast').mark_line(color='black').encode(
    alt.X('Date:T', scale=alt.Scale(zero=False)),
    alt.Y('Temperature (Celsius):Q', scale=alt.Scale(zero=False))).properties(
    height=360, width=1260).interactive()
chart.altair_chart(history, use_container_width=False)

# ARIMA forecasting

with open('./data/forecast_fit.pkl', 'rb') as input_file:
    forecast_fit = pickle.load(input_file)

forecast = forecast_fit.predict(start=len(series), end=len(series)+input_weeks)
forecast.index = pd.date_range(series.index[-1], periods=input_weeks+1, freq='W')

forecast_df = pd.DataFrame({'Date':forecast.index.to_list(), 
                            'Temperature (Celsius)':forecast.to_list()})

for i in range(1,len(forecast_df[:-2])+1):
    new_points = alt.Chart(forecast_df[0:i], title='Forecast').mark_line(color='blue').encode(
                           alt.X('Date:T', scale=alt.Scale(zero=False)),
                           alt.Y('Temperature (Celsius):Q', scale=alt.Scale(zero=False))).properties(
                           height=360, width=720).interactive()
    chart.altair_chart(history+new_points, use_container_width=False)
    time.sleep(0.02)

st.markdown('## Dataset')
st.markdown('Kaggle: <https://www.kaggle.com/uciml/el-nino-dataset>')
st.write("""
Dataset used here contains sea surface temperature readings taken daily from a series of buoys positioned at the equatorial Pacific. 
All readings were taken at the same time of the day. This data is used to understand and predict seasonal-to-inter annual 
climate variations originating in the tropics.

The data under observation covers a span of 4 years — from 1 January, 1993 to 31 December, 1996.
""")
st.markdown('## Github repo')
st.markdown('See the full implementation of ARIMA model here: <https://github.com/yashdeep01/Time-Series-Forecasting>')