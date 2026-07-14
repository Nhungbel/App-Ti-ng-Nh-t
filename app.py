import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Thêm encoding='utf-8' để đọc tiếng Nhật
    return pd.read_csv('tuvung.csv', encoding='utf-8')

df = load_data()

st.title("🇯🇵 Tra cứu 1000 Từ Vựng")

# Sử dụng key để giữ trạng thái input ổn định
search_query = st.text_input("Tìm kiếm:", key="search_bar")

if search_query:
    # Lọc: Tìm trong cột 'Nghia' HOẶC 'TiengNhat'
    # .str.strip() giúp xóa khoảng trắng vô tình có ở đầu/cuối ô
    mask = (df['Nghia'].str.contains(search_query, case=False, na=False)) | \
           (df['TiengNhat'].str.contains(search_query, case=False, na=False))
    
    results = df[mask]
    
    if not results.empty:
        for index, row in results.iterrows():
            st.write(f"### {row['Nghia']} - {row['TiengNhat']}")
            st.write(f"**Romaji:** {row['Romaji']}")
            st.markdown(f"**Pitch Accent:** {row['PitchAccent']}", unsafe_allow_html=True)
            st.write("---")
    else:
        # Nếu vẫn hiện ra đây, nghĩa là từ bạn tìm không nằm trong file CSV
        st.warning(f"Không tìm thấy từ: '{search_query}'. Hãy kiểm tra lại file CSV.")
        st.write("Dữ liệu hiện có trong hệ thống:")
        st.write(df['Nghia'].tolist()) # Hiển thị danh sách từ để debug
# 5. LOGIC XỬ LÝ
filtered_df = df.copy()

# Lọc theo danh mục
if selected_category != "Tất cả":
    filtered_df = filtered_df[filtered_df["PhanLoai"] == selected_category]

# Lọc theo ô tìm kiếm
if search:
    filtered_df = filtered_df[
        filtered_df["Nghia"].str.contains(search, case=False, na=False) | 
        filtered_df["TiengNhat"].str.contains(search, case=False, na=False)
    ]

# 6. HIỂN THỊ KẾT QUẢ
if not filtered_df.empty:
    st.success(f"Tìm thấy {len(filtered_df)} từ:")
    for _, r in filtered_df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {r['TiengNhat']}")
            st.write(f"**Nghĩa:** {r['Nghia']} | **Phân loại:** {r['PhanLoai']}")
        
        with col2:
            # Tạo âm thanh chuyên nghiệp
            text_clean = re.sub(r'\(.*?\)', '', str(r['TiengNhat'])).strip()
            tts = gTTS(text=text_clean, lang='ja')
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')
        st.divider()
else:
    st.warning("Không tìm thấy kết quả nào. Bạn hãy thử từ khác nhé!")

# 7. CHÂN TRANG
st.markdown("---")
st.write("Cập nhật dữ liệu tại file `tuvung.csv` trên GitHub của bạn.")
