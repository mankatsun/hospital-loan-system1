import streamlit as st
import pandas as pd
from datetime import date

# 設定網頁標題
st.set_page_config(page_title="醫院物品租借管理系統", layout="wide")

st.title("🏥 醫院物品租借/領用數位系統")
st.write("請根據紙本表單內容填寫以下資訊")

# 建立側邊欄導覽
menu = ["新增租借紀錄", "查看所有紀錄"]
choice = st.sidebar.selectbox("選單", menu)

# 初始化資料儲存 (實際應用時可改為資料庫)
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=[
        "表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", "借用日期", "歸還日期", "備註", 
        "借用部門主管", "借出部門主管", "狀態"
    ])

if choice == "新增租借紀錄":
    st.subheader("📝 填寫暫借物品表 (Temporary Transfer Form)")
    
    # 表單基本資訊
    st.markdown("### 📋 表單基本資訊")
    col1, col2, col3 = st.columns(3)
    with col1:
        form_no = st.text_input("表單編號 (No.)", placeholder="例: 008913")
    with col2:
        form_date = st.date_input("日期 (Date)", value=date.today())
    with col3:
        dept = st.text_input("領用部門 / 病房 (Borrow Department / Ward)")
    
    # 物品明細
    st.markdown("### 📦 物品明細")
    col1, col2 = st.columns(2)
    with col1:
        item_code = st.text_input("物品編號 (Code No.)")
        quantity = st.number_input("數量 (Quantity)", min_value=1, step=1)
    with col2:
        description = st.text_area("摘要 (Description)")
        remark = st.text_area("備註 (Remark)", placeholder="特殊需求或說明...")
    
    # 日期資訊
    col1, col2 = st.columns(2)
    with col1:
        loan_date = st.date_input("借用日期 (Date Loan)", value=date.today())
    with col2:
        return_date = st.date_input("歸還日期 (Date Return)")
    
    # 主管簽名
    st.markdown("### ✍️ 主管簽名")
    col1, col2 = st.columns(2)
    with col1:
        borrow_manager = st.text_input("借用部門主管 (Borrow Dept. i/c)", placeholder="請輸入姓名")
    with col2:
        loan_manager = st.text_input("借出部門主管 (Loan Dept. i/c)", placeholder="請輸入姓名")

    if st.button("📤 提交申請", use_container_width=True):
        if not form_no or not dept or not item_code or not description:
            st.error("請填寫必填欄位：表單編號、領用部門、物品編號、摘要")
        else:
            new_data = {
                "表單編號": form_no,
                "領用部門": dept,
                "日期": form_date,
                "物品編號": item_code,
                "摘要": description,
                "數量": quantity,
                "借用日期": loan_date,
                "歸還日期": return_date,
                "備註": remark,
                "借用部門主管": borrow_manager,
                "借出部門主管": loan_manager,
                "狀態": "租借中"
            }
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
            st.success("✅ 紀錄已成功儲存！")
            st.balloons()

elif choice == "查看所有紀錄":
    st.subheader("📋 租借紀錄總覽")
    if not st.session_state.df.empty:
        st.dataframe(st.session_state.df)
        
        # 匯出 Excel 功能
        csv = st.session_state.df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="下載紀錄 (CSV)",
            data=csv,
            file_name="hospital_loan_records.csv",
            mime="text/csv",
        )
    else:
        st.info("目前尚無任何紀錄。")
