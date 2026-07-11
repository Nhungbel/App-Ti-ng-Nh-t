import streamlit as st
import pandas as pd
from gtts import gTTS
import io

st.set_page_config(page_title="App Tiếng Nhật", page_icon="🇯🇵")
st.title("🇯🇵 App Tra Cứu Tiếng Nhật")

@st.cache_data
def load_data():
    return pd.read_csv("tuvung.csv")

df = load_data()

search = st.text_input("🔍 Nhập từ cần tìm:")

if search:
    # Lọc dữ liệu
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | df["TiengNhat"].str.contains(search, case=False, na=False)]
    
    if not res.empty:
        for _, r in res.iterrows():
            st.write(f"### {r['TiengNhat']}")
            st.write(f"💡 Nghĩa: {r['Nghia']}")
            # Chỉ tạo âm thanh nếu có dữ liệu tiếng Nhật
            tts = gTTS(text=str(r['TiengNhat']).split('(')[0].strip(), lang='ja')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')
    else:
        st.warning("Không tìm thấy từ này trong từ điển!")
