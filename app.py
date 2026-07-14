import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import re

st.set_page_config(page_title="App Tra Cứu Tiếng Nhật", page_icon="🇯🇵", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1a4d4a;'>🇯🇵 APP TRA CỨU & LUYỆN NGHE TIẾNG NHẬT</h1>", unsafe_allow_html=True)

# Tải dữ liệu
@st.cache_data
def load_data():
    return pd.read_csv("tuvung.csv")

df = load_data()

# Tìm kiếm và lọc
search_query = st.text_input("🔍 Nhập từ cần tìm:")
categories = ["Tất cả"] + list(df["PhanLoai"].unique())
selected_cat = st.selectbox("📂 Lọc theo danh mục:", categories)

filtered_df = df.copy()
if selected_cat != "Tất cả":
    filtered_df = filtered_df[filtered_df["PhanLoai"] == selected_cat]
if search_query:
    filtered_df = filtered_df[filtered_df["Nghia"].str.contains(search_query, case=False, na=False) | filtered_df["TiengNhat"].str.contains(search_query, case=False, na=False)]

# Hiển thị kết quả
for index, row in filtered_df.iterrows():
    st.markdown(f"**{row['TiengNhat']}** - *{row['PhanLoai']}*")
    st.write(f"💡 Nghĩa: {row['Nghia']}")
    # Tạo âm thanh
    text_to_speak = re.sub(r'\[.*?\]', '', str(row['TiengNhat'])).strip()
    tts = gTTS(text=text_to_speak, lang='ja')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    st.audio(fp, format='audio/mp3')
