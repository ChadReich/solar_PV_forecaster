import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd

df=pd.read_csv('solar_prediction_results.csv')

fig = px.bar(title='Real vs Predicted Power Output for site 10710')
fig.add_trace(go.Bar(x=df['tstamp'],y=df['ptot_pred'],name='Predicted Power Output'))
fig.add_trace(go.Bar(x=df['tstamp'],y=df['ptot'],name='Real Power Output'))
st.plotly_chart(fig)
