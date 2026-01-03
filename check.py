import os
import requests
from bs4 import BeautifulSoup

# 監視したいページ
URL = "https://www.keishicho-gto.metro.tokyo.lg.jp/keishicho-u/reserve/offerList_detail?tempSeq=679&accessFrom=offerList"

# GitHub Secrets から取得
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def notify(message):
    if not SLACK_WEBHOOK_URL:
        print("Slack Webhook URL が設定されていません")
        return

    payload = {"text": message}
    requests.post(SLACK_WEBHOOK_URL, json=payload)

def main():
    print("Checking reservation page...")

    r = requests.get(URL, timeout=30)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    page_text = soup.get_text()

    # 「×」が見当たらなければ空きがある可能性あり
    if "×" not in page_text:
        notify("🚨 予約に空きが出た可能性があります！\n" + URL)
    else:
        print("No availability yet.")

if __name__ == "__main__":
    main()
