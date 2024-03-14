import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import time

@st.cache_data
def load_data():
    data = pd.read_csv("서울교통공사_지하철혼잡도정보_20231231.csv", encoding="cp949")
    return data

data = load_data()

def txt_gen(txt):
    for t in list(txt):
        yield t
        time.sleep(0.02)

# 홈 화면
def home():
    HOME_TITLE = "서울교통공사 지하철 혼잡도 정보"
    st.caption(HOME_TITLE)
    st.subheader("데이터 정보")
    st.info("지하철 혼잡도 정보(수정:2024-02-22)")
    st.divider()
    
    txt = """본 데이터는 서울교통공사가 제공하는 1-8호선의 30분의 정원대비 승차 인원을 혼잡도로 산정하여 작성된 데이터입니다. 승차인과 좌석 수가 일치할 경우 혼잡도를 34%로 산정했습니다.
    해당 데이터는 요일구분(평일, 토요일, 일요일), 호선, 역번호, 역명, 상하선구분, 30분단위 별 혼잡도 데이터로 구성되어 있습니다."""
    st.write_stream(txt_gen(txt))
    st.divider()
    st.markdown("#### ▼ 지하철 혼잡도 정보")
    st.dataframe(data)

# 시간별(특정 역)
def period():
    st.title("특정 역의 시간별 분석")
    pass

# 시간별(전체)
def period_all():
    st.title("전체 역의 시간별 분석")
    pass

# 호선별(특정 역)
def line():
    st.title("특정 역의 호선별 분석")
    pass

# 호선별(전체)
def line_all():
    st.title("전체 역의 호선별 분석")
    pass

# 역 별(특정 호선)
def station():
    st.title("특정 호선의 시간대에 따른 역별 분석")
    pass

# 역 별(전체)
def station_all():
    st.title("특정 호선의 전체 시간의 역별 분석")
    pass