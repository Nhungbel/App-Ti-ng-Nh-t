import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Giả sử bạn đã up file csv lên GitHub
    return pd.read_csv("tuvung.csv")

df = load_data()

st.title("🇯🇵 Từ điển 10.000 từ")
search = st.text_input("🔍 Tìm kiếm:")

if search:
    res = df[df["Nghia"].str.contains(search, case=False, na=False) | 
             df["TiengNhat"].str.contains(search, case=False, na=False)]
    
    # Phân trang: Chỉ hiển thị 20 kết quả mỗi lần để App không bị treo
    page = st.number_input("Trang", min_value=1, value=1)
    start = (page - 1) * 20
    end = start + 20
    
    st.write(f"Hiển thị {start+1} đến {min(end, len(res))} của {len(res)} kết quả")
    for _, r in res.iloc[start:end].iterrows():
        st.write(f"**{r['TiengNhat']}** - {r['Nghia']}")
