import streamlit as st
import pandas as pd

# โหลดข้อมูล
@st.cache_data
def load_data():
    file_path = "C:/Users/informatics/Desktop/65160401/17/Lineman_Shops_Final_Clean.csv"  # เปลี่ยนเป็น path ของคุณ
    df = pd.read_csv(file_path)
    return df

df = load_data()

# Inject custom CSS styling (ธีม Dark Mode แบบใหม่)
st.markdown("""
    <style>
        /* นำเข้า Google Fonts (Poppins) */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
        
        /* ตั้งค่า background ทั้งหน้าเป็น gradient แบบ Dark */
        html, body {
            background: linear-gradient(135deg, #2c3e50, #000000);
            font-family: 'Poppins', sans-serif;
            color: #f1f1f1;
            margin: 0;
            padding: 0;
        }
        
        /* ทำให้พื้นที่หลักของ Streamlit โปร่งใส */
        .css-18e3th9 {
            background-color: transparent;
        }
        
        /* ปรับแต่ง sidebar ให้มีพื้นหลังแบบโปร่งแสงในธีมมืด */
        .css-1d391kg {
            background-color: rgba(0, 0, 0, 0.7);
            border-radius: 10px;
            padding: 20px;
        }
        
        /* สไตล์หัวข้อหลัก */
        h1 {
            color: #e67e22;
            text-align: center;
            margin-top: 40px;
            text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.8);
        }
        
        /* สไตล์ของกล่องผลลัพธ์ (restaurant card) */
        .restaurant-card {
            background: rgba(44, 62, 80, 0.85);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .restaurant-card:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 16px rgba(0,0,0,0.7);
        }
        .restaurant-card h3 {
            color: #e67e22;
            margin-bottom: 10px;
        }
        
        /* สไตล์ของลิงก์ */
        a {
            color: #3498db;
            text-decoration: none;
            font-weight: 600;
        }
        a:hover {
            text-decoration: underline;
        }
        
        /* สไตล์ของปุ่ม */
        .stButton > button {
            background-color: #e67e22;
            color: #ffffff;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        .stButton > button:hover {
            background-color: #d35400;
        }
    </style>
""", unsafe_allow_html=True)

# ฟังก์ชันแก้ไขลิงก์ URL
def format_url(name, url):
    if pd.isna(url) or url.strip() in ["-", ""]:
        return f"https://www.google.com/search?q={name} ร้านอาหาร"
    return url

# ฟังก์ชันแนะนำร้านตามตัวกรอง (ใช้เพียง "ประเภทอาหาร" และ "ระดับราคา")
def recommend_restaurants(category, price_level, top_n=5):
    filtered_df = df[df["category"].str.contains(category, na=False, case=False)]
    filtered_df = filtered_df[filtered_df["price_level"] == price_level]
    results = []
    for _, row in filtered_df.head(top_n).iterrows():
        paragraph = f"""
        <div class="restaurant-card">
            <h3>🍽 {row['name']}</h3>
            <p>
                <strong>หมวดหมู่:</strong> {row['category']}<br>
                <strong>ราคา:</strong> {row['price_level']}<br>
                🔗 <a href="{format_url(row['name'], row['url'])}" target="_blank">ดูรายละเอียดเพิ่มเติม</a>
            </p>
        </div>
        """
        results.append(paragraph)
    return results if results else ["<div class='restaurant-card'>❌ ไม่พบร้านที่ตรงกับเงื่อนไข</div>"]

# สร้าง UI ด้วย Streamlit
st.title("🍽️ เย็นนี้กินอะไรดี?")
st.sidebar.header("🔍 ค้นหาร้านอาหาร")

# เอาส่วนเลือกที่อยู่ออกไป
category = st.selectbox("🍜 เลือกประเภทอาหาร", df["category"].dropna().unique())
price_level = st.selectbox("💰 เลือกระดับราคา", df["price_level"].unique())

if st.button("🔍 ค้นหาร้านอาหาร"):
    results = recommend_restaurants(category, price_level)
    for res in results:
        st.markdown(res, unsafe_allow_html=True)

st.sidebar.markdown("### 📢 วิธีใช้")
st.sidebar.write("""
- เลือกประเภทอาหาร และระดับราคา
- คลิกเพื่อค้นหาร้านอาหารที่ตรงกับเงื่อนไข
- คลิกที่ลิงก์เพื่อดูรายละเอียดเพิ่มเติม
""")
