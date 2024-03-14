import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pages import *

# 상태 저장
if "page" not in st.session_state:
    st.session_state["page"] = "HOME"

menus = {"HOME": home, "시간별(특정 역)": period, "시간별(전체)": period_all,"호선별(특정 역)": line,
          "호선별(전체)": line_all, "역 별(특정 호선)": station, "역 별(전체)": station_all}
with st.sidebar:
    for menu in menus:
        if st.button(menu, use_container_width=True, type = "primary" if st.session_state["page"] == menu else "secondary"):
            st.session_state["page"] = menu
            st.rerun()

    for menu in menus.keys():
        if st.session_state["page"] == menu:
            menus[menu]()