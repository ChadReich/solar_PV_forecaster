import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
data = st.session_state['data']
original_df=st.session_state['data']
data = data.groupby('meter_id').resample("M").agg({'ptot': np.mean,'Dhi': np.mean, 'Dni': np.mean,'Ebh': np.mean, 'Ghi': np.mean}).reset_index()




original_df=original_df.groupby(['meter_id']).resample('D').sum()
original_df=original_df.drop(columns=['meter_id']).reset_index()
original_df = original_df.sort_values(by="tstamp")
fig = px.line(original_df, x="tstamp", y='ptot',color='meter_id',title='Total Power')
st.plotly_chart(fig)







st.markdown('<p style="text-align: center;"> The Average Total Power Yield Per Month for each Site</p>', unsafe_allow_html=True)

fig = px.line(data, x="tstamp", y="ptot",color="meter_id")
# Display the plotly chart
st.plotly_chart(fig,use_container_width=True)

#with st.expander("See explanation"):
    #st.write(
        #"The chart above shows some numbers I picked for you")

# Select the different types of feature to explain the above graph

# Display Features
# Site Information
st.sidebar.title(':blue[Show and Plot Features:]')


if st.sidebar.checkbox('Plot Different Types of irradiation'):
 st.markdown('<p style="text-align: center;"> The Different Types of irradiation </p>', unsafe_allow_html=True)
 irradiations = st.radio(
    'Select irradiation Type.',
    ("Dhi", "Dni", "Ebh", "Ghi"),horizontal=True
)

 data=data.sort_values('tstamp')

 fig = go.Figure()
 for meter_id in data['meter_id'].unique():
    filtered = data[data['meter_id']==meter_id]
    fig.add_scatter(x=filtered['tstamp'], y=filtered[irradiations],mode='lines',name=str(meter_id))

# Show plot
 st.plotly_chart(fig)





project_df=st.session_state['data']
original_df=st.session_state['data']

project_df=project_df[(project_df.index>=pd.to_datetime(st.session_state['start_date'])) &  (project_df.index<=pd.to_datetime(st.session_state['end_date']))]

project_df.reset_index(inplace=True)

project_df=project_df.groupby(['tstamp','meter_id','Power Loss Event']).count().reset_index()
project_df.set_index('tstamp',inplace=True)
project_df=project_df.groupby(['meter_id',"Power Loss Event"]).resample('M').count().drop(columns=['meter_id','Power Loss Event']).reset_index()
sites_data = {
    'Cape Town': {'latitude': -33.918861, 'longitude': 18.423300, 'meter':5884},
    'Plettenberg Bay': {'latitude': -34.052235, 'longitude': 23.371119, 'meter':7672},
    'Bloemfontein': {'latitude': -29.085214, 'longitude': 26.159576, 'meter':7657},
    'Pretoria': {'latitude': -25.746111, 'longitude': 28.188056, 'meter':6508},
    'Springbok': {'latitude': -29.664308, 'longitude': 17.886539, 'meter':1111}
}

project_df["Event Name"]=project_df['Power Loss Event'].map({0: 'Normal operation', 1: 'Loadshedding', 2: 'Outlier event'})
sites_data=pd.DataFrame.from_dict(sites_data,orient='index')
for meter in project_df['meter_id'].unique():
    fig = px.bar(project_df[project_df['meter_id']==meter]
    , x='tstamp', y='ptot',color='Event Name',title='Power Loss Event for site ' +str(meter) + ' in ' + sites_data[sites_data['meter']==meter].index[0],barmode='group')

    st.plotly_chart(fig)
all_project_df=original_df
all_project_df["Event Name"]=all_project_df['Power Loss Event'].map({0: 'Normal operation', 1: 'Loadshedding', 2: 'Outlier event'})
all_project_df = original_df.groupby('Event Name').count().reset_index()

st.write(all_project_df)

fig = px.histogram(all_project_df,x='Event Name',y='meter_id',color='Event Name',title='Power Loss Event for all sites',barmode='group')
st.plotly_chart(fig)

original_df=original_df.groupby(['meter_id']).resample('D').sum()
original_df=original_df.drop(columns=['meter_id']).reset_index()
original_df = original_df.sort_values(by="tstamp")
fig = px.line(original_df, x="tstamp", y='ptot',color='meter_id',title='Total Power')
#st.plotly_chart(fig)
