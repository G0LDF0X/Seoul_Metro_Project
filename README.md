# Seoul_Metro_Project

본 프로젝트는 공공 데이터 포털에서 제공하는 "서울교통공사_지하철혼잡도정보" 정보를 기반으로 하여 시간별, 호선별 지하철의 복잡도를 나타내고 이를 다른 호선과 비교하거나 함께 볼 수 있도록, 그리고 챗봇을 이용해 어느 지하철을 탈 것인지 추천을 받는 것을 목표로 하고 있습니다.


### 목표하는 기능 구현
1. "서울교통공사_지하철혼잡도정보"를 CSV 파일로 받아 특정 역의 시간별 호선의 복잡도 데이터, 모든 역의 전체적인 시간별 호선의 복잡도 데이터, 특정 역의 호선별 복잡도 데이터, 모든 역의 전체적힌 호선별 복잡도 데이터, 특정 호선의 동일 시간대 역별 복잡도 데이터, 특정 호선의 전체적인 시간 대 역별 복잡도 데이터를 비교하기

2. 특정 역의 시간별 비교에서는 Select Box를 통해 비교할 역을 고르고, Multi Select 기능을 넣어 비교할 호선을 다수 선택할 수 있도록 하기 : 꺾은선 그래프를 통해 시간별 변화 추이 확인하기
3. 전체 역의 시간별 비교에서는 데이터의 평균 및 전반적인 통계값을 사용하며, Multi Select 기능만을 넣어 호선 별 비교할 수 있도록 하기 : 꺾은선 그래프를 통해 시간별 변화 추이 확인하기
4. 2와 3에서는 오늘의 날짜가 반영되며, 추후 Date input 기능을 통해 평일 / 토요일 / 일요일에 따른 데이터 변화 추이 보여주기

5. 특정 역의 호선별 비교에서는 Select Box를 통해 비교할 역을 고르고, 추가로 시간을 고를 Select Box를 추가하여 해당 시간에 해당 역을 지나는 모든 호선들의 복잡도를 비교하기 : 막대 그래프를 통해 복잡도 차이 확인하기
6. 전체 역의 호선별 비교에서는 데이터의 평균 및 전반적인 통계값을 사용하며, Multi Select를 통해 비교할 호선을 고르고 추가로 시간을 고를 Select Box를 추가하여, 해당 시간에 Multi Select로 선택한 호선의 전반적인 복잡도를 비교하기 : Violin plot이나 barplot을 확인하여 전반적인 통계값과 복잡도 차이가 잘 보이게 하기
7. 5와 6에서는 오늘의 날짜가 반영되며, 추후 Date input 기능을 통해 평일 / 토요일 / 일요일에 따른 데이터 변화 추이 보여주기

8. 특정 호선의 동일 시간 대 역별 복잡도 비교에서는 Select Box를 통해 호선을 선택하고, 추가로 시간을 고를 Select Box를 추가하여 해당 시간에 고른 호선의 역에 따른 복잡도를 비교하기 : 꺾은선 그래프 혹은 다른 그래프를 통해 역 별 복잡도 차이 확인하기
9. 특정 호선의 전체 시간 대 역별 복잡도 비교에서는 데이터의 평균 및 전반적인 통계값을 사용하며, Select Box를 통해 호선을 선택하면 하루의 전반적인 통계적인 역별 복잡도를 보여줘서 비교하기
10. 8와 9에서는 오늘의 날짜가 반영되며, 추후 Date input 기능을 통해 평일 / 토요일 / 일요일에 따른 데이터 변화 추이 보여주기

11. CSV가 아닌 오픈 API 호출을 통해, CSV 파일이 없더라도 사이트가 동작하도록 하기
12. 추후 위의 기능 구현이 완성되면, 챗봇 기능을 추가하여 현재 어떤 역과 호선이 한가하고 어떤 역과 호선이 가장 붐비는지, 어떤 지하철을 탈 것인데 어느 역이 가장 붐비는지 등의 정보를 물어보고 답할 수 있도록 하기