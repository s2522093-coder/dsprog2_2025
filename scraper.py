import requests
from bs4 import BeautifulSoup
import time
import sqlite3
from datetime import datetime, timedelta

class HakoneFinalScraper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.setup_db()

    def setup_db(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS hotel_prices (hotel_name TEXT, price INTEGER, stay_date TEXT)')
        conn.commit()
        conn.close()

    def scrape_date(self, year, month, day):
        # 成功した時のパラメーターを完全に再現
        url = "https://search.travel.rakuten.co.jp/ds/vacant/searchVacant"
        checkin = datetime(year, month, day)
        checkout = checkin + timedelta(days=1)

        params = {
            "f_dai": "japan", "f_chu": "kanagawa", "f_shou": "hakone",
            "f_nen1": checkin.year, "f_tuki1": checkin.month, "f_hi1": checkin.day,
            "f_nen2": checkout.year, "f_tuki2": checkout.month, "f_hi2": checkout.day,
            "f_heya_su": 1, "f_otona_su": 1, "f_hyoji": 30,
            "f_sort": "hotel", "f_tab": "hotel", "f_kind": "area", "f_cd": "03"
        }
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        try:
            res = requests.get(url, params=params, headers=headers, timeout=10)
            if res.status_code != 200: return []
            soup = BeautifulSoup(res.content, 'html.parser')
            
            hotels_data = []
            # さっき成功したセレクタ 'section h2 a' を使用
            hotel_titles = soup.select('section h2 a')
            if not hotel_titles:
                hotel_titles = soup.select('h2 a')

            for title_el in hotel_titles:
                try:
                    name = title_el.get_text(strip=True)
                    # 価格を頑張って探す
                    card = title_el.find_parent('section')
                    price = 0
                    if card:
                        price_el = card.select_one('.itemPrc')
                        if price_el:
                            price_text = price_el.get_text(strip=True).replace(',','').replace('円','').replace('～','')
                            price = int(price_text)
                    
                    hotels_data.append((name, price, checkin.strftime('%Y-%m-%d')))
                except:
                    continue
            return hotels_data
        except:
            return []

    def save_to_db(self, data):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        c.executemany('INSERT INTO hotel_prices VALUES (?,?,?)', data)
        conn.commit()
        conn.close()

if __name__ == "__main__":
    db_file = 'hakone_final_data.db'
    scraper = HakoneFinalScraper(db_file)

    # 4月〜6月の「火曜」と「土曜」を両方チェック
    current_date = datetime(2026, 4, 1)
    end_date = datetime(2026, 6, 30)

    print("データ収集を開始します（火曜と土曜をチェック）...")

    while current_date <= end_date:
        # 1 = 火曜, 5 = 土曜
        if current_date.weekday() in [1, 5]: 
            y, m, d = current_date.year, current_date.month, current_date.day
            day_name = "土曜" if current_date.weekday() == 5 else "火曜"
            print(f"Checking {y}-{m}-{d} ({day_name})...")
            
            data = scraper.scrape_date(y, m, d)
            if data:
                scraper.save_to_db(data)
                print(f"  →【成功】{len(data)}件保存！")
            else:
                print(f"  →【データなし】")
            
            time.sleep(2)
        current_date += timedelta(days=1)

    print("\n完了しました！")
