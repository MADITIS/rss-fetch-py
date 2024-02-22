import json
from typing import List
from bs4 import BeautifulSoup
from src.models import Post, Article
import httpx
from datetime import datetime


target_url = "https://announcements.bybit.com/en/?category=new_crypto&page=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

posts: list[Post] = []


async def scrape():
    async with httpx.AsyncClient() as client:
        response = await client.get(target_url, timeout=30, headers=headers)
        # if response.status_code
        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            # a_tags = soup.select(".article-list > a")

            # for article in a_tags[:1]:
            # print(a_tags)
            # if a_tags:
            # url_tag = a_tags[0]
            # print(url_tag)
            # url = f"https://announcements.bybit.com{url_tag.get("href")}"
            # image_response = await client.get(url, timeout=30, headers=headers)
            # print(image_response.text)
            # image_soup = BeautifulSoup(image_response.text, "html.parser")
            # print(image_soup.prettify())
            script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
            json_blob = json.loads(script_tag.get_text())
            # asset = image_soup.find("div", class_="embedded-asset")
            # print("asset", asset)

            json_data = json_blob["props"]["pageProps"]["articleInitEntity"]["list"]
            articles: List[Article] = [Article(**article) for article in json_data]
            for article in articles:
                posted_date = extract_date(article.date_timestamp)
                start_date = extract_date(article.start_date_timestamp)
                end_date = extract_date(article.end_date_timestamp)
                thumbnail_url = article.thumbnail_url
                title = article.title
                url = article.url
                description = article.description
                post = Post(
                    title=title,
                    date=posted_date,
                    url=url,
                    thumbnail=thumbnail_url,
                    start_date=start_date,
                    end_date=end_date,
                    description=description,
                )
                posts.append(post)


def extract_date(unix_time: int, format: str = "%B %d, %Y"):
    return datetime.utcfromtimestamp(unix_time).strftime(format)
