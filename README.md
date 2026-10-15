# 全台停車費查詢

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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

- TDX 運輸資料流通服務平台 - 路邊停車費查詢 API：
  https://tdx.transportdata.tw/api-service-thirdParty/parkingFee
- 全國路邊停車費查詢 API 服務規範：
  https://drive.google.com/file/d/1bu7X4QWhDnXsypu82KJtPVW7K6wbdpXQ/view?usp=sharing

### 各縣市 API Endpoint

| 縣市 | API URL |
|------|---------|
| 台北市 | https://trafficapi.pma.gov.taipei/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 新北市 | https://trafficapi.traffic.ntpc.gov.tw/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 基隆市 | https://park.klcg.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 桃園市 | https://bill-epark.tycg.gov.tw/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 新竹市 | https://histmp.hccg.gov.tw:5443/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 新竹縣 | https://hcpark.hchg.gov.tw/NationalParkingPayBillInquiry/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 苗栗縣 | https://miaoliparking.jotangi.com.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 台中市 | http://tcparkingapi.taichung.gov.tw:8081/NationalParkingPayBillInquiry.Api/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 彰化縣 | https://chpark.chcg.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 雲林縣 | https://parking.yunlin.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 嘉義市 | https://parking.chiayi.gov.tw/cypark/api/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 嘉義縣 | https://8voc0wuf1g.execute-api.ap-southeast-1.amazonaws.com/default/chiayi/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 台南市 | https://parkingbill.tainan.gov.tw/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 高雄市 | https://kpp.tbkc.gov.tw/parking/V1/parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 屏東縣 | https://8voc0wuf1g.execute-api.ap-southeast-1.amazonaws.com/default/pingtung/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 南投縣 | https://parking.nantou.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 宜蘭縣 | https://billparking.e-land.gov.tw/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 花蓮縣 | https://hl.parchere.com.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 台東縣 | https://tt.guoyun.com.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 金門縣 | https://km.guoyun.com.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |
| 澎湖縣 | https://parking.penghu.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{CarID}/CarType/{CarType} |

## License

本專案以 [MIT License](LICENSE) 釋出。

**注意**：本 License 僅適用於程式碼本身。透過本工具查詢之停車費資料，其著作權與使用規範仍依 [TDX 運輸資料流通服務平台資料使用授權規範](https://tdx.transportdata.tw/term) 及各縣市政府相關規定辦理。

## 注意事項

- 部分縣市政府 API 使用自簽 SSL 憑證，後端已設定 `verify_ssl=False`
- 台中市 API 使用 HTTP（非加密）
- 查詢結果僅供參考，實際金額以各縣市停車管理單位公告為準
