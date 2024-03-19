import streamlit as st
import pandas as pd
# from streamlit_folium import st_folium
# import folium
import matplotlib.pyplot as plt
import time
from datetime import timedelta, datetime
import requests
import os
# from dotenv import load_dotenv
import json
from collections import defaultdict
import matplotlib.font_manager as fm
from app_func import *

@st.cache_data
def fontRegistered():
    font_dirs = [os.getcwd() + '/customFonts']
    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)
    fm._load_fontmanager(try_read_cache=False)

fontRegistered()
plt.rc('font', family="NanumGothic")
plt.rcParams['axes.unicode_minus'] =False

@st.cache_data
def load_data():

    # 기존 방식: csv로 가져오기
    # data = pd.read_csv("서울교통공사_지하철혼잡도정보_20231231.csv", encoding="cp949")

    # dotenv를 이용한 API 호출
    # load_dotenv()
    # data_api_key = os.getenv("DATA_API_KEY")

    # Streamlit에서 쓰는 API 호출
    data_api_key = st.secrets["DATA_API_KEY"]

    URL = "http://api.odcloud.kr/api/15071311/v1/uddi:e477f1d9-2c3a-4dc8-b147-a55584583fa2?page=1&perPage=5000&serviceKey={}".format(data_api_key)
    response = requests.get(URL)
    contents = response.text
    json_data = json.loads(contents)
    data = pd.json_normalize(json_data["data"])
    data = data[['연번', '요일구분', '호선', '역번호', '출발역', '상하구분', '5시30분', '6시00분', '6시30분', '7시00분', '7시30분', '8시00분', '8시30분', 
                 '9시00분', '9시30분', '10시00분', '10시30분', '11시00분', '11시30분', '12시00분', '12시30분', '13시00분', '13시30분', '14시00분', '14시30분', 
                 '15시00분', '15시30분', '16시00분', '16시30분', '17시00분', '17시30분', '18시00분', '18시30분', '19시00분', '19시30분', '20시00분', '20시30분', 
                 '21시00분', '21시30분', '22시00분', '22시30분', '23시00분', '23시30분', '00시00분', '00시30분', '01시00분']]
    data["역명"] = data.apply(lambda x: x["출발역"] + " " + x["상하구분"], axis=1)
    data["호선"] = data["호선"].astype(str) + "호선"
    return data

data = load_data()
line_list = data["호선"].unique()
station_list = data["역명"].unique()
time_list = data.columns[6:-1]
color_data = {"1호선":"#0032A0", "2호선":"#00B140", "3호선":"#FC4C02", "4호선":"#00A9E0", "5호선":"#A05EB5",
              "6호선":"#A9431E", "7호선":"#67823A", "8호선":"#E31C79", "혼잡도 34%": "#FF0000"}

def txt_gen(txt):
    for t in list(txt):
        yield t
        time.sleep(0.02)

# 홈 화면
def home():
    st.markdown("## :metro: 서울 지하철 혼잡도 대시보드")
    st.caption("서울교통공사에서 공공데이터 포털에 정보 제공")
    st.page_link("https://www.data.go.kr/data/15071311/fileData.do#tab-layer-file", label = "공공데이터 포털(Link)", icon="ℹ️")
    st.info("데이터 최종 수정 : 2024-02-22")
    st.divider()
    
    txt = """본 데이터는 서울교통공사가 제공하는 1-8호선의 30분의 정원대비 승차 인원을 혼잡도로 산정하여 작성된 데이터입니다. 승차인과 좌석 수가 일치할 경우 혼잡도를 34%로 산정했습니다.
    해당 데이터는 요일구분(평일, 토요일, 일요일), 호선, 역번호, 역명, 상하선구분, 30분단위 별 혼잡도 데이터로 구성되어 있습니다.
    해당 데이터를 시간별, 호선별, 역별로 가공하여 분석하여 데이터 대시보드를 제작하였습니다."""
    st.write_stream(txt_gen(txt))
    st.divider()
    st.markdown("#### ▼ 지하철 혼잡도 정보")

    # Streamlit 서버는 로컬 시간과 달라서 9시간을 더해줘야함
    now_time = (datetime.now() + timedelta(hours=9)).strftime("%H-%M")
    time_split = now_time.split("-")
    hour, minute = int(time_split[0]), int(time_split[1])
    if minute >= 0 and minute < 30:
        minute = "00분"
    else:
        minute = "30분"
    
    if hour <= 1:
        hour = "0" + str(hour) + "시"
    else:
        hour = str(hour) + "시"
        
    time_str = hour + minute
    df = defaultdict(list)
    for line in line_list:
        line_data = data[data["호선"] == line]
        line_remove_zero_data = line_data[line_data[time_str].astype("float") != 0.0]
        line_max = line_remove_zero_data[time_str].astype("float").max()
        line_min = line_remove_zero_data[time_str].astype("float").min()

        df["호선"].append(line)
        df["최대"].append(line_max)
        df["최소"].append(line_min)
    
    df = pd.DataFrame(df).set_index(keys="호선")

    st.info("💡 데이터는 30분마다 갱신됩니다.")
    st.markdown("**현재 시각 전 호선 복잡도 :**")
    st.caption("(0.0으로 표기되는 곳 제외)")
    st.dataframe(df.T, use_container_width=True)


    not_zero_data = data[data[time_str].astype("float") != 0.0]
    float_data = not_zero_data[time_str].astype("float")
    no_nan_data = float_data.dropna(axis=0)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**현재 가장 혼잡한 곳 :**")

        max_result = no_nan_data.max()
        max_data = data[data[time_str].astype("float") == max_result]

        for index, row in max_data.iterrows():
            st.write(row["호선"], row["역명"], ":", max_result)

    with col2:
        st.markdown("**현재 가장 한가한 곳 :**")
        

        min_result = no_nan_data.min()
        min_data = data[data[time_str].astype("float") == min_result]

        for index, row in min_data.iterrows():
            st.write(row["호선"], row["역명"], ":", min_result)
        st.caption("(0.0으로 표기되는 곳 제외)")

