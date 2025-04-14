# 🌦️ LINE 天氣預報機器人

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![LINE Messaging API](https://img.shields.io/badge/LINE%20Messaging%20API-✔-green.svg)
![中央氣象署API](https://img.shields.io/badge/中央氣象署API-✔-success.svg)
![Render](https://img.shields.io/badge/Deploy%20on-Render-46d3f7.svg)
![AI-Assisted](https://img.shields.io/badge/AI%20Assisted-DeepSeek%20Chat-orange.svg)

## ✨ 功能特色
- **精準天氣預報**：使用中央氣象署官方資料
- **定時自動推送**：每天23:00發送明日天氣
- **美觀格式**：精心設計的訊息排版與Emoji圖示
- **完全免費**：利用免費雲端服務部署
- **AI協作開發**：由 DeepSeek Chat 提供技術指導

## 🛠️ 技術架構
```mermaid
graph TD
    A[中央氣象署API] -->|取得天氣資料| B(Python Flask)
    B -->|格式化訊息| C[LINE Messaging API]
    D[GitHub Actions] -->|定時觸發| B
    B -->|部署| E[Render]
    F[DeepSeek Chat] -->|技術指導| B
```

## 🔧 使用技術與服務
| 技術/服務         | 用途                  | 備註                     |
|-------------------|-----------------------|--------------------------|
| Python 3.9+       | 後端程式邏輯          |                          |
| LINE Messaging API| 訊息推送              | 免費每月500則            |
| 中央氣象署API     | 天氣資料來源          | 免信用卡申請             |
| Render            | 免費雲端部署          |                          |
| GitHub Actions    | 定時任務觸發          | 替代Cron Job             |
| DeepSeek Chat     | 開發輔助              | 解決API整合問題          |

## 🧠 AI 協助內容
本專案在以下環節接受 DeepSeek Chat 的技術指導：
- LINE Messaging API 整合與錯誤排查
- 中央氣象署API 資料解析
- Render 部署配置
- GitHub Actions 定時任務設定
- 天氣訊息格式優化

## 🚀 快速部署
```bash
# 克隆倉庫
git clone https://github.com/feifacunzai/LineWeather.git
cd LineWeather

# 設定環境變數 (需自行建立 .env 檔案)
echo "LINE_TOKEN=YOUR_LINE_TOKEN" > .env
echo "CWA_API_KEY=YOUR_CWA_KEY" >> .env
echo "USER_ID=YOUR_USER_ID" >> .env
```

## 📝 使用說明
```
🌤️ 【台北明日天氣預報】
▸ 天氣狀況：晴時多雲
▸ 降雨機率：10%
▸ 溫度範圍：13°C ~ 29°C
▸ 舒適度：寒冷至舒適
──────────────────
⏰ 預報時段：06:00 ~ 18:00
📅 資料來源：中央氣象署
```

## 📜 授權
[MIT License](LICENSE) | **AI 貢獻聲明**：本專案核心邏輯由開發者實現，DeepSeek Chat 提供技術建議與除錯協助。

---

<p align="center">
  <img src="https://img.shields.io/github/last-commit/yourusername/line-weather-bot" alt="最後更新">
  <img src="https://img.shields.io/github/issues/yourusername/line-weather-bot" alt="問題">
  <img src="https://img.shields.io/badge/狀態-運作中-brightgreen" alt="狀態">
</p>

<p align="center">
  <em>🤖 人機協作開發範例 | 💡 天氣資訊從此主動報到！</em>
</p>
