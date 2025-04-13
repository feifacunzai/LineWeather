from flask import Flask, request
import requests
from linebot import LineBotApi
from linebot.models import TextSendMessage
import os
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env 變數

app = Flask(__name__)

# 從環境變數讀取 LINE Token 和 CWA API Key
LINE_TOKEN = os.getenv("LINE_TOKEN")
CWA_API_KEY = os.getenv("CWA_API_KEY")
USER_ID = os.getenv("USER_ID")  # 你的 LINE User ID

line_bot_api = LineBotApi(LINE_TOKEN)

def get_weather():
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={CWA_API_KEY}&locationName=臺北市"
    response = requests.get(url)
    data = response.json()
    
    # 解析明日天氣（臺北市的第一筆預報）
    forecast = data["records"]["location"][0]["weatherElement"]
    weather = forecast[0]["time"][1]["parameter"]["parameterName"]  # 天氣現象
    rain_prob = forecast[1]["time"][1]["parameter"]["parameterName"]  # 降雨機率
    min_temp = forecast[2]["time"][1]["parameter"]["parameterName"]  # 最低溫
    max_temp = forecast[4]["time"][1]["parameter"]["parameterName"]  # 最高溫
    
    return f"🌤️ 台北明日天氣預報\n天氣: {weather}\n降雨機率: {rain_prob}%\n溫度: {min_temp}°C ~ {max_temp}°C"

@app.route("/send-weather", methods=["GET"])
def send_weather():
    weather_info = get_weather()
    line_bot_api.push_message(USER_ID, TextSendMessage(text=weather_info))
    return "天氣訊息已發送！"

if __name__ == "__main__":
    app.run(port=5000)