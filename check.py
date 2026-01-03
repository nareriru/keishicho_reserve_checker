import os
import requests
from bs4 import BeautifulSoup

# ========= 設定 =========
URL = "https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=679&accessFrom=offerList"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")
# ========================

def notify(message):
    if not SLACK_WEBHOOK_URL:
        print("Slack Webhook URL が設定されていません")
        return

    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def main():
    # ←←← ここが「main」
    # テスト通知（動作確認用）
    notify("✅ テスト通知：GitHub Actions から正常に実行されました")

    r = requests.get(URL, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    page_text = soup.get_text()

    if "×" not in page_text:
        notify("🚨 予約に空きが出た可能性があります！\n" + URL)
    else:
        print("No availability yet.")

# ↓↓↓ この2行があることで main が実行される
if __name__ == "__main__":
    main()