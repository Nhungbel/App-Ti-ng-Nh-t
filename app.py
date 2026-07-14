import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import re

st.set_page_config(page_title="App Tiếng Nhật 1000 từ", page_icon="🇯🇵")
st.title("🇯🇵 Tra cứu 1000 từ vựng")

# Hàm đọc dữ liệu nhanh
@st.cache_data(ttl=60) # Tự refresh dữ liệu sau mỗi 60 giây
def load_data():
    return pd.read_csv("tuvung.csv")

df = load_data()

search = st.text_input("🔍 Nhập từ tìm kiếm:")

if search:
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | 
             df["TiengNhat"].str.contains(search, case=False, na=False)]
    
    st.write(f"Tìm thấy {len(res)} từ.")
    for _, r in res.head(10).iterrows(): # Chỉ hiện 10 kết quả đầu để tránh treo màn hình
        st.write(f"### {r['TiengNhat']} - {r['Nghia']}")
        
        # Tạo âm thanh trực tiếp
        text_clean = re.sub(r'\(.*?\)', '', str(r['TiengNhat'])).strip()
        tts = gTTS(text=text_clean, lang='ja')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