# 시간별(특정 역)
def period():
    st.title("⏲️ 특정 역의 시간별 분석")

    # 날짜 선택
    data_today, search_date = date_select(data)

    # 비교할 역 선택
    station_data, select_station = station_select(data_today, station_list)

    # 호선 선택
    graph_data, line_selects = multi_line_select(station_data)

    # 그래프 그리기
    matplot_data = graph_data.T

    fig = plt.figure()
    plt.title("{} 시간에 따른 {} 지하철 혼잡도".format(search_date, select_station))
    plt.xlabel("시간")
    plt.ylabel("혼잡도")
    plt.xticks(fontsize=5, rotation=45)
    plt.yticks(fontsize=7)
    plt.plot(matplot_data.index, [34.0] * len(matplot_data), label="혼잡도 34%", linestyle=":", color="red")
    plt.legend(loc="best")

    for line in line_selects:
        plt.plot(matplot_data.index, matplot_data[line], label=line, linestyle="-", color=color_data[line])
    
    st.pyplot(fig)

    """
    아래쪽에 있는 내용은 matplotlib를 사용하지 않고, Streamlit에서 제공되는 line_chart를 시도해보았던 내용이다.
    하지만 편의성 면에서 matplotlib가 훨씬 좋기 때문에 사용하지 않고 주석처리만 한다.
    """
    # Streamlit에서 line_chart의 자동 정렬 문제를 해결하기 위해, 임의로 시간 앞에 날짜를 붙여주기로 했다.
    # tmp_data = graph_data.iloc[:,6:-1].transpose()
    # index_list = tmp_data.index
    # index_list = list(index_list)
    # for i in range(len(index_list)):
    #     if i >= 37:
    #         index_list[i] = (search_date + timedelta(days=1)).strftime("%Y-%m-%d") + " " + index_list[i]
    #     elif i <= 8:
    #         index_list[i] = search_date.strftime("%Y-%m-%d") + " 0" + index_list[i]
    #     else:
    #         index_list[i] = search_date.strftime("%Y-%m-%d") + " " + index_list[i]

    # tmp_data.index = sorted(index_list)
    
    # # 승차인 = 좌석 수를 나타내는 기준 34%를 표기
    # tmp_data["혼잡도 34%"] = 34.0

    # # 지하철 호선에 맞게 칠해주기
    # color_list = []
    # for line in line_selects:
    #     color_list.append(color_data[line])

    # color_list.append(color_data["혼잡도 34%"])
    # st.line_chart(tmp_data, color=color_list, use_container_width=True)


# 시간별(전체)
def period_all():
    st.title("⏲️ 전체 역의 평균 시간별 분석")
    st.info("해당 데이터는 각 호선의 평균을 사용했습니다.")
    
    data_today, search_date = date_select(data)

    # 호선 선택
    line_selects = st.multiselect("호선을 선택해주세요.", data_today["호선"].unique(), placeholder="평균을 확인 할 지하철 호선")

    # 그래프 그리기
    fig = plt.figure()
    plt.title("{} 시간에 따른 전체 역 평균 지하철 혼잡도".format(search_date))
    plt.xlabel("시간")
    plt.ylabel("혼잡도")

    # 호선을 여러 개 선택했을 경우
    for line in line_selects:
        graph_data = data_today[data_today["호선"] == line].iloc[:, 6:-1].astype("float")
        matplot_data = graph_data.describe().T[["mean"]]
        plt.plot(matplot_data.index, matplot_data["mean"], label = "{} 평균".format(line), color=color_data[line])

    plt.xticks(fontsize=5, rotation=45)
    plt.yticks(fontsize=7)
    plt.plot(time_list, [34.0] * len(time_list), label="혼잡도 34%", linestyle=":", color="red")
    plt.legend(loc="best")
    st.pyplot(fig)

