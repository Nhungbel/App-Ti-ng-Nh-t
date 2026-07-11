import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import re

st.set_page_config(page_title="App Tiếng Nhật", page_icon="🇯🇵")
st.title("🇯🇵 App Tra Cứu Tiếng Nhật (Auto-Update)")

# KHÔNG DÙNG @st.cache_data ĐỂ NÓ LUÔN ĐỌC FILE MỚI NHẤT
def load_data():
    try:
        return pd.read_csv("tuvung.csv")
    except:
        return pd.DataFrame(columns=["Nghia", "TiengNhat", "PhanLoai"])

df = load_data()
search = st.text_input("🔍 Nhập từ cần tìm:")

if search:
    # Lọc dữ liệu
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | 
             df["TiengNhat"].str.contains(search, case=False, na=False)]
    
    if not res.empty:
        for _, r in res.iterrows():
            st.write(f"### {r['TiengNhat']}")
            st.write(f"💡 Nghĩa: {r['Nghia']}")
            
            # Tạo âm thanh
            try:
                text_clean = re.sub(r'\(.*?\)', '', str(r['TiengNhat'])).strip()
                tts = gTTS(text=text_clean, lang='ja')
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                st.audio(fp, format='audio/mp3')
            except:
                st.error("Lỗi tạo âm thanh!")
            st.divider()
    else:
        st.warning("Từ này chưa có trong từ điển. Bạn hãy thêm vào file tuvung.csv trên GitHub nhé!")
