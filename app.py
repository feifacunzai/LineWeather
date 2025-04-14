from flask import Flask, request, jsonify
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    SourceGroup,  # 用於群組訊息
    SourceRoom,   # 用於聊天室訊息
    SourceUser    # 用於個人訊息
)
import os
from dotenv import load_dotenv

load_dotenv()  # 讀取 .env 變數

app = Flask(__name__)

# 從環境變數讀取 LINE Token 和 CWA API Key
LINE_TOKEN = os.getenv("LINE_TOKEN")
LINE_SECRET = os.getenv("LINE_SECRET")
CWA_API_KEY = os.getenv("CWA_API_KEY")
USER_ID = os.getenv("USER_ID")  # 你的 LINE User ID

# 開關狀態儲存
callback_enabled = os.getenv('CALLBACK_ENABLED', 'true').lower() == 'true'

line_bot_api = LineBotApi(LINE_TOKEN)
handler = WebhookHandler(LINE_SECRET)

def get_weather():
    session = requests.session()
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={CWA_API_KEY}&locationName=臺北市"
    session.keey_alive = False
    session.proxies = {"https": "60.248.77.86:555"}
    response = session.get(url)
    data = response.json()
    
    # 解析天氣資料
    location = data["records"]["location"][0]
    elements = {elem["elementName"]: elem["time"] for elem in location["weatherElement"]}
    
    # 取得明日白天時段（06:00-18:00）的資料
    tomorrow_day = {
        "Wx": elements["Wx"][1]["parameter"]["parameterName"],  # 天氣現象
        "PoP": elements["PoP"][1]["parameter"]["parameterName"],  # 降雨機率
        "MinT": elements["MinT"][1]["parameter"]["parameterName"],  # 最低溫
        "MaxT": elements["MaxT"][1]["parameter"]["parameterName"],  # 最高溫
        "CI": elements["CI"][1]["parameter"]["parameterName"]  # 舒適度
    }
    
    # 組合 Emoji 對應表
    weather_icons = {
        "晴": "☀️",
        "多雲": "⛅",
        "陰": "☁️",
        "雨": "🌧️",
        "雷": "⛈️",
        "晴時多雲": "🌤️"
    }
    
    # 自動匹配 Emoji
    icon = "🌫️"
    for key in weather_icons:
        if key in tomorrow_day["Wx"]:
            icon = weather_icons[key]
            break
    
    # 組合成易讀訊息
    message = (
        f"{icon} 【台北明日天氣預報】\n"
        f"▸ 天氣狀況：{tomorrow_day['Wx']}\n"
        f"▸ 降雨機率：{tomorrow_day['PoP']}%\n"
        f"▸ 溫度範圍：{tomorrow_day['MinT']}°C ~ {tomorrow_day['MaxT']}°C\n"
        f"▸ 舒適度：{tomorrow_day['CI']}\n"
        "──────────────────\n"
        "⏰ 預報時段：06:00 ~ 18:00\n"
        "📅 資料來源：中央氣象署"
    )

    if int(tomorrow_day["PoP"]) > 50:
        message += "\n⚠️ 提醒：明日降雨機率較高，建議攜帶雨具！"
    return message

@app.route("/send-weather", methods=["GET"])
def send_weather():
    weather_info = get_weather()  # 取得美化後的天氣訊息
    line_bot_api.push_message(USER_ID, TextSendMessage(text=weather_info))
    return "天氣訊息已發送！"

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except Exception as e:
        print(e)
        return "Error", 400
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 判斷訊息來源類型
    if isinstance(event.source, SourceGroup):
        group_id = event.source.group_id
        print(f"群組 ID: {group_id}")
        if callback_enabled:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"你的正確 GROUP_ID 是：{group_id}")
            )
        # 這裡可以儲存 group_id 供後續使用
    elif isinstance(event.source, SourceRoom):
        room_id = event.source.room_id
        print(f"聊天室 ID: {room_id}")
        if callback_enabled:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"你的正確 ROOM_ID 是：{room_id}")
            )
    elif isinstance(event.source, SourceUser):
        user_id = event.source.user_id
        print(f"用戶 ID: {user_id}")
        if callback_enabled:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f"你的正確 USER_ID 是：{user_id}")
            )

if __name__ == "__main__":
    app.run(port=5000)