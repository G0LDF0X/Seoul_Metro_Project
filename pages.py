import streamlit as st
import pandas as pd
from streamlit_folium import st_folium
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import time
from datetime import datetime, timedelta

plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False

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
color_data = {"1호선":"#0032A0", "2호선":"#00B140", "3호선":"#FC4C02", "4호선":"#00A9E0", "5호선":"#A05EB5",
              "6호선":"#A9431E", "7호선":"#67823A", "8호선":"E31C79", "혼잡도 34%": "#FF0000"}

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

    search_date = datetime.today()
    st.title("특정 역의 시간별 분석")

    # 날짜 선택
    search_date = st.date_input("검색하고자 하는 날짜를 입력해주세요.", search_date)
    st.caption("날짜를 선택하지 않을 경우 기본적으로 오늘을 선택합니다.")

    # 검색하는 날짜가 평일인지 토요일인지 일요일인지 체크
    if search_date.weekday() == 5:
        weekday = "토요일"
    elif search_date.weekday() == 6:
        weekday = "일요일"
    else:
        weekday = "평일"

    data_today = data[data["요일구분"] == weekday]

    # 비교할 역 선택
    station_select = st.selectbox("역을 선택해주세요.", station_list, index = None, placeholder="역 이름(상하선 구분)")
    station_data = data_today[data_today["역명"] == station_select]

    # 호선 선택
    line_selects = st.multiselect("호선을 선택해주세요.", station_data["호선"].unique(), placeholder="해당 역을 지나는 지하철 호선")
    graph_data = station_data[station_data["호선"].isin(line_selects)].set_index(keys="호선").iloc[:, 5:-1]

    # 그래프 그리기
    matplot_data = graph_data.T

    fig = plt.figure()
    plt.title("{} 시간에 따른 지하철 복잡도".format(search_date))
    plt.xlabel("시간")
    plt.ylabel("복잡도")
    for line in line_selects:
        plt.plot(matplot_data.index, matplot_data[line], label=line, linestyle="-", color=color_data[line])
    plt.xticks(fontsize=5, rotation=45)
    plt.yticks(fontsize=7)
    plt.plot(matplot_data.index, [34.0] * len(matplot_data), label="혼잡도 34%", linestyle=":", color="red")
    plt.legend(loc="best")
    # plt.grid(True)
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