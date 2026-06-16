import streamlit as st

st.set_page_config(
    page_title="SET50 Dashboard",
    layout="wide"
)

st.title("SET50 Dashboard")
st.caption("ระบบวิเคราะห์ข้อมูลผู้ถือหุ้น SET50 จาก Neon Database")

st.markdown("""
## เมนูหลัก

เลือกหน้าจากแถบด้านซ้าย

- **SET50 Social Analytics**  
  วิเคราะห์เครือข่ายความเชื่อมโยงระหว่างหุ้นและผู้ถือหุ้นใหญ่

ในอนาคตสามารถเพิ่มหน้าอื่นได้ เช่น

- วิเคราะห์ผู้ถือหุ้นรายใหญ่
- วิเคราะห์กลุ่ม Nominee
- วิเคราะห์หุ้นที่มีผู้ถือหุ้นร่วมกัน
- Dashboard รายตัวหุ้น
""")
