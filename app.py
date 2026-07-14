import streamlit as st
import pandas as pd
from gtts import gTTS
import io
import re

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="Học Tiếng Nhật Pro", page_icon="🇯🇵", layout="wide")

# CSS tinh chỉnh giao diện
st.markdown("""
    <style>
    .big-font { font-size:30px !important; font-weight: bold; color: #1a4d4a; }
    .stApp { background-color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# 2. TẢI DỮ LIỆU VỚI CƠ CHẾ CACHE
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("tuvung.csv")
        return df
    except:
        return pd.DataFrame(columns=["Nghia", "TiengNhat", "PhanLoai"])

df = load_data()

# 3. SIDEBAR (THANH BÊN)
st.sidebar.title("🎛️ Bảng điều khiển")
selected_category = st.sidebar.selectbox("Lọc theo nhóm:", ["Tất cả"] + list(df["PhanLoai"].unique()))
st.sidebar.info(f"Tổng số từ: {len(df)}")

# 4. GIAO DIỆN CHÍNH
st.markdown('<p class="big-font">🇯🇵 App Tra Cứu Tiếng Nhật Pro</p>', unsafe_allow_html=True)
search = st.text_input("🔍 Nhập từ tiếng Nhật hoặc nghĩa tiếng Việt:", placeholder="Ví dụ: Ăn...")

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
