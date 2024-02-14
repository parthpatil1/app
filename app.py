# importing libraries
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px


# setting page configuration
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# reading csv files
Delhi = pd.read_csv('delhi.csv', parse_dates=['time'])
kuala_lumpur = pd.read_csv(
    'kuala_lumpur.csv', parse_dates=['time'])
Singapore = pd.read_csv(
    'singapore.csv', parse_dates=['time'])
Tokyo = pd.read_csv('Tokyo.csv', parse_dates=['time'])

# defining function
def rt_chart(City):
    # creating date,month and year column
    City['date'] = pd.DatetimeIndex(City['time']).day
    City['month'] = pd.DatetimeIndex(City['time']).month
    City['year'] = pd.DatetimeIndex(City['time']).year

    # rainfall analysis
    st.header('Rainfall Analysis')
    st.subheader('Over the Past 40 Years')
    col1, col2 = st.columns(2, gap='large')
    with col1:
        Year = st.slider('Choose Year', min_value=1980, max_value=2022, key=1)
        st.write('The selected Year is', Year)
    with col2:
        if Year == 2022:
            Month = st.slider('Choose Month', min_value=1, max_value=10, key=5)
        else:
            Month = st.slider('Choose Month', min_value=1, max_value=12, key=2)
        st.write('The selected Month is', Month)

    col1, col2 = st.columns([3, 1], gap='large')
    with col1:
        tab1, tab2 = st.tabs(['Table', 'Chart'])
        with tab1:
            st.dataframe(City[(City['month'] == Month) & (
                City['year'] == Year)], height=350, width=1000)
        with tab2:
            rain_chart = alt.Chart(City[(City['month'] == Month) & (City['year'] == Year)]).mark_line().encode(
                x='date', y='rainfall', tooltip=[alt.Tooltip('date', title="Date"), alt.Tooltip('rainfall', title='Rainfall in mm')], color=alt.value('green')).interactive().properties(height=350, width=750)
            st.altair_chart(rain_chart)

    with col2:
        st.metric("Year", value=Year)
        st.metric('Month', value=Month)
        st.metric("Total Precipitation in mm", value=round(
            City[(City['month'] == Month) & (City['year'] == Year)]['rainfall'].sum(), 1))
    st.markdown('''---''')

    # Filtering data based on selected year and month
    filtered_data = City[(City['year'] == Year) & (City['month'] == Month)]

    # Rainfall line chart
    st.write('Rainfall Trend:')
    rain_chart = alt.Chart(filtered_data).mark_line().encode(
        x='date',
        y='rainfall',
        tooltip=['date', 'rainfall']
    ).properties(height=300, width=600)
    st.altair_chart(rain_chart)

    # 3D Scatter plot
    st.header('3D Scatter Plot')
    scatter_data = City[['year', 'month', 'rainfall']]
    fig = px.scatter_3d(scatter_data, x='year', y='month', z='rainfall', color='rainfall')
    st.plotly_chart(fig)

    # Pie chart for rainfall distribution by month
    st.header('Rainfall Distribution by Month')
    pie_data = City.groupby('month').sum(numeric_only=True)['rainfall']
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    st.pyplot(fig)


    # temperature analysis
    st.header('Temperature over 40 years')

    Year = st.slider('Choose Year', min_value=1980, max_value=2022, key=3)
    st.write('The selected Year is', Year)

    col1, col2 = st.columns([3, 1], gap='large')
    with col1:
        tab1, tab2 = st.tabs(['Table', 'Chart',])
        with tab1:
            st.dataframe(City[City['year'] == Year])
        with tab2:
            temp_chart = alt.Chart(City[City['year'] == Year]).mark_rect().encode(x='date:O', y='month:O', color=alt.Color('avg_temp', scale=alt.Scale(scheme="inferno")), tooltip=[
                alt.Tooltip('date', title="Date"), alt.Tooltip('avg_temp', title='Average Temperature in °C')]).properties(height=450, width=750)
            st.altair_chart(temp_chart)
        


    with col2:
        st.metric('Year', value=Year)
        st.metric('Maximum tempertature in °C',
                  value=City[City['year'] == Year]['max_temp'].max())
        st.metric('Minimum tempertature in °C',
                  value=City[City['year'] == Year]['min_temp'].min())

    #Average tempertaure bar chartt 
    st.write('Average Temperature Trend:')
    temp_chart = alt.Chart(City).mark_rect().encode(
        x='date:O',
        y='month:O',
        color=alt.Color('avg_temp', scale=alt.Scale(scheme="inferno")),
        tooltip=['date', 'avg_temp']
    ).properties(height=400, width=800)
    st.altair_chart(temp_chart)
     
    
    
    # Bar graph for average temperature by year
    st.header('Average Temperature by Year')
    bar_data = City.groupby('year').mean()['avg_temp']
    fig, ax = plt.subplots()
    ax.bar(bar_data.index, bar_data)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average Temperature (°C)')
    st.pyplot(fig)
             


