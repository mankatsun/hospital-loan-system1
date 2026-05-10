# 🚀 醫院物品租借系統部署指南

## 🌟 推薦：Streamlit Cloud 部署

### ✅ 優點：
- 完全免費
- 一鍵部署
- 自動 HTTPS
- 支援 GitHub 連接
- 無需管理伺服器

### 📋 步驟：

#### 1. 準備檔案
您的專案已經包含所有必要檔案：
- `app_cloud.py` - 主程式
- `requirements.txt` - 套件依賴
- `google_sheets_config.py` - Google Sheets 連接

#### 2. 建立 GitHub 儲存庫
```bash
# 初始化 Git
git init
git add .
git commit -m "Initial commit"

# 連接到 GitHub
git remote add origin https://github.com/您的用戶名/hospital-loan-system.git
git push -u origin main
```

#### 3. Streamlit Cloud 部署
1. 前往 [Streamlit Cloud](https://streamlit.io/cloud)
2. 使用 GitHub 帳號登入
3. 點擊 "New app"
4. 選擇您的 GitHub 儲存庫
5. 設定：
   - **Main file path**: `app_cloud.py`
   - **Python version**: `3.11` 或更新

#### 4. 設定環境變數
在 Streamlit Cloud 中設定：
```
# Google Sheets 認證 (需要將 JSON 內容貼上)
GOOGLE_APPLICATION_CREDENTIALS_JSON: "您的 JSON 內容"
```

---

## 🔧 其他部署選擇

### Heroku 部署
```bash
# 建立 Procfile
echo "web: streamlit run app_cloud.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# 部署到 Heroku
heroku create your-app-name
git push heroku main
```

### Docker 部署
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app_cloud.py"]
```

---

## ⚠️ 重要注意事項

### Google Sheets 認證
部署時需要重新處理認證：
1. **不要**上傳 `service_account.json` 到 Git
2. 在部署平台設定環境變數
3. 修改程式碼使用環境變數

### 安全性
- 認證檔案不要公開
- 定期更新 API 金鑰
- 限制 Google Sheets 分享權限

---

## 📱 部署後功能

部署後您的系統將擁有：
- 🔗 公開 URL (例如：https://your-app.streamlit.app)
- 🌐 全球可存取
- 📱 手機友好界面
- 👥 多人同時使用
- 🔄 自動更新

---

## 🎯 快速部署檢查清單

- [ ] 建立 GitHub 儲存庫
- [ ] 上傳程式碼
- [ ] 設定 Streamlit Cloud
- [ ] 配置環境變數
- [ ] 測試部署功能
- [ ] 分享 URL 給團隊

---

## 🆘 故障排除

### 常見問題：
1. **認證失敗** - 檢查環境變數設定
2. **Google Sheets 連接失敗** - 確認 API 權限
3. **程式無法啟動** - 檢查 requirements.txt

### 技術支援：
- 查看 Streamlit Cloud 日誌
- 檢查 Google Cloud Console
- 確認所有檔案正確上傳
