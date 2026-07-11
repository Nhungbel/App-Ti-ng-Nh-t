import streamlit as st
import pandas as pd
from gtts import gTTS
import io

st.set_page_config(page_title="App 1000 từ", layout="centered")
st.title("🇯🇵 Tra cứu 1000 Từ Vựng")

@st.cache_data
def load_data():
    return pd.read_csv("tuvung.csv")

df = load_data()
search = st.text_input("🔍 Tìm kiếm:")

if search:
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | 
             df["TiengNhat"].str.contains(search, case=False, na=False)]
    
    # Chỉ hiển thị kết quả đầu tiên để không bị lag
    if not res.empty:
        r = res.iloc[0] 
        st.subheader(f"{r['TiengNhat']} - {r['Nghia']}")
        
        tts = gTTS(text=str(r['TiengNhat']), lang='ja')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
    else:
        st.warning("Không tìm thấy từ này.")