# Sidebar
st.sidebar.title('Climatic Changes')
image = 'https://www.noaa.gov/sites/default/files/styles/landscape_width_1275/public/2022-03/PHOTO-Climate-Collage-Diagonal-Design-NOAA-Communications-NO-NOAA-Logo.jpg'
st.sidebar.image(image)
st.sidebar.markdown('''
> Climate change refers to long-term shifts in temperatures and weather patterns. It also includes sea level rise, changes in weather patterns like drought and flooding, and much more.
---
''')
selected_city = st.sidebar.selectbox(
    'Select a City:', ('Delhi', 'Kuala Lumpur', 'Singapore', 'Tokyo'))
st.sidebar.markdown(
    'Here is an analysis of the weather data for four cities in Asia for 20 years.')


# Main Dashboard
st.title("Weather Data Analysis")


if selected_city == 'Delhi':
    st.markdown('''
    # Weather Dashboard - ***Delhi*** 
    > Delhi, the capital of India, is one of the most populous and polluted cities in the world. The city has changed a lot over the years with respect to its weather. There have been a number of factors that have contributed to this change, including climate change. Here is a dashboard for the analysis of weather data for 20 years.
    ---
    ''')
    rt_chart(Delhi)
elif selected_city == 'Kuala Lumpur':
    st.markdown('''
    # Weather Data Dashboard - ***Kuala Lumpur***
    > Kaula Lumpur, the capital city of Malaysia, home to the iconic Twin Towers. Kuala Lumpur is best known for its affordable luxury hotels, great shopping scene, and even better food. Malaysian capital boasts some of the finest shopping centers in the world, head towards Pavilion KL and Suria KLC for high-end luxurious items, or visit Petaling Street to have a real sense of local shopping. The city has changed a lot over the years with respect to its weather. There have been a number of factors that have contributed to this change, including climate change. Here is a dashboard for the analysis of weather data for 20 years.
    ---
    ''')
    rt_chart(kuala_lumpur)
elif selected_city == 'Singapore':
    st.markdown('''
    # Weather Data Dashboard - ***Singapore***
    > Singapore, officially the Republic of Singapore, is a sovereign island country and city-state in maritime Southeast Asia. It is famous for being a global financial center, being among the most densely populated places in the world, having a world-class city airport with a waterfall, and a Botanic Garden that is a World Heritage Site. The city has changed a lot over the years with respect to its weather. There have been a number of factors that have contributed to this change, including climate change. Here is a dashboard for the analysis of weather data for 20 years.
    ''')
    rt_chart(Singapore)
else:
    st.markdown('''
    # Weather Data Dashboard - ***Tokyo***
    > Tokyo, Japan’s busy capital, mixes the ultramodern and the traditional, from neon-lit skyscrapers to historic temples. The city has changed a lot over the years with respect to its weather. There have been a number of factors that have contributed to this change, including climate change. Here is a dashboard for the analysis of weather data for 20 years.
    ''')
    rt_chart(Tokyo)
