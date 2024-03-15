import streamlit as st
from pages import *

# 상태 저장
if "page" not in st.session_state:
    st.session_state["page"] = "HOME"

menus = {"HOME": home, "시간별(특정 역)": period, "시간별(전체)": period_all,"호선별(특정 역)": line,
          "역별(특정 시간)": line_all, "역별(전체)": station_all, "💬 챗봇": chatbot}
with st.sidebar:
    for menu in menus:
        if st.button(menu, use_container_width=True, type = "primary" if st.session_state["page"] == menu else "secondary"):
            st.session_state["page"] = menu
            st.rerun()

st.sidebar.title("TECHIT 백엔드 스쿨 9기")
st.sidebar.subheader("서울 지하철 혼잡도 데이터 대시보드")
st.sidebar.text("1차 프로젝트")
st.sidebar.link_button(":computer: GitHub", "https://github.com/G0LDF0X/Seoul_Metro_Project")
st.sidebar.video("https://youtu.be/ulDltzR-ljI?si=rStHV8akn4nZI-64")

for menu in menus.keys():
    if st.session_state["page"] == menu:
        menus[menu]()