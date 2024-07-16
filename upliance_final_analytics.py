import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pymongo import MongoClient

# Function to load the datasets from MongoDB
@st.cache_resource()
def load_data():

    # Create a connection to the MongoDB database OR Fetch Preprocessed data locally
    # client = MongoClient('mongodb+srv://kajdhfywgdUDVHsdvhsvds+shdvhsd/svdhsv/') 
    # db = client['upliance_data']
    # # Load data into DataFrames
    # filtered_trips_df = pd.DataFrame(list(db['filtered_trips'].find()))
    # short_trips_df = pd.DataFrame(list(db['short_trips'].find()))
    # long_trips_df = pd.DataFrame(list(db['long_trips'].find()))
    # trips_by_hour_df = pd.DataFrame(list(db['trips_by_hour'].find()))

# Fetch Pre-Processed data from CSV
    filtered_trips_df=pd.read_csv("filtered_df.csv")
    short_trips_df=pd.read_csv("short_trips.csv")
    long_trips_df=pd.read_csv("long_trips.csv")
    trips_by_hour_df=pd.read_csv("trips_by_hour.csv")

    return filtered_trips_df, short_trips_df, long_trips_df, trips_by_hour_df



# Main function to render the Streamlit app (Visualisation The Data)
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
    filtered_trips_df, short_trips_df, long_trips_df, trips_by_hour_df = load_data()

    # Display filtered data (previews)
    st.subheader("Trips Ending at Crate and Barrel Flagship Store")
    st.dataframe(filtered_trips_df.head(1000), use_container_width=True)  

    # Compute counts of short and long trips
    num_short_trips = short_trips_df.shape[0]
    num_long_trips = long_trips_df.shape[0]

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
    trips_by_hour_df = trips_by_hour_df.sort_values(by='hour')
    fig = go.Figure(data=[go.Bar(x=trips_by_hour_df['hour'], y=trips_by_hour_df['number_of_trips'])])
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

