from app.util import gemini
from app.util import search
import json
import asyncio

# def main():
#     contents = [
#         "ソニーの売上をまとめてください",
#         """
#         以下のJSONフォーマットで出力してください
#         {"2022年": "", "2023年": "", "2024年": ""}
#         """,
#     ]
#     response = gemini.gemini_with_grounding(contents)
#     print(response.candidates)


# async def main():
#     contents = [
#         "Pythonを学ぶコンテンツを検討してください",
#         """
#         出力フォーマット
#         {"初心者": "", "中級者": "", "上級者": ""}
#         """,
#     ]
#     response = gemini.gemini(contents)
#     print(json.loads(response.candidates[0].content.parts[0].text))


# async def main():
#     response = await search.google("ソニーの2024年の売上")
#     with open("response.json", "w") as f:
#         f.write(json.dumps(response, ensure_ascii=False, indent=4))


async def main():
    response = await search.fetch_page(
        # "https://eetimes.itmedia.co.jp/ee/articles/2411/11/news059.html"
        # "https://gepuro.net"
        # "https://www.sony.com/ja/SonyInfo/IR/library/presen/er/archive.html"
        # "https://www.nitori.co.jp/about_us/corporate_data.html"
        # "https://semi-journal.jp/career/company/sony.html"
        # "https://global.toyota/jp/ir/finance/index.html"
        "https://dena.com/jp/ir/finance/highlight.html"
    )
    with open("response.md", "w") as f:
        f.write(response["markdown"])


if __name__ == "__main__":
    asyncio.run(main())
