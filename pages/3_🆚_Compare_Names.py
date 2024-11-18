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

st.set_page_config(page_title="Name Comparison over Time", page_icon="🆚")

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
    data['pct'] = data['count'] / data.groupby('year')['count'].transform('sum')
    return data

def get_name():
    val = get_random_name(data)

data = load_name_data()


st.markdown("# Compare Name Popularity")
st.sidebar.header("Compare Names over Time")
st.markdown('*Enter 2 names to see to compare their popularity over time!*')
st.write('')

if 'input_name1' not in st.session_state:
    st.session_state.input_name1 = ""

if 'input_name2' not in st.session_state:
    st.session_state.input_name2 = ""

with st.sidebar:
    input_name1 = st.text_input('Enter Name 1:', value=st.session_state.input_name1)
    input_name2 = st.text_input('Enter Name 2:', value=st.session_state.input_name2)

if len(input_name1) > 0:

    chart_placeholder = st.empty()

try:
    fig = names_trend_line(data, [input_name1, input_name2])
    with chart_placeholder.container():
        st.plotly_chart(fig)

except:
    None
