import streamlit as st
from pages import *

# 상태 저장
if "page" not in st.session_state:
    st.session_state["page"] = "HOME"

menus = {"HOME": home, "시간별(특정 역)": period, "시간별(전체)": period_all,"호선별(특정 역)": line,
          "역별(특정 호선)": line_all, "역 별(전체)": station_all}
with st.sidebar:
    for menu in menus:
        if st.button(menu, use_container_width=True, type = "primary" if st.session_state["page"] == menu else "secondary"):
            st.session_state["page"] = menu
            st.rerun()

st.sidebar.title("TECHIT 백엔드 스쿨 9기")
st.sidebar.subheader("서울 지하철 혼잡도 데이터 대시보드")
st.sidebar.text("1차 프로젝트")

for menu in menus.keys():
    if st.session_state["page"] == menu:
        menus[menu]()