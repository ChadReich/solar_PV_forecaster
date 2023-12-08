import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import folium
from streamlit_folium import folium_static

# Centered title using Markdown
st.markdown("<h1 style='text-align: center;'> Solar PV Forecaster 🌤️ </h1>", unsafe_allow_html=True)


st.image('commercial-solar-system-1000x1000.jpeg', caption='Racold Off Grid Solar PV System')
with st.expander("Expand to see the reference"):
     st.write("Click on this [link](https://www.indiamart.com/proddetail/off-grid-solar-pv-system-20200785488.html)")


# Site Information
st.sidebar.title(':blue[Site selection:]')
Select_Site = st.sidebar.selectbox(
    'Select a Site.',
    ('Cape Town', 'Plettenberg Bay', 'Bloemfontein', 'Pretoria', 'Springbok')
)


# Dictionary with site names and corresponding latitude, longitude
sites_data = {
    'Cape Town': {'latitude': -33.918861, 'longitude': 18.423300, 'meter':5884},
    'Plettenberg Bay': {'latitude': -34.052235, 'longitude': 23.371119, 'meter':7672},
    'Bloemfontein': {'latitude': -29.085214, 'longitude': 26.159576, 'meter':7657},
    'Pretoria': {'latitude': -25.746111, 'longitude': 28.188056, 'meter':6508},
    'Springbok': {'latitude': -29.664308, 'longitude': 17.886539, 'meter':1111}
}

# Create a DataFrame from the dictionary
df = pd.DataFrame.from_dict(sites_data, orient='index')

# Get the selected site's coordinates
selected_site_coordinates = df.loc[Select_Site, ['latitude', 'longitude','meter']]

#st.session_state['selected_site_coordinates'] = selected_site_coordinates
# Display the transposed DataFrame
selected_site_coordinates=selected_site_coordinates.to_frame().transpose()

# Display map
# st.map(df, size= 10000)#, zoom =  1000)
m = folium.Map(location=[-33.9249, 18.4241], zoom_start=5)

folium.Marker(
    [-29.664308, 17.886539], popup="<i>Springbok</i>",
).add_to(m)
folium.Marker(
    [-25.746111, 28.188056], popup="<i>Pretoria</i>",
).add_to(m)
folium.Marker(
    [-29.085214, 26.159576], popup="<i>Bloemfontein</i>",
).add_to(m)
folium.Marker(
    [-34.052235, 23.371119], popup="<i>Plettenberg Bay</i>",
).add_to(m)
folium.Marker(
    [-33.918861, 18.423300], popup="<i>Cape Town</i>",
).add_to(m)
folium_static(m)

st.markdown('<p style="text-align: center;">Solar PV sites at different provinces in South Africa</p>', unsafe_allow_html=True)


# Display the site
Display = st.sidebar.checkbox('Show Site Coordinates')

if Display:
    Select_Site = st.sidebar.write(selected_site_coordinates)


# Loading the Data, changing the data/time and setting time as the index
DATE_COLUMN = 'tstamp'
DATA_PATH = ('solar_project_data.csv')

@st.cache_data
def load_data(DATA_PATH):
    data = pd.read_csv(DATA_PATH)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data = data.set_index("tstamp")
    return data

st.session_state['data'] = load_data(DATA_PATH)

@st.cache_data
def select_site_dataframe(meter_id,DATA_PATH):
    Data = load_data(DATA_PATH)
    Data_meter_ID = Data[Data["meter_id"] == int(meter_id)]
    return Data_meter_ID


Site_DataFrame = select_site_dataframe(selected_site_coordinates["meter"],DATA_PATH)
#Site_DataFrame['ptot'] = abs(Site_DataFrame['ptot'])

# Interract With the Data
st.sidebar.title(':blue[Interact with the data:]')

# Resmapling the data
# Define the dictionary
time_intervals = {'5 min': '5T', '1 hour': '1H', '2 hours': '2H'}

# Create a radio button
selected_option = st.sidebar.radio('Select a resampling time', list(time_intervals.keys()), index=0, key='time_interval',horizontal=True)

# Get the corresponding value from the dictionary
selected_value = time_intervals[selected_option]

Site_DataFrame = Site_DataFrame.resample(selected_value).sum()
Site_DataFrame_monthly_average = Site_DataFrame.resample('M').mean()
st.session_state['Site_DataFrame_monthly_average'] = Site_DataFrame_monthly_average

start_date=st.sidebar.date_input('Start Date', key='Start Date',value=pd.to_datetime("2022/01/01"))
end_date=st.sidebar.date_input('End Date', key = 'End Date')


st.session_state['start_date'] = start_date
st.session_state['end_date'] = end_date

filtered_values=Site_DataFrame[(Site_DataFrame.index>=pd.to_datetime(start_date)) &  (Site_DataFrame.index<=pd.to_datetime(end_date))]
filtered_values=filtered_values.drop(columns="meter_id")

filtered_monthly_average = Site_DataFrame_monthly_average.drop(columns="meter_id")


# Display the site DataFrame
if st.sidebar.checkbox('Show Site DataFrame'):
    st.caption("Site DataFrame Resampled at "+ selected_option )
    st.write(filtered_values)
    st.caption("Montly Average of Site Data")
    st.write(filtered_monthly_average)

# Display the site Graph
if st.sidebar.checkbox('Plot Total Power Yield per site'):
    fig, ax = plt.subplots()
    ax.plot(filtered_values["ptot"])
    st.plotly_chart(fig)
    st.markdown('<p style="text-align: center;"> The Total Power Yield Per Site</p>', unsafe_allow_html=True)
