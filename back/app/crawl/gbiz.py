import httpx
from bs4 import BeautifulSoup, Comment
import pandas as pd
import re
from app.db.crud import houjin_bangou
from app.db import session
import asyncio
import json
import time
from loguru import logger


def tidy_text(text: str):
    text = re.sub(r"\s", " ", text)
    text = re.sub(r"\(.*?\)", "", text)
    return text


def fetch_gbiz(corporate_number: str):
    url = f"https://info.gbiz.go.jp/hojin/ichiran?hojinBango={corporate_number}"
    response = httpx.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.select("#collapse7 > dl")[0]

    dt_elements = table.find_all("dt")
    dd_elements = table.find_all("dd")

    # 辞書を作成
    data = {
        tidy_text(dt.get_text(strip=True)): tidy_text(dd.get_text(strip=True))
        for dt, dd in zip(dt_elements, dd_elements)
    }

    time.sleep(0.1)
    return data


async def get_corporate_number(db, pagination: int):
    houjin_bangou_data = await houjin_bangou.fetch_houjin_bangou_with_pagination(
        db, pagination
    )
    return houjin_bangou_data


async def save_gbiz_data():
    corporate_numbers = []
    try:
        with open("data/gbiz.json") as f:
            for line in f:
                data = json.loads(line)
                corporate_numbers.append(data["corporate_number"])
    except FileNotFoundError:
        pass

    async with session.SessionLocal() as db:
        for page in range(1, 1000000):
            logger.info(f"page: {page}")
            houjin_bangou_data = await get_corporate_number(db, page)
            if len(houjin_bangou_data) == 0:
                break

            for data in houjin_bangou_data:
                corporate_number = data["corporate_number"]
                if corporate_number in corporate_numbers:
                    continue

                gbiz_data = fetch_gbiz(corporate_number)
                gbiz_data["corporate_number"] = corporate_number

                with open(f"data/gbiz.json", "a") as f:
                    f.write(json.dumps(gbiz_data) + "\n")


if __name__ == "__main__":

    # print(fetch_gbiz("3430001044958"))
    # print(fetch_gbiz("1010401084202"))
    # asyncio.run(get_corporate_number(100000))

    # 取得済みの法人番号を取得
    asyncio.run(save_gbiz_data())
