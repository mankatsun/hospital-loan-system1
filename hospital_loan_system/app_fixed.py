import streamlit as st
import pandas as pd
from datetime import date
import gspread
import os
import json

# 設定網頁標題
st.set_page_config(page_title="醫院物品租借管理系統", layout="wide")

st.title("🏥 醫院物品租借/領用數位系統")
st.write("🌐 資料即時同步至 Google Sheets")

# 建立側邊欄導覽
menu = ["新增租借紀錄", "查看所有紀錄"]
choice = st.sidebar.selectbox("選單", menu)

# Google Sheets 連接
def connect_to_sheets():
    try:
        # 從環境變數讀取認證
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if credentials_json:
            # 清理 JSON 字符串
            credentials_json = credentials_json.strip()
            # 移除可能的控制字符
            credentials_json = json.loads(credentials_json)
            
            from google.oauth2.service_account import Credentials
            creds = Credentials.from_service_account_info(credentials_json, scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ])
            client = gspread.authorize(creds)
            sheet = client.open('醫院物品租借系統')
            worksheet = sheet.worksheet('租借紀錄')
            return worksheet
        else:
            st.error("❌ 環境變數未設定")
            return None
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON 格式錯誤：{str(e)}")
        st.write("請檢查 TOML 格式中的 JSON 內容")
        return None
    except Exception as e:
        st.error(f"❌ 連接失敗：{str(e)}")
        return None

# 初始化資料
if 'worksheet' not in st.session_state:
    st.session_state.worksheet = connect_to_sheets()
    if st.session_state.worksheet:
        st.success("✅ 已成功連接到 Google Sheets！")

if choice == "新增租借紀錄":
    st.subheader("📝 填寫暫借物品表")
    
    col1, col2 = st.columns(2)
    with col1:
        form_no = st.text_input("表單編號 (No.)")
        dept = st.text_input("領用部門")
        item_code = st.text_input("物品編號")
        description = st.text_area("摘要")
    
    with col2:
        quantity = st.number_input("數量", min_value=1, step=1)
        loan_date = st.date_input("借用日期", value=date.today())
        return_date = st.date_input("歸還日期")
        remark = st.text_area("備註")

    if st.button("📤 提交申請"):
        if form_no and dept and item_code and description:
            if st.session_state.worksheet:
                try:
                    # 新增紀錄到 Google Sheets
                    new_row = [
                        form_no, dept, date.today().strftime("%Y-%m-%d"), 
                        item_code, description, str(quantity),
                        loan_date.strftime("%Y-%m-%d"), return_date.strftime("%Y-%m-%d"),
                        remark, "", "", "租借中"
                    ]
                    st.session_state.worksheet.append_row(new_row)
                    st.success("✅ 紀錄已成功儲存至 Google Sheets！")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ 儲存失敗：{str(e)}")
            else:
                st.error("❌ Google Sheets 連接失敗")
        else:
            st.error("請填寫必填欄位")

elif choice == "查看所有紀錄":
    st.subheader("📋 租借紀錄總覽")
    
    if st.session_state.worksheet:
        try:
            data = st.session_state.worksheet.get_all_records()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df, use_container_width=True)
                
                # 統計資訊
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("總紀錄數", len(df))
                with col2:
                    st.metric("租借中", len(df[df["狀態"] == "租借中"]))
            else:
                st.info("目前尚無任何紀錄。")
        except Exception as e:
            st.error(f"❌ 載入失敗：{str(e)}")
    else:
        st.error("❌ Google Sheets 連接失敗")
