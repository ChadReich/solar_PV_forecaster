import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

project_df=pd.read_csv('solar_project_data.csv')
# Filter DataFrame for only the year 2022
project_df = project_df[(project_df['tstamp'] >= '2022-01-01') & (project_df['tstamp'] < '2023-01-01')]

# Define the meter ids for plotting
meter_ids_to_plot = [5884, 6508, 7672, 7672]

# Create subplots
fig, axes = plt.subplots(nrows=len(meter_ids_to_plot), figsize=(10, 8), sharex=True)

# Plot each meter on a separate subplot
for i, meter_id in enumerate(meter_ids_to_plot):
    df_meter = project_df[project_df['meter_id'] == meter_id]
    colors = ['blue', 'green', 'red']  # Colors for Power Loss Event 0, 1, and 2

    for event_value, color in zip([0, 1, 2], colors):
        df_event = df_meter[df_meter['Power Loss Event'] == event_value]

        # Assign labels based on event values
        event_label = {0: 'Normal operation', 1: 'Loadshedding', 2: 'Outlier event'}.get(event_value, f'Event {event_value}')

        axes[i].scatter(df_event['tstamp'], df_event['Power Loss Event'], label=event_label, color=color)

    axes[i].set_title(f'Meter {meter_id}')
    axes[i].set_ylabel('Power Loss Event')
    axes[i].legend()

# Add labels, title, and legend
axes[-1].set_xlabel('Timestamp')
st.pyploy(axes)
plt.suptitle('Power Loss Event for Meters in 2022')
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Adjust subplot layout to accommodate suptitle
plt.show()
