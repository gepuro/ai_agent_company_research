import os
from datetime import datetime
from tenacity import retry, stop_after_attempt, stop_after_delay
import json
from googleapiclient.discovery import build
import pprint
import httpx
import asyncio
from app.util import bs
import markitdown
import tempfile
from loguru import logger
from timeout_executor import AsyncResult, TimeoutExecutor
from duckduckgo_search import DDGS
from app.core import config

# GOOGLE_API_KEY = "<取得したAPI鍵>"
# APIキーの利用は、IP制限をしている。
# 鍵の管理: https://console.cloud.google.com/apis/credentials?authuser=0&inv=1&invt=Ablz6g&project=ai-agent-cr-20241229
with open(config.API_KEY) as f:
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


async def fetch_page_with_tool(url):
    try:
        res = await fetch_page_with_httpx(url)
    except:
        res = None

    # splashを利用する場合はコメントアウトを外す
    # if res is None:
    #     res = await fetch_page_with_splash(url)
    return res


@retry(stop=stop_after_attempt(2) | stop_after_delay(10))
async def fetch_page_with_splash(url):
    logger.info(f"fetching {url} with splash")
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "http://splash:8050/render.html",
            params={"url": url, "wait": 1, "timeout": 10},
            timeout=10,
        )
    return res


@retry(stop=stop_after_attempt(3) | stop_after_delay(10))
async def fetch_page_with_httpx(url):
    logger.info(f"fetching {url} with httpx")
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(url, timeout=10, headers={"User-Agent": user_agent})
    return res


async def fetch_page_with_markitdown(url):
    logger.info(f"fetching {url} with markitdown")
    mid = markitdown.MarkItDown()
    text_content = mid.convert(url).text_content
    return text_content


async def fetch_page(url):
    """
    データ取得の優先順位
    1. Splashで取得
    2. HTTPXで取得
    3. 1か2で取得できなければNoneを返す(平仮名を含むかどうかで判定)
    4. MarkitDownを利用
    """
    logger.info(f"fetching {url}")
    res = await fetch_page_with_tool(url)

    if res is not None:
        if not contains_hiragana(res.text):
            res = None

    mid = markitdown.MarkItDown()
    if res is None:
        # FIXME: markitdownで取得は不安定？要調査
        return {"url": url, "markdown": ""}
        try:
            executor = TimeoutExecutor(15)
            text_content = executor.apply(fetch_page_with_markitdown, url).result()

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
            return {"url": url, "markdown": ""}
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
                return {"url": url, "markdown": ""}


async def google(KEYWORD, top_n=2):
    logger.info(f"google search: {KEYWORD}")

    # Google Customサーチ結果を取得
    s = build("customsearch", "v1", developerKey=GOOGLE_API_KEY)

    r = (
        s.cse()
        .list(q=KEYWORD, cx=CUSTOM_SEARCH_ENGINE_ID, lr="lang_ja", num=top_n, start=1)
        .execute()
    )

    items = r["items"][0:top_n]
    tasks = []
    for item in items:
        if item.get("mime", "") == "application/pdf":
            continue
        tasks.append(asyncio.ensure_future(fetch_page(item["link"])))
    task_results = await asyncio.gather(*tasks)
    url2markdown = {result["url"]: result["markdown"] for result in task_results}

    response = []
    for rank, item in enumerate(items):
        if item.get("mime", "") == "application/pdf":
            continue

        response.append(
            {
                "title": item["title"],
                "link": item["link"],
                "snippet": item["snippet"],
                "markdown": url2markdown[item["link"]],
                "rank": rank,
            }
        )
    return response

    # pprint.pprint(r["items"])
    # return r


async def duckduckgo_news(KEYWORD):
    with DDGS() as ddgs:
        results = list(
            ddgs.news(
                keywords=KEYWORD,
                region="jp-jp",
                safesearch="off",
                timelimit=None,
                max_results=10,
            )
        )
        return [
            {
                "title": result.get("title"),
                "link": result.get("url"),
                "snippet": result.get("body"),
                "rank": rank,
                "date": result.get("date"),
            }
            for rank, result in enumerate(results)
        ]