# 호선별(특정 역)
def line():
    st.title("🚇 특정 역의 특정 시간대 호선별 분석")

    # 날짜 선택
    data_today, search_date = date_select(data)

    # 비교할 역 선택
    station_data, select_station = station_select(data_today, station_list)

    # 비교 시간 선택
    time_data, select_time = time_select(station_data, time_list)
     
    st.info("해당 역에 지하철이 하나만 다닐 경우에는 혼잡도 34% 선이 보이지 않습니다.")

    # 그래프 그리기
    fig = plt.figure()
    plt.title("{} {} {} 지하철 혼잡도".format(search_date, select_time, select_station))
    plt.xlabel("호선")
    plt.ylabel("혼잡도")
    plt.xticks(fontsize=7, rotation=45)
    plt.yticks(fontsize=7)
    plt.legend(loc="best")

    # 막대 그래프
    plt.bar(time_data["호선"], time_data[select_time])

    # 선그래프
    plt.plot(time_data["호선"], [34.0] * len(time_data["호선"]), label="혼잡도 34%", linestyle=":", color="red")
    
    st.pyplot(fig)

# 역별(특정 시간)
def line_all():
    st.title("🚉 특정 호선의 특정 시간대 역별 분석")

    # 날짜 선택
    data_today, search_date = date_select(data)

    data_today["역번호"] = data_today["역번호"].astype("float")
    data_today = data_today.sort_values(by="역번호", ascending=False)

    # 호선 선택
    line_data, select_line = line_select(data_today)

    # 비교 시간 선택
    time_data, select_time = time_select(line_data, time_list)

    time_data["역명"] = time_data["역명"].astype("category")
    time_data[select_time] = time_data[select_time].astype("float")

    st.info("해당 데이터는 실제 노선 진행 방향과는 상관 없이, 역 번호 순으로 정렬되었습니다.")
    
    # 그래프 그리기
    fig = plt.figure(figsize=(10, 20))
    plt.title("{} {} 지하철 혼잡도".format(search_date, select_time, select_line))
    plt.xlabel("혼잡도")
    plt.ylabel("역 이름")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc="best")

    # 막대 그래프
    plt.barh(time_data["역명"], time_data[select_time], color=color_data[select_line])

    # 선그래프
    plt.plot([34.0] * len(time_data["역명"]), time_data["역명"], label="혼잡도 34%", linestyle=":", color=color_data["혼잡도 34%"])
    
    st.pyplot(fig)


# 역 별(전체)
def station_all():
    st.title("🚉 특정 호선의 전체 시간 평균 역별 분석")

    # 날짜 선택
    data_today, search_date = date_select(data)

    # iloc으로 데이터를 자르기 전에 역번호 순으로 데이터를 정렬
    data_today["역번호"] = data_today["역번호"].astype("float")
    data_today = data_today.sort_values(by="역번호", ascending=False)

    # 호선 선택
    select_line = st.selectbox("호선을 선택해주세요.", line_list, placeholder="해당 역을 지나는 지하철 호선")
    line_data = data_today[data_today["호선"] == select_line].set_index(keys="역명").iloc[:,6:-1].astype("float")
    matplot_data = line_data.T.describe().T
    
    st.info("해당 데이터는 실제 노선 진행 방향과는 상관 없이, 역 번호 순으로 정렬되었습니다.")

    fig = plt.figure(figsize=(10, 20))
    plt.title("{} {} 전체 시각 평균 지하철 혼잡도".format(search_date, select_line))
    plt.xlabel("혼잡도")
    plt.ylabel("역 이름")
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.legend(loc="best")
    
    plt.barh(matplot_data.index, matplot_data["mean"], color=color_data[select_line])

    # 혼잡도 34% 기준
    plt.plot([34.0] * len(matplot_data.index), matplot_data.index, label="혼잡도 34%", linestyle=":", color="red")
    st.pyplot(fig)

def page_search():
    st.title("🔍 혼잡도 검색")
    st.caption("검색하려는 날짜와 역, 호선과 시간대를 입력하고 검색 버튼을 누르면 해당 데이터에 따른 혼잡도를 보여줍니다.")

    # 시간 검색
    date_data, search_date = date_select(data)

    # 역 검색
    station_data, select_station = station_select(date_data, station_list)

    # 호선 선택
    line_data, select_line = line_select(station_data)

    # 시간 선택
    time_data, select_time = time_select(line_data, time_list)

    if st.button("검색", use_container_width=True, type = "primary"):
            check_time = time_data[select_time]
            st.write(search_date, select_station, select_line, select_time, "혼잡도 :", check_time[0].astype(str))