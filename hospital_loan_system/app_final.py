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
menu = ["新增租借紀錄", "查看所有紀錄", "系統狀態"]
choice = st.sidebar.selectbox("選單", menu)

# Google Sheets 連接
def connect_to_sheets():
    try:
        # 顯示環境變數狀態
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        
        if credentials_json:
            st.success("🔑 環境變數已讀取")
            st.write(f"📊 認證內容長度：{len(credentials_json)} 字符")
            
            # 嘗試解析 JSON
            try:
                credentials_json = json.loads(credentials_json)
                st.success("✅ JSON 解析成功")
            except json.JSONDecodeError as e:
                st.error(f"❌ JSON 解析失敗：{str(e)}")
                st.write("請檢查 TOML 格式中的 JSON 內容")
                return None
            
            # 嘗試連接 Google Sheets
            try:
                from google.oauth2.service_account import Credentials
                creds = Credentials.from_service_account_info(credentials_json, scopes=[
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ])
                client = gspread.authorize(creds)
                
                # 嘗試開啟試算表
                sheet = client.open('醫院物品租借系統')
                worksheet = sheet.worksheet('租借紀錄')
                
                st.success("✅ Google Sheets 連接成功！")
                return worksheet
                
            except gspread.SpreadsheetNotFound:
                st.error("❌ 試算表不存在，正在建立...")
                sheet = client.create('醫院物品租借系統')
                worksheet = sheet.add_worksheet('租借紀錄', rows=1000, cols=20)
                # 建立標題
                headers = ["表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", 
                          "借用日期", "歸還日期", "備註", "借用部門主管", "借出部門主管", "狀態"]
                worksheet.append_row(headers)
                st.success("✅ 試算表建立成功！")
                return worksheet
                
            except Exception as e:
                st.error(f"❌ Google Sheets 連接失敗：{str(e)}")
                return None
        else:
            st.error("❌ 環境變數未設定")
            st.info("請在 Streamlit Cloud 中設定 GOOGLE_APPLICATION_CREDENTIALS_JSON 環境變數")
            return None
            
    except Exception as e:
        st.error(f"❌ 整體連接失敗：{str(e)}")
        return None

# 初始化資料
if 'worksheet' not in st.session_state:
    st.session_state.worksheet = connect_to_sheets()

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
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("總紀錄數", len(df))
                with col2:
                    st.metric("租借中", len(df[df["狀態"] == "租借中"]))
                with col3:
                    st.metric("已歸還", len(df[df["狀態"] == "已歸還"]))
            else:
                st.info("目前尚無任何紀錄。")
        except Exception as e:
            st.error(f"❌ 載入失敗：{str(e)}")
    else:
        st.error("❌ Google Sheets 連接失敗")

elif choice == "系統狀態":
    st.subheader("🔧 系統狀態")
    
    # 顯示連接狀態
    if st.session_state.worksheet:
        st.success("✅ Google Sheets 連接正常")
        
        # 顯示試算表資訊
        try:
            data = st.session_state.worksheet.get_all_records()
            st.write(f"📊 目前資料筆數：{len(data)}")
        except:
            st.write("📊 無法讀取資料統計")
    else:
        st.error("❌ Google Sheets 連接失敗")
    
    # 顯示環境變數狀態
    credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if credentials_json:
        st.success("🔑 環境變數已設定")
    else:
        st.error("❌ 環境變數未設定")
    
    # 重新連接按鈕
    if st.button("🔄 重新連接"):
        st.session_state.worksheet = connect_to_sheets()
        st.rerun()
