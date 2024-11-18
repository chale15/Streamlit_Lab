import numpy as np
import pandas as pd
import zipfile
import plotly.express as px
import matplotlib.pyplot as plt
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from my_plots import *
import streamlit as st

st.set_page_config(page_title="Name Popularity over Time", page_icon="📈")

@st.cache_data
def load_name_data():
    names_file = 'https://www.ssa.gov/oact/babynames/names.zip'
    response = requests.get(names_file)
    with zipfile.ZipFile(BytesIO(response.content)) as z:
        dfs = []
        files = [file for file in z.namelist() if file.endswith('.txt')]
        for file in files:
            with z.open(file) as f:
                df = pd.read_csv(f, header=None)
                df.columns = ['name','sex','count']
                df['year'] = int(file[3:7])
                dfs.append(df)
        data = pd.concat(dfs, ignore_index=True)
    data['pct'] = data['count'] / data.groupby(['year', 'sex'])['count'].transform('sum')
    return data

def get_name():
    val = get_random_name(data)

data = load_name_data()


st.markdown("# Name Popularity over Time")
st.sidebar.header("Name Popularity over Time")
st.markdown('*Enter a name to see a plot of its popularity over time!*')
st.write('')

if 'input_name' not in st.session_state:
    st.session_state.input_name = ""

with st.sidebar:
    input_name = st.text_input('Enter a name:', value=st.session_state.input_name)
        
    if st.button("Random Name"):
        random_name = get_random_name(data)
        st.session_state.input_name = random_name
        st.experimental_rerun()



chart_placeholder = st.empty()

try:
    stats = name_trend_stats(data, input_name)
    if len(stats)==0:
        st.write(f"No Occurrances of the Name {input_name} Found")
    else:
        st.write(f"First Recorded Occurrance of Name: {stats[0]}")
        st.write(f"Peak Popularity: {stats[2]}  ({stats[1]})")

    fig = name_trend_line(data, input_name)
    with chart_placeholder.container():
        st.plotly_chart(fig)

except:
    None
