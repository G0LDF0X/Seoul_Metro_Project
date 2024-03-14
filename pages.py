import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime, timedelta

@st.cache_data
def load_data():
    data = pd.read_csv("서울교통공사_지하철혼잡도정보_20231231.csv", encoding="cp949")
    data["역명"] = data.apply(lambda x: x["출발역"] + " " + x["상하구분"], axis=1)
    data["호선"] = data["호선"].astype(str) + "호선"
    return data

data = load_data()
line_list = data["호선"].unique()
station_list = data["역명"].unique()
time_list = data.columns[6:-1]

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
    # 오늘이 평일인지 토요일인지 일요일인지 체크
    if datetime.today().weekday() == 5:
        weekday = "토요일"
    elif datetime.today().weekday() == 6:
        weekday = "일요일"
    else:
        weekday = "평일"

    data_today = data[data["요일구분"] == weekday]

    # 비교할 역 선택
    station_select = st.selectbox("역을 선택해주세요.", station_list, index = None, placeholder="역명")

    # 임시로 보여주는 테이블 데이터
    station_data = data_today[data_today["역명"] == station_select]
    st.dataframe(station_data)

    # 호선 선택
    line_selects = st.multiselect("호선을 선택해주세요.", station_data["호선"].unique())
    graph_data = station_data[station_data["호선"].isin(line_selects)].set_index(keys="호선")

    # 시간 자동 정렬 문제를 해결하기 위해, 임의로 시간 앞에 날짜를 붙여주기로 했다.
    tmp_data = graph_data.iloc[:,6:-1].transpose()
    index_list = tmp_data.index
    index_list = list(index_list)
    for i in range(len(index_list)):
        if i >= 37:
            index_list[i] = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d") + " " + index_list[i]
        elif i <= 8:
            index_list[i] = datetime.today().strftime("%Y-%m-%d") + " 0" + index_list[i]
        else:
            index_list[i] = datetime.today().strftime("%Y-%m-%d") + " " + index_list[i]

    tmp_data.index = sorted(index_list)

    st.dataframe(graph_data)
    st.line_chart(graph_data.iloc[:,6:-1].transpose())
    st.line_chart(tmp_data)


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