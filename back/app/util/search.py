import os
from datetime import datetime
import json
from googleapiclient.discovery import build
import pprint
import httpx
import asyncio
from app.util import bs
import markitdown
import tempfile

# GOOGLE_API_KEY = "<取得したAPI鍵>"
# APIキーの利用は、IP制限をしている。
with open(".secret/api_key.txt") as f:
    GOOGLE_API_KEY = f.read().strip()

CUSTOM_SEARCH_ENGINE_ID = "57d60b9d0fe3e4a0e"  # https://programmablesearchengine.google.com/controlpanel/all で作成
# KEYWORD = "プログラミング"


import re


def contains_hiragana(text):
    """
    指定された文字列に平仮名が含まれているかを判定する関数。

    Args:
        text (str): 判定する文字列

    Returns:
        bool: 平仮名が含まれていればTrue、含まれていなければFalse
    """
    # 平仮名の範囲を表す正規表現
    hiragana_pattern = re.compile(r"[\u3041-\u3096]")
    return bool(hiragana_pattern.search(text))


async def fetch_page_with_splash(url):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                "http://splash:8050/render.html",
                params={"url": url, "wait": 1},
            )
        return res
    except:
        return None


async def fetch_page_with_httpx(url):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(url)
        return res
    except:
        return None


async def fetch_page(url):
    """
    データ取得の優先順位
    1. Splashで取得
    2. HTTPXで取得
    3. 1か2で取得できなければNoneを返す(平仮名を含むかどうかで判定)
    4. MarkitDownを利用
    """

    res = await fetch_page_with_splash(url)
    if res is None:
        res = await fetch_page_with_httpx(url)

    if res is not None:
        if not contains_hiragana(res.text):
            res = None

    mid = markitdown.MarkItDown()
    if res is None:
        try:
            text_content = mid.convert(url).text_content

            # ワークアラウンド: markitdownのバグで、htmlをそのまま返す場合がある。ファイルに一度保存してから、変換する
            if text_content.find("<head>") > 0:
                with tempfile.NamedTemporaryFile(
                    delete_on_close=True, suffix=".html", mode="w"
                ) as fp:
                    fp.write(text_content)
                    fp.flush()
                    return {
                        "url": url,
                        "markdown": mid.convert(fp.name).text_content,
                    }
            else:
                return {"url": url, "markdown": text_content}

        except:
            return {"url": url, "markdown": None}
    else:
        with tempfile.NamedTemporaryFile(
            delete_on_close=True, suffix=".html", mode="w"
        ) as fp:
            try:
                fp.write(res.text)
                fp.flush()
                return {
                    "url": url,
                    "markdown": mid.convert(fp.name).text_content,
                }
            except:
                return {"url": url, "markdown": None}


async def google(KEYWORD):
    # Google Customサーチ結果を取得
    s = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

    r = (
        s.cse()
        .list(q=KEYWORD, cx=CUSTOM_SEARCH_ENGINE_ID, lr="lang_ja", num=10, start=1)
        .execute()
    )

    tasks = []
    for item in r["items"]:
        if item.get("mime", "") == "application/pdf":
            continue
        tasks.append(asyncio.ensure_future(fetch_page(item["link"])))
    task_results = await asyncio.gather(*tasks)
    url2markdown = {result["url"]: result["markdown"] for result in task_results}

    response = []
    for item in r["items"]:
        if item.get("mime", "") == "application/pdf":
            continue

        response.append(
            {
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"],
                "markdown": url2markdown[item["link"]],
            }
        )
    return response

    # pprint.pprint(r["items"])
    # return r
