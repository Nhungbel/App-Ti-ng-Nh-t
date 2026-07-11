import streamlit as st
import pandas as pd

# Load dữ liệu
df = pd.read_csv('tuvung.csv')

st.title("🇯🇵 Tra cứu 1000 Từ Vựng")

# Sử dụng key để quản lý input, giúp tránh lỗi đơ màn hình
search_query = st.text_input("Tìm kiếm:", key="search_bar")

if search_query:
    # Lọc dữ liệu
    result = df[df['Nghia'].str.contains(search_query, case=False, na=False) | 
                df['TiengNhat'].str.contains(search_query, case=False, na=False)]
    
    if not result.empty:
        for i, row in result.iterrows():
            st.write(f"### {row['Nghia']} - {row['TiengNhat']}")
            st.write(f"**Romaji:** {row['Romaji']}")
            # Hiển thị pitch accent màu đỏ
            st.markdown(f"**Pitch Accent:** {row['PitchAccent']}", unsafe_allow_html=True)
            st.divider()
    else:
        st.warning("Không tìm thấy từ này.")

# Nút xóa nhanh để khỏi phải ấn backspace nhiều
if st.button("Xóa tìm kiếm"):
    st.rerun()
