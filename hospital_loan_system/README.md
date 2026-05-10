# 🏥 醫院物品租借管理系統 (雲端版)

## 📋 功能特色

- 🌐 **雲端同步** - 資料即時同步至 Google Sheets
- 👥 **多人協作** - 支援多人同時使用
- 📱 **隨時存取** - 任何有網路的地方都能使用
- 🔄 **自動備份** - 資料安全儲存在雲端
- 📊 **資料分析** - 即時統計和篩選功能

## 🚀 快速開始

### 1. 安裝所需套件
```bash
pip install streamlit pandas gspread google-auth-oauthlib
```

### 2. Google Sheets 設定

#### 步驟一：Google Cloud 設定
1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 建立新專案或選擇現有專案
3. 啟用以下 API：
   - Google Sheets API
   - Google Drive API

#### 步驟二：建立服務帳戶
1. 在 Google Cloud Console 中，前往「IAM 與管理」>「服務帳戶」
2. 點擊「建立服務帳戶」
3. 填寫服務帳戶資訊
4. 建立並下載 JSON 金鑰檔案
5. 將檔案重新命名為 `service_account.json` 並放在專案資料夾中

#### 步驟三：設定 Google Sheets
1. 建立新的 Google Sheets 試算表
2. 將試算表命名為「醫院物品租借系統」
3. 分享試算表給服務帳戶的電子郵件地址（在 JSON 檔案中找到）
4. 給予「編輯」權限

### 3. 運行系統
```bash
streamlit run app_cloud.py
```

## 📁 檔案結構

```
hospital_loan_system/
├── app_cloud.py              # 雲端版主程式
├── app.py                    # 本地版主程式
├── google_sheets_config.py   # Google Sheets 連接設定
├── service_account.json      # Google 服務帳戶金鑰（需要自行建立）
└── README.md                 # 說明文件
```

## 🎯 使用說明

### 新增租借紀錄
1. 填寫表單基本資訊（表單編號、日期、領用部門）
2. 填寫物品明細（物品編號、摘要、數量、備註）
3. 設定借用和歸還日期
4. 填寫主管簽名資訊
5. 點擊「提交申請」

### 查看紀錄
1. 切換到「查看所有紀錄」頁面
2. 可按狀態篩選紀錄
3. 查看統計資訊
4. 下載 CSV 檔案

### 系統設定
1. 測試 Google Sheets 連接
2. 查看設定說明
3. 檢查系統狀態

## 🔧 故障排除

### 常見問題

**Q: 連接 Google Sheets 失敗**
A: 請檢查：
- `service_account.json` 檔案是否存在
- Google Sheets API 是否已啟用
- 服務帳戶是否有試算表的編輯權限

**Q: 資料沒有同步**
A: 請檢查：
- 網路連接是否正常
- 試算表是否正確分享給服務帳戶
- 重新載入頁面

**Q: 看不到 JSON 檔案中的電子郵件**
A: 開啟 `service_account.json` 檔案，找到 `client_email` 欄位

## 📞 技術支援

如需協助，請檢查：
1. 網路連接狀態
2. Google Cloud 設定
3. 檔案權限設定

## 🔄 版本資訊

- **v1.0** - 基本本地版功能
- **v2.0** - 雲端同步功能
- **v2.1** - 多人協作支援

---

💡 **提示：** 建議先在測試環境中驗證所有功能正常後，再投入正式使用。
