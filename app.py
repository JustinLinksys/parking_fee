#!/usr/bin/env python3
"""
全台停車費查詢 - Python Flask 後端
繞過瀏覽器 CORS 限制，直接呼叫各縣市政府 API
"""

from flask import Flask, request, jsonify, render_template_string
import requests
import urllib3

# 停用 SSL 警告（部分政府網站憑證有問題）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# 各縣市 API 設定
CITY_APIS = {
    "taipei": {
        "name": "台北市",
        "url": "https://trafficapi.pma.gov.taipei/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "newtaipei": {
        "name": "新北市",
        "url": "https://trafficapi.traffic.ntpc.gov.tw/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "keelung": {
        "name": "基隆市",
        "url": "https://park.klcg.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "taoyuan": {
        "name": "桃園市",
        "url": "https://bill-epark.tycg.gov.tw/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "hsinchu_city": {
        "name": "新竹市",
        "url": "https://histmp.hccg.gov.tw:5443/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "hsinchu_county": {
        "name": "新竹縣",
        "url": "https://hcpark.hchg.gov.tw/NationalParkingPayBillInquiry/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "miaoli": {
        "name": "苗栗縣",
        "url": "https://miaoliparking.jotangi.com.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "taichung": {
        "name": "台中市",
        "url": "http://tcparkingapi.taichung.gov.tw:8081/NationalParkingPayBillInquiry.Api/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "changhua": {
        "name": "彰化縣",
        "url": "https://chpark.chcg.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "yunlin": {
        "name": "雲林縣",
        "url": "https://parking.yunlin.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "chiayi_city": {
        "name": "嘉義市",
        "url": "https://parking.chiayi.gov.tw/cypark/api/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "chiayi_county": {
        "name": "嘉義縣",
        "url": "https://8voc0wuf1g.execute-api.ap-southeast-1.amazonaws.com/default/chiayi/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "tainan": {
        "name": "台南市",
        "url": "https://parkingbill.tainan.gov.tw/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "kaohsiung": {
        "name": "高雄市",
        "url": "https://kpp.tbkc.gov.tw/parking/V1/parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": False,  # SSL 憑證有問題
    },
    "pingtung": {
        "name": "屏東縣",
        "url": "https://8voc0wuf1g.execute-api.ap-southeast-1.amazonaws.com/default/pingtung/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "nantou": {
        "name": "南投縣",
        "url": "https://parking.nantou.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "yilan": {
        "name": "宜蘭縣",
        "url": "https://billparking.e-land.gov.tw/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "hualien": {
        "name": "花蓮縣",
        "url": "https://hl.parchere.com.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "taitung": {
        "name": "台東縣",
        "url": "https://tt.guoyun.com.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "kinmen": {
        "name": "金門縣",
        "url": "https://km.guoyun.com.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
    "penghu": {
        "name": "澎湖縣",
        "url": "https://parking.penghu.gov.tw/TrafficPayBill/Parking/PayBill/CarID/{car_id}/CarType/{car_type}",
        "verify_ssl": True,
    },
}


def query_city(city_key, car_id, car_type):
    """查詢單一縣市停車費"""
    city = CITY_APIS.get(city_key)
    if not city:
        return {"success": False, "error": f"未知縣市: {city_key}"}

    url = city["url"].format(car_id=car_id, car_type=car_type)
    verify_ssl = city.get("verify_ssl", True)

    try:
        resp = requests.get(
            url,
            timeout=10,
            verify=verify_ssl,
            headers={"Accept": "application/json", "User-Agent": "ParkingFeeQuery/1.0"},
        )
        resp.raise_for_status()
        data = resp.json()

        # 解析回應格式
        bills = []
        if isinstance(data, list):
            bills = data
        elif isinstance(data, dict):
            if data.get("Result") and isinstance(data["Result"], list):
                bills = data["Result"]
            elif data.get("data") and isinstance(data["data"], list):
                bills = data["data"]
            elif data.get("PayBills") and isinstance(data["PayBills"], list):
                bills = data["PayBills"]

        total_amount = sum(
            float(b.get("Amount") or b.get("amount") or b.get("TotalAmount") or 0)
            for b in bills
        )

        return {
            "success": True,
            "city": city["name"],
            "bills": bills,
            "bill_count": len(bills),
            "total_amount": total_amount,
            "raw": data,  # 保留原始回應供除錯
        }

    except requests.exceptions.SSLError as e:
        return {"success": False, "city": city["name"], "error": f"SSL 錯誤: {str(e)}"}
    except requests.exceptions.Timeout:
        return {"success": False, "city": city["name"], "error": "查詢逾時 (10s)"}
    except requests.exceptions.ConnectionError as e:
        return {"success": False, "city": city["name"], "error": f"連線失敗: {str(e)}"}
    except Exception as e:
        return {"success": False, "city": city["name"], "error": str(e)}


@app.route("/")
def index():
    """主頁面"""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return html


@app.route("/api/query", methods=["POST"])
def api_query():
    """查詢停車費 API"""
    data = request.get_json()
    car_id = data.get("car_id", "").strip().upper()
    car_type = data.get("car_type", "C")
    cities = data.get("cities", list(CITY_APIS.keys()))

    if not car_id:
        return jsonify({"success": False, "error": "請輸入車牌號碼"}), 400

    results = {}
    total_bills = 0
    total_amount = 0
    success_count = 0

    for city_key in cities:
        if city_key not in CITY_APIS:
            continue
        result = query_city(city_key, car_id, car_type)
        results[city_key] = result

        if result.get("success"):
            success_count += 1
            total_bills += result.get("bill_count", 0)
            total_amount += result.get("total_amount", 0)

    return jsonify(
        {
            "success": True,
            "car_id": car_id,
            "car_type": car_type,
            "summary": {
                "queried_cities": len(cities),
                "success_cities": success_count,
                "total_bills": total_bills,
                "total_amount": total_amount,
            },
            "results": results,
        }
    )


@app.route("/api/cities", methods=["GET"])
def api_cities():
    """取得支援的縣市列表"""
    cities = [
        {"key": k, "name": v["name"], "url": v["url"]}
        for k, v in CITY_APIS.items()
    ]
    return jsonify({"cities": cities})


if __name__ == "__main__":
    port = 5001
    print("🅿️  全台停車費查詢後端啟動")
    print(f"📍 http://localhost:{port}")
    print(f"📋 支援 {len(CITY_APIS)} 個縣市")
    app.run(host="0.0.0.0", port=port, debug=True)
