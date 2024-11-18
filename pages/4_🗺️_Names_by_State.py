import numpy as np
import pandas as pd
import zipfile
import requests
from io import BytesIO
import plotly.express as px
import streamlit as st
from my_plots import *


st.set_page_config(page_title="Top Names Map", page_icon="🗺️", layout='wide')

#@st.cache_data
#def load_state_name_data():
#    data = pd.read_csv('map_data.zip')
#    return data

#data = load_state_name_data()

@st.cache_data
def read_csv_from_zip(zip_file_path, csv_file_name):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        with zip_ref.open(csv_file_name) as csv_file:
            df = pd.read_csv(csv_file)
            return df

data = read_csv_from_zip('map_data.zip', 'map_data.csv')

st.markdown("# Top Names by State")
st.sidebar.header("Top Names by State")
st.markdown('*Select a State and a Year to see Top Names!*')
st.write('')

if 'input_year' not in st.session_state:
    st.session_state.input_year = ""

if 'input_state' not in st.session_state:
    st.session_state.input_state = ""
  
col1, col2 = st.columns(2)
with col1:
    state = st.selectbox('Select State:', data['name2'].unique())
    
with col2:
    year = st.selectbox('Select Year:', sorted(data['year'].unique(), reverse=True))

with st.sidebar:
    n_names = st.number_input('Number of Names to Display (per sex)', value = 5)
    try:
        st.write(f"State: {state}")
    except: st.empty()
    try:
        st.write(f"Year: {year}")
    except: st.empty()



map_placeholder = st.empty()


state_coords_f = data[data['name2']==state]

fig = top_names_state_plot(state_coords_f, year = year, n = n_names, state = state)


with map_placeholder.container():
    try:
        st.write('')
        st.markdown(f'### Top Names for {state} in {year}')
        st.plotly_chart(fig)
        #if(state == 'Alaska' or state == 'Texas'):
        #    st.map(state_coords_f, zoom = 3, size= 100)
        #else:
        #    st.map(state_coords_f, zoom = 5, size = 100)
            

    except:
        None


