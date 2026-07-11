import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import re

st.set_page_config(page_title="App Tra Cứu Tiếng Nhật", page_icon="🇯🇵")
st.title("🇯🇵 App Tra Cứu Tiếng Nhật")

@st.cache_data
def load_data():
    return pd.read_csv("tuvung.csv")

df = load_data()
search = st.text_input("🔍 Tìm kiếm:")

if search:
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | df["TiengNhat"].str.contains(search, case=False, na=False)]
    for _, r in res.iterrows():
        st.write(f"**{r['TiengNhat']}** - {r['Nghia']}")
        tts = gTTS(text=re.sub(r'\[.*?\]', '', str(r['TiengNhat'])), lang='ja')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')
