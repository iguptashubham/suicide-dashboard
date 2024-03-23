#import dependencies

import numpy as np
import pandas as pd
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go
import json 
import urllib.request

st.set_page_config( page_icon='🪦',page_title='Suicide in India', layout = 'wide',)
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

df = pd.read_parquet('(preprocessed)Suicides_in_India(2001-2012).parquet')

col1, col2 = st.columns([0.7,0.3])

with col1:
  st.markdown('# :red[⚥ Suicides] in India (2019-2023)', unsafe_allow_html=True)
with col2:
  year = st.selectbox(options=list(df['Year'].unique()),label= '')
  st.write('Select the Year')

c1, c2 = st.columns([0.7,0.3])

with c1:
  st.write('Suicide is the third leading cause of death among young adults worldwide. There is a growing recognition that prevention strategies need to be tailored to the region-specific demographics of a country and to be implemented in a culturally-sensitive manner. This review explores the historical, epidemiological and demographic factors of suicide in India and examines the strategies aimed at the prevention of suicide. There has been an increase in the rates of suicide in India over the years, although trends of both increases and decline in suicide rates have been present. ')
  
  cl1, cl2 = st.columns([0.7,0.3])
  
  with cl1:
    st.markdown('##### India heatmap with least to :red[Most Suicides Cases]', unsafe_allow_html=True)
    st.markdown('India map showing shows states with sucide caes. darker the color high the suicides')
    filterdf2 = df[df['Year']==year].groupby(['State'])['Total'].sum().reset_index()
    filterdf2.columns = ['State','Total Suicides']
    geojson_url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
    
    with urllib.request.urlopen(geojson_url) as response:
      india_geojson = json.load(response)
      
    fig2 = px.choropleth(filterdf2,geojson=india_geojson,locations='State',featureidkey='properties.ST_NM', color='Total Suicides',color_continuous_scale='Reds')

    fig2.update_geos(
    visible=False,  # Hide the base map
    projection_scale=5,  # Adjust the scale for better visibility
    center={'lat': 22, 'lon': 80},  # Set the center coordinates for India
    scope='asia')
    
    st.plotly_chart(fig2, use_container_width=True)
    
  with cl2:
    st.markdown('##### States with total Suicides')
    df2 = df.query('State not in ["Total (All India)", "Total (States)", "Total (Uts)"]')
    filterdf3 = df2[df2['Year']==year].groupby('State')['Total'].sum().sort_values(ascending = False).reset_index().tail(35)
    st.dataframe(filterdf3,hide_index=True ,use_container_width=True)
    
  cl3, cl4 = st.columns([0.4,0.6])
  
  with cl3:
    st.markdown('##### :red[Suicides] Reason Distribution', unsafe_allow_html=True)
    option2 = st.selectbox(options = list(df['Type_code'].unique()), label='Sucide Reason')
    df4 = df[df['Type_code'] == option2]
    df5 = df4['Type'].value_counts()
    fig4 = px.pie(df5, values=df5.values, labels=df5.index, names=df5.index)
    fig4.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1], hole=0.4)
    fig4.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0, t=0))
    st.plotly_chart(fig4, use_container_width=True)

  with cl4:
    st.markdown('##### :red[Suicides] throughout the year', unsafe_allow_html=True)
    st.write('This graph show the sucidies cases through year 2019-2023')
    df3 = df4.groupby('Year')['Total'].sum().reset_index()
    fig3 = px.line(df3, x = 'Year', y='Total')
    st.plotly_chart(fig3, use_container_width=True)

  
with c2:
  st.markdown('##### Distribution of :red[Reason Type of Suicide]', unsafe_allow_html=True)
  st.write('Suicide is a complex issue influenced by various socio-economic, cultural, and psychological factors. Understanding the reasons behind suicidal tendencies is crucial for prevention and intervention efforts. Here’s a breakdown of the different categories of suicide reasons:')
  typedf = df['Type_code'].value_counts(ascending=True).reset_index()
  fig1 = px.pie(typedf, values='count', names='Type_code')
  fig1.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1], hole=0.4)
  fig1.update_layout(showlegend=False, margin=dict(l=0, r=0, b=0, t=0))
  st.plotly_chart(fig1, use_container_width=True)
  st.write('Distribution of Reason Type of Suicide is highest in Causes with 46%, Adopted with 28.3%, Professional Profile with 20.7%, Education with 3.07% and lowest with social status with 1.92%')
  
  c3 = st.columns(1)
  
  st.markdown('##### :red[Sucide cases] among the Age group')
  df6 = df4.groupby(['Age_group'])['Total'].sum().reset_index()
  fig5 = px.bar(df6,x = 'Age_group', y = 'Total')
  st.plotly_chart(fig5, use_container_width=True)






