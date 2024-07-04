import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# Streamlit 설정
st.set_page_config(page_title="구해줘 공장 🗺", layout="wide")

# CSV 데이터 로드
store = pd.read_csv('https://blog.kakaocdn.net/dn/ooQp5/btsIn79vdrW/NU7TR5Qybu8Oqk9sZL0ick/good_price.csv?attach=1&knm=tfile.csv')

# 업종명 목록 추출
business_types = store['업종명'].unique()

# 주소에서 시 단위 추출
store['시단위'] = store['주소'].apply(lambda x: x.split(' ')[0])
cities = store['시단위'].unique()

# 사이드바에 필터 옵션 추가
selected_business_types = st.sidebar.multiselect('업종명을 선택하세요', business_types)
selected_cities = st.sidebar.multiselect('지역을 선택하세요', cities, ['서울특별시', '서울', '구로구', '제주특별자치도'])

# 선택한 업종명과 지역에 따라 데이터 필터링
filtered_store = store

if selected_business_types:
    filtered_store = filtered_store[filtered_store['업종명'].isin(selected_business_types)]

if selected_cities:
    filtered_store = filtered_store[filtered_store['시단위'].isin(selected_cities)]

# 지도 중심 좌표 설정
center_lat, center_lng = 37.1, 128.8
m = folium.Map(location=[center_lat, center_lng], zoom_start=8, width='100%', height='100%')

# 필터링된 데이터에서 위도와 경도 추출하여 Marker 추가
for index, row in filtered_store.iterrows():
    lat, lng = row['위도'], row['경도']
    store_name = row['업소명']
    main_item = row['주요품목']
    price = row['가격']
    tel = row['업소 전화번호']
    popup_text = f"{store_name} - {main_item} - {price}원\n{tel}"
    
    folium.Marker(
        [lat, lng], 
        popup=popup_text, 
        tooltip="Click for more info", 
        icon=folium.Icon(color='green')
    ).add_to(m)

# 스타일 설정
st.markdown("""
    <style>
    .folium-map {
        width: 100%;
        height: calc(100vh - 70px);  /* Adjust height as needed */
    }
    </style>
    """, unsafe_allow_html=True)

# Streamlit에 Folium 지도 표시
folium_static(m, width=1920, height=1080)