import streamlit as st
from datetime import datetime

# 날짜 선택하기
def date_select(input_data):
    today_date = datetime.today()
    search_date = st.date_input("검색하고자 하는 날짜를 입력해주세요.", today_date)

    # 검색하는 날짜가 평일인지 토요일인지 일요일인지 체크
    if search_date.weekday() == 5:
        weekday = "토요일"
    elif search_date.weekday() == 6:
        weekday = "일요일"
    else:
        weekday = "평일"

    data_today = input_data[input_data["요일구분"] == weekday]
    return data_today, search_date

# 역 선택하기
def station_select(input_data, station_list):
    select_station = st.selectbox("역을 선택해주세요.", station_list, index = None, placeholder="역 이름(상하선 구분)")
    station_data = input_data[input_data["역명"] == select_station]
    return station_data, select_station
# 호선 여러개 선택하기
def multi_line_select(input_data):
    line_selects = st.multiselect("호선을 선택해주세요.", input_data["호선"].unique(), placeholder="해당 역을 지나는 지하철 호선")
    lines_data = input_data[input_data["호선"].isin(line_selects)].set_index(keys="호선").iloc[:, 5:-1].astype("float")
    return lines_data, line_selects

# 호선 단일 선택하기
def line_select(input_data):
    select_line = st.selectbox("호선을 선택해주세요.", input_data["호선"].unique(), placeholder="해당 역을 지나는 지하철 호선")
    line_data = input_data[input_data["호선"] == select_line]
    return line_data, select_line

# 시간 선택하기
def time_select(input_data, time_list):
    select_time = st.selectbox("시간을 선택해주세요.", time_list)
    time_data = input_data[["호선", "역명", select_time]]
    time_data[select_time] = time_data[select_time].astype("float")
    return time_data, select_time