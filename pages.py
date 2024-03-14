import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import time

@st.cache_data
def load_data():
    data = pd.read_csv("")
    return data

data = load_data()

# 홈 화면
def home():
    pass

# 시간별(특정 역)
def period():
    pass

# 시간별(전체)
def period_all():
    pass

# 호선별(특정 역)
def line():
    pass

# 호선별(전체)
def line_all():
    pass

# 역 별(특정 호선)
def station():
    pass

# 역 별(전체)
def station_all():
    pass