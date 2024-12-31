from app.util.geocoding import GeocodingAPI
from app.db import models
from app.db import session
from app.db.crud import common
import asyncio
from app.util import domain
import json


import re


def extract_names(data):
    """
    修正すべきパターン
    - 代表取締役社長執行役員  浜 田 晋 吾
    - 代表取締役社長 山田太郎
    """

    # 各行のリストに分割
    lines = data.splitlines()
    # 正規表現パターン：最後に漢字またはスペースを含む名前部分を抽出
    name_pattern = re.compile(r"[^\s]*\s[^\s]+$")

    # 各行を処理して名前を抽出
    names = []
    for line in lines:
        match = name_pattern.search(line)
        if match:
            names.append(match.group(0).strip())

    if len(names) > 0:

        name = names[0]

        # 「代表取締役社長　山田太郎」のような場合、名前部分を抽出。
        #  FIXME: 名字が4文字以上の場合にバグが出る
        if len(name.split(" ")[0]) >= 4:
            return name.split(" ")[1].replace(" ", "")

        return name.replace(" ", "")
    else:
        return None


# def extract_names(data):
#     # 各行のリストに分割
#     lines = data.splitlines()
#     # 正規表現パターン：行頭の肩書部分をスキップし、名前部分を抽出
#     name_pattern = re.compile(r"^(?:\S+\s)*(.+)$")

#     # 各行を処理して名前を抽出
#     names = []
#     for line in lines:
#         match = name_pattern.search(line)
#         if match:
#             names.append(match.group(1).strip())

#     return names


# def extract_names(data):
#     # 各行のリストに分割
#     lines = data.splitlines()
#     # 正規表現パターン: 最後の2つ以上の単語を名前部分として抽出
#     name_pattern = re.compile(
#         r"(?:\S+\s+)*([\u4E00-\u9FFF\u3040-\u30FF\uFF66-\uFF9F\s]+)$"
#     )

#     # 各行を処理して名前を抽出
#     names = []
#     for line in lines:
#         match = name_pattern.search(line)
#         if match:
#             names.append(match.group(1).strip())

#     return names


async def load_gbiz():
    with open("data/gbiz.json") as f:
        for line in f:
            record = json.loads(line)
            # print(record)
            record = {
                "corporate_number": record.get("corporate_number"),
                "representative_name": extract_names(record.get("代表者名", "")),
                "establishment_date": record.get("設立年月日"),
                "foundation_date": record.get("創業年"),
                "number_of_employees": record.get("従業員数"),
                "capital": record.get("資本金"),
                "url": record.get("企業ホームページ"),
                "domain": domain.get_domain_from_url(record.get("企業ホームページ")),
            }
            if record.get("url") is not None and record.get("url").find("http") != -1:
                print(record)


if __name__ == "__main__":
    asyncio.run(load_gbiz())
