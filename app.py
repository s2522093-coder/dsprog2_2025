import sqlite3
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# DB接続関数
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# 天気情報を取得してDBに保存し、DBからデータを返すエンドポイント
@app.route('/weather/<area_code>')
def get_weather(area_code):
    # 1. 気象庁APIから最新データを取得
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
    response = requests.get(url)
    data = response.json()

    # 2. DBに保存
    conn = get_db_connection()
    cur = conn.cursor()
    
    # 例：今日・明日・明後日の予報を保存
    time_series = data[0]['timeSeries'][0]
    dates = time_series['timeDefines']
    weathers = time_series['areas'][0]['weathers']

    for date, weather in zip(dates, weathers):
        cur.execute(
            "INSERT INTO forecasts (area_code, target_date, weather_text) VALUES (?, ?, ?)",
            (area_code, date, weather)
        )
    conn.commit()

    # 3. DBから最新のデータを取得して返す
    rows = cur.execute(
        "SELECT * FROM forecasts WHERE area_code = ? ORDER BY get_date DESC LIMIT 3",
        (area_code,)
    ).fetchall()
    
    conn.close()
    
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(debug=True)