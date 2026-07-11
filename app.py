import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import re

st.set_page_config(page_title="App Tiếng Nhật", page_icon="🇯🇵")
st.title("🇯🇵 App Tra Cứu Tiếng Nhật")

# Hàm đọc file (không dùng cache để luôn lấy dữ liệu mới nhất)
def load_data():
    try:
        return pd.read_csv("tuvung.csv")
    except:
        return pd.DataFrame(columns=["Nghia", "TiengNhat", "PhanLoai"])

df = load_data()

# Tạo một key riêng cho ô input để nó tự refresh mà không làm sập app
search = st.text_input("🔍 Nhập từ cần tìm:", key="input_search")

if search:
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | 
             df["TiengNhat"].str.contains(search, case=False, na=False)]
    
    if not res.empty:
        for _, r in res.iterrows():
            st.write(f"### {r['TiengNhat']}")
            st.write(f"💡 Nghĩa: {r['Nghia']}")
            
            # Tạo âm thanh vào biến tạm thay vì ghi đè file hệ thống
            text_clean = re.sub(r'\(.*?\)', '', str(r['TiengNhat'])).strip()
            tts = gTTS(text=text_clean, lang='ja')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            
            # Đọc trực tiếp từ bộ nhớ
            st.audio(fp, format='audio/mp3')
            st.divider()
    else:
        st.warning("Không tìm thấy từ này!")
