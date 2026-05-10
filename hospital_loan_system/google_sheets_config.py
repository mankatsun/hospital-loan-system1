import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import json

# Google Sheets 設定
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# 這裡需要您上傳 Google Cloud 的服務帳戶 JSON 檔案
SERVICE_ACCOUNT_FILE = 'service_account.json'

class GoogleSheetsManager:
    def __init__(self, sheet_name="醫院物品租借系統"):
        self.sheet_name = sheet_name
        self.sheet = None
        self.worksheet = None
        
    def connect(self):
        """連接到 Google Sheets"""
        try:
            # 先嘗試從環境變數讀取 (適用於部署平台)
            import os
            credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            if credentials_json:
                from google.oauth2.service_account import Credentials as ServiceAccountCredentials
                import json
                creds_info = json.loads(credentials_json)
                creds = ServiceAccountCredentials.from_service_account_info(creds_info, scopes=SCOPES)
                client = gspread.authorize(creds)
            else:
                # 如果有服務帳戶檔案，使用它
                creds = Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
                client = gspread.authorize(creds)
        except FileNotFoundError:
            # 如果兩種檔案都不存在，拋出錯誤
            raise FileNotFoundError(
                "找不到 Google Sheets 認證檔案。請確保：\n"
                "1. 在本地環境中有 service_account.json 檔案，或\n"
                "2. 在雲端環境中設定了 GOOGLE_APPLICATION_CREDENTIALS_JSON 環境變數"
            )
        except Exception as e:
            # 其他錯誤
            raise Exception(f"Google Sheets 連接失敗：{str(e)}")
        
        # 開啟或建立試算表
        try:
            self.sheet = client.open(self.sheet_name)
        except gspread.SpreadsheetNotFound:
            self.sheet = client.create(self.sheet_name)
        
        # 開啟或建立工作表
        try:
            self.worksheet = self.sheet.worksheet("租借紀錄")
        except gspread.WorksheetNotFound:
            self.worksheet = self.sheet.add_worksheet("租借紀錄", 1000, 20)
            # 建立標題列
            headers = [
                "表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", 
                "借用日期", "歸還日期", "備註", "借用部門主管", "借出部門主管", "狀態"
            ]
            self.worksheet.append_row(headers)
        
        return True
    
    def load_data(self):
        """從 Google Sheets 載入資料"""
        if not self.worksheet:
            self.connect()
        
        data = self.worksheet.get_all_records()
        if data:
            return pd.DataFrame(data)
        else:
            # 如果沒有資料，建立空的 DataFrame
            return pd.DataFrame(columns=[
                "表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", 
                "借用日期", "歸還日期", "備註", "借用部門主管", "借出部門主管", "狀態"
            ])
    
    def save_data(self, df):
        """儲存資料到 Google Sheets"""
        if not self.worksheet:
            self.connect()
        
        # 清除現有資料（保留標題列）
        self.worksheet.clear()
        headers = [
            "表單編號", "領用部門", "日期", "物品編號", "摘要", "數量", 
            "借用日期", "歸還日期", "備註", "借用部門主管", "借出部門主管", "狀態"
        ]
        self.worksheet.append_row(headers)
        
        # 新增所有資料列
        for index, row in df.iterrows():
            self.worksheet.append_row(row.tolist())
        
        return True
    
    def add_record(self, record):
        """新增單筆紀錄"""
        if not self.worksheet:
            self.connect()
        
        self.worksheet.append_row(record)
        return True
