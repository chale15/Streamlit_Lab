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

st.set_page_config(page_title="Top Names by Year", page_icon="🏅")

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

def random_year():
    year_input = get_random_year(data)

data = load_name_data()
year_val = 2000

st.markdown("# Top Names by Year")
st.sidebar.header("Top Names by Year")
st.markdown('*Discover the most popular baby names for any given year!*')
st.write('')
with st.sidebar:
    slider_placeholder = st.empty()

    if st.button("Random Year"):
        year_val = get_random_year(data)

    n_names = st.number_input('Number of Names to Display (per sex)', value = 5)


chart_placeholder = st.empty()


with slider_placeholder.container():
    year_input = st.slider('Year', min_value = 1880, max_value = 2023, value=year_val)


fig2 = top_names_plot(data, year=year_input, n=n_names)


with chart_placeholder.container():
    st.plotly_chart(fig2)

unique_male = len(data[(data['year']==year_input) & (data['sex']=='M')]['name'].unique())
unique_female = len(data[(data['year']==year_input) & (data['sex']=='F')]['name'].unique())

st.write(f"Number of Unique Male Names: {unique_male}")
st.write(f"Number of Unique Female Names: {unique_female}")
