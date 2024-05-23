import json
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st

# Function to load data
@st.cache
def load_data(file_path):
    with open(file_path, 'r') as f:
        click_data = [json.loads(line) for line in f]
    return pd.DataFrame(click_data)

# Load data
df = load_data('click_data.json')

# Process data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['button_number'] = df['elementId'].str.extract(r'button(\d+)').astype(float)
df['hour'] = df['timestamp'].dt.hour
df['date'] = df['timestamp'].dt.date
button_clicks = df['button_number'].value_counts().reset_index()
button_clicks.columns = ['button_number', 'click_count']
heatmap_data = button_clicks.pivot_table(index='button_number', values='click_count', fill_value=0)
daily_clicks = df.groupby('date').size().reset_index(name='click_count')

# Streamlit app
st.title("Click Data Dashboard")

st.header("Scatter Plot of Button Clicks Over Time")
fig_scatter = px.scatter(df, x='timestamp', y='button_number', color='elementClass',
                         title='Scatter Plot of Button Clicks Over Time',
                         labels={'timestamp': 'Timestamp', 'button_number': 'Button Number'})
st.plotly_chart(fig_scatter)

st.header("Box Plot of Button Clicks by Hour")
fig_box = px.box(df, x='hour', y='button_number', color='elementClass',
                 title='Box Plot of Button Clicks by Hour',
                 labels={'hour': 'Hour of the Day', 'button_number': 'Button Number'})
st.plotly_chart(fig_box)

st.header("Heatmap of Clicks per Button Number")
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", linewidths=.5)
plt.title('Heatmap of Clicks per Button Number')
plt.xlabel('Click Count')
plt.ylabel('Button Number')
st.pyplot(plt.gcf())

st.header("Per Day Click Data")
fig_daily = go.Figure()
fig_daily.add_trace(go.Scatter(x=daily_clicks['date'], y=daily_clicks['click_count'], mode='lines+markers', name='Click Count'))
fig_daily.update_layout(
    title='Per Day Click Data',
    xaxis_title='Date',
    yaxis_title='Click Count',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)
st.plotly_chart(fig_daily)
