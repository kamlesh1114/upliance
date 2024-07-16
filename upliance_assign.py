
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# Function to load the dataset using SQLAlchemy
@st.cache_resource()
def load_data():
    # Create a connection to the database
    engine = create_engine('sqlite:///upliance_test.db')

    # Define the query to fetch the necessary columns
    query = '''
    SELECT tpep_pickup_datetime, tpep_dropoff_datetime, dropoff_longitude, dropoff_latitude
    FROM your_table_name
    '''

    # Fetch data and load into DataFrame
    df = pd.read_sql(query, con=engine)

    # Filter rows with dropoff location near Crate and Barrel
    crate_and_barrel_latitude = 40.7258
    crate_and_barrel_longitude = -74.0047
    threshold = 0.001
    filtered_df = df[
        (df['dropoff_latitude'].between(crate_and_barrel_latitude - threshold, crate_and_barrel_latitude + threshold)) &
        (df['dropoff_longitude'].between(crate_and_barrel_longitude - threshold, crate_and_barrel_longitude + threshold))
    ].copy()

    return filtered_df

# Function to calculate trip durations
def calculate_trip_durations(df):
    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds()

    short_trips = df[df['trip_duration'] < 600]  # 600 seconds = 10 minutes
    long_trips = df[df['trip_duration'] > 3660]  # 3660 seconds = 61 minutes
    return short_trips, long_trips

# Main function to render the Streamlit app
def main():
    # Set page configuration
    st.set_page_config(
        page_title="Taxi Data Analytics",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state='collapsed'
    )

    # Logo
    st.image('upliance.ai-wordmark.png', use_column_width=False, width=250) 

    st.title("NYC Yellow Taxi Trip Data Analysis")

    # Load data
    df = load_data()

    # Display filtered data (first 1000 rows for preview)
    st.subheader("Trips Ending at Crate and Barrel Flagship Store")
    st.dataframe(df.head(1000), use_container_width=True)  

    # Calculate trip durations
    short_trips, long_trips = calculate_trip_durations(df)

    # Compute counts of short and long trips
    num_short_trips = short_trips.shape[0]
    num_long_trips = long_trips.shape[0]

    # Display trip durations
    st.subheader("Trip Duration Analysis")
    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.markdown(f'<div style="padding: 20px; background-color: #4C3BCF; border-radius: 10px; color: white;"> \
                        <h3 style="text-align: center; color: white;">Trips shorter than 10 minutes</h3> \
                        <p style="text-align: center; font-size: 32px;">{num_short_trips}</p> \
                        </div>', unsafe_allow_html=True)

    with col2:
        with st.container():
            st.markdown(f'<div style="padding: 20px; background-color: #4C3BCF; border-radius: 10px; color: white;"> \
                        <h3 style="text-align: center; color: white;">Trips longer than 61 minutes</h3> \
                        <p style="text-align: center; font-size: 32px;">{num_long_trips}</p> \
                        </div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown("")
    # Time of day visualization using Plotly
    st.subheader("Time of Day Visualization for Trips Ending at Crate and Barrel")
    df['end_hour'] = df['tpep_dropoff_datetime'].dt.hour
    trips_by_hour = df['end_hour'].value_counts().sort_index()

    fig = go.Figure(data=[go.Bar(x=trips_by_hour.index, y=trips_by_hour.values)])
    fig.update_layout(
        title='Trips Ending at Crate and Barrel by Hour of the Day',
        xaxis_title='Hour of the Day',
        yaxis_title='Number of Trips',
        template='plotly_white',
        width=None,  
        height=500  
    )

    st.plotly_chart(fig, use_container_width=True)  

if __name__ == "__main__":
    main()


