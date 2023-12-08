import streamlit as st
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

data = st.session_state['data']
data = data.groupby('meter_id').resample("M").agg({'ptot': np.mean,'Dhi': np.mean, 'Dni': np.mean,'Ebh': np.mean, 'Ghi': np.mean}).reset_index()

st.header('The Average Total for each Site')

fig = px.line(data, x="tstamp", y="ptot", title='The Average Total Power Yeild Per Month for each Site',color="meter_id")
# Display the plotly chart
st.plotly_chart(fig,use_container_width=True)

with st.expander("See explanation"):
    st.write(
        "The chart above shows some numbers I picked for you")




st.header('The Different Types of Irradiation')

#st.title('The Different Types of Irradiation')

irradiations = st.radio(
    'Select Irradiation Type.',
    ("Dhi", "Dni", "Ebh", "Ghi"),horizontal=True
)

data=data.sort_values('tstamp')

fig = go.Figure()
for meter_id in data['meter_id'].unique():
    filtered = data[data['meter_id']==meter_id]
    fig.add_scatter(x=filtered['tstamp'], y=filtered[irradiations],mode='lines',name=str(meter_id))

# Show plot
st.plotly_chart(fig)

with st.expander("See explanation"):
    st.write(
        "The chart above shows some numbers I picked for you")
