import streamlit as st
import pandas as pd
from datetime import date
from google_sheets_config import GoogleSheetsManager

# 設定網頁標題
st.set_page_config(page_title="醫院物品租借管理系統 (雲端版)", layout="wide")

st.title("🏥 醫院物品租借/領用數位系統 (雲端版)")
st.write("🌐 資料即時同步至 Google Sheets，支援多人協作")

# 建立側邊欄導覽
menu = ["新增租借紀錄", "查看所有紀錄", "系統設定"]
choice = st.sidebar.selectbox("選單", menu)

# 初始化 Google Sheets 連接
if 'sheets_manager' not in st.session_state:
    st.session_state.sheets_manager = GoogleSheetsManager()
    
# 初始化資料
if 'df' not in st.session_state:
    try:
        # 先建立連接
        import os
        credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
        if credentials_json:
            st.write("🔑 環境變數已讀取")
            st.write(f"📊 認證內容長度：{len(credentials_json)} 字符")
        else:
            st.write("❌ 環境變數未設定")
        
        st.session_state.sheets_manager.connect()
        # 然後載入資料
        st.session_state.df = st.session_state.sheets_manager.load_data()
        st.success("✅ 已成功連接到 Google Sheets！")
    except Exception as e:
        st.error(f"❌ 連接 Google Sheets 失敗：{str(e)}")
        st.info("請檢查 Google Sheets 設定檔案")
        # 建立本地備用資料
        st.session_state.df = pd.DataFrame(columns=[
            "表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", 
            "借用日期", "歸還日期", "備註", "借用部門主管", "借出部門主管", "狀態"
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
                "日期": form_date.strftime("%Y-%m-%d"),
                "物品編號": item_code,
                "摘要": description,
                "數量": quantity,
                "借用日期": loan_date.strftime("%Y-%m-%d"),
                "歸還日期": return_date.strftime("%Y-%m-%d"),
                "備註": remark,
                "借用部門主管": borrow_manager,
                "借出部門主管": loan_manager,
                "狀態": "租借中"
            }
            
            # 新增到 DataFrame
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_data])], ignore_index=True)
            
            # 儲存到 Google Sheets
            try:
                # 直接新增單筆紀錄到 Google Sheets
                record_data = [
                    form_no, dept, form_date.strftime("%Y-%m-%d"), item_code, description,
                    str(quantity), loan_date.strftime("%Y-%m-%d"), return_date.strftime("%Y-%m-%d"), 
                    remark, borrow_manager, loan_manager, "租借中"
                ]
                
                # 顯示除錯訊息
                st.write("🔄 正在儲存到 Google Sheets...")
                st.write(f"📋 資料內容：{record_data}")
                
                result = st.session_state.sheets_manager.add_record(record_data)
                st.success("✅ 紀錄已成功儲存至 Google Sheets！")
                st.balloons()
                
                # 顯示成功後的資料統計
                current_data = st.session_state.sheets_manager.load_data()
                st.info(f"📊 Google Sheets 現在有 {len(current_data)} 筆資料")
                
            except Exception as e:
                st.error(f"❌ 儲存至 Google Sheets 失敗：{str(e)}")
                st.warning("資料暫存在本地，請檢查網路連接")
                # 顯示詳細錯誤資訊
                st.code(str(e))

elif choice == "查看所有紀錄":
    st.subheader("📋 租借紀錄總覽")
    
    # 重新載入最新資料
    if st.button("🔄 重新載入資料"):
        try:
            st.session_state.df = st.session_state.sheets_manager.load_data()
            st.success("✅ 資料已更新！")
        except Exception as e:
            st.error(f"❌ 載入資料失敗：{str(e)}")
    
    if not st.session_state.df.empty:
        # 狀態篩選
        status_filter = st.selectbox("篩選狀態", ["全部", "租借中", "已歸還"])
        if status_filter != "全部":
            filtered_df = st.session_state.df[st.session_state.df["狀態"] == status_filter]
        else:
            filtered_df = st.session_state.df
        
        st.dataframe(filtered_df, use_container_width=True)
        
        # 統計資訊
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("總紀錄數", len(st.session_state.df))
        with col2:
            st.metric("租借中", len(st.session_state.df[st.session_state.df["狀態"] == "租借中"]))
        with col3:
            st.metric("已歸還", len(st.session_state.df[st.session_state.df["狀態"] == "已歸還"]))
        
        # 匯出功能
        csv = filtered_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 下載紀錄 (CSV)",
            data=csv,
            file_name="hospital_loan_records.csv",
            mime="text/csv",
        )
    else:
        st.info("目前尚無任何紀錄。")

elif choice == "系統設定":
    st.subheader("⚙️ 系統設定")
    
    st.markdown("### 🌐 Google Sheets 設定")
    st.info("""
    **設定步驟：**
    1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
    2. 建立新專案或選擇現有專案
    3. 啟用 Google Sheets API 和 Google Drive API
    4. 建立服務帳戶並下載 JSON 檔案
    5. 將 JSON 檔案重新命名為 `service_account.json` 並放在專案資料夾中
    6. 在 Google Sheets 中分享試算表給服務帳戶的電子郵件
    """)
    
    st.markdown("### 📊 功能特色")
    col1, col2 = st.columns(2)
    with col1:
        st.write("✅ 即時同步")
        st.write("✅ 多人協作")
        st.write("✅ 自動備份")
    with col2:
        st.write("✅ 雲端儲存")
        st.write("✅ 隨時存取")
        st.write("✅ 資料安全")
    
    # 連接測試
    if st.button("🔗 測試 Google Sheets 連接"):
        try:
            manager = GoogleSheetsManager()
            if manager.connect():
                st.success("✅ 連接成功！")
            else:
                st.error("❌ 連接失敗")
        except Exception as e:
            st.error(f"❌ 連接錯誤：{str(e)}")

# 側邊欄資訊
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 系統狀態")
if not st.session_state.df.empty:
    st.sidebar.write(f"📝 總紀錄：{len(st.session_state.df)}")
    st.sidebar.write(f"🔄 租借中：{len(st.session_state.df[st.session_state.df['狀態'] == '租借中'])}")
else:
    st.sidebar.write("📝 總紀錄：0")

st.sidebar.markdown("### 💡 提示")
st.sidebar.write("• 資料自動同步至雲端")
st.sidebar.write("• 支援多人同時使用")
st.sidebar.write("• 可隨時匯出資料")
