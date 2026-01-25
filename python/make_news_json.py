import json
import os

from google_search_rss import fetch_google_news
from naver_search_rss import fetch_naver_news

fileNameMap = {
    "테슬라": "tesla",
    "싸이클": "cyclone",
    "등산": "hiking",
}

def main():
    keyword = "테슬라"
    news_results = fetch_naver_news(keyword, 20)
    news_results.extend(fetch_google_news(keyword, 20))

    news_results.sort(key=lambda x: x["published_at"], reverse=True)

    if not news_results:
        print("No news found or error occurred.")
        return

    out_path = os.path.join("json", f"{fileNameMap[keyword]}_news.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(news_results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
