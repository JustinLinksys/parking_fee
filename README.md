# 全台停車費查詢

Python Flask 後端 + 純前端 HTML/JS，查詢全台 21 縣市路邊停車費。

## 快速開始

```bash
cd ~/code/parking_fee

# 建立 venv 並安裝依賴
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 啟動後端
python3 app.py
# 或
./run.sh
```

打開瀏覽器訪問：http://localhost:5001

## 功能

- 輸入車牌號碼 + 選擇車種
- 勾選要查詢的縣市（預設全選 21 縣市）
- 後端並行呼叫各縣市政府 API
- 即時顯示各縣市查詢結果與應繳金額

## API

### POST /api/query

```json
{
  "car_id": "ABC-1234",
  "car_type": "C",
  "cities": ["taipei", "newtaipei", "taoyuan"]
}
```

### GET /api/cities

取得支援的縣市列表。

## 車種代碼

| 代碼 | 說明 |
|------|------|
| C | 自小客車 |
| M | 機車 |
| T | 自小貨車 |
| B | 大客車 |
| K | 大貨車 |
| H | 曳引車 |
| E | 電動自小客車 |

## 資料來源

TDX 運輸資料流通服務平台 + 各縣市政府停車費查詢 API

## 注意事項

- 部分縣市政府 API 使用自簽 SSL 憑證，後端已設定 `verify_ssl=False`
- 台中市 API 使用 HTTP（非加密）
- 查詢結果僅供參考，實際金額以各縣市停車管理單位公告為準
