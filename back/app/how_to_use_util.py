from app.util import gemini
from app.util import search
import json
import asyncio
from pydantic import BaseModel

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


class ResponseSchema(BaseModel):
    beginner_level: str
    mid_level: str
    senior_level: str


async def main():
    contents = [
        "Pythonを学ぶコンテンツを検討してください",
        """
        出力データの説明: ```
          - beginner_level: 初心者
          - mid_level: 中級者
          - senior_level: 上級者
        ```
        """,
    ]
    response = gemini.gemini_sync(contents, ResponseSchema)
    # print(response)
    response = json.loads(response.candidates[0].content.parts[0].text)
    print(type(response), response)


# async def main():
#     response = await search.google("ソニーの2024年の売上")
#     with open("response.json", "w") as f:
#         f.write(json.dumps(response, ensure_ascii=False, indent=4))


# async def main():
#     response = await search.fetch_page(
#         # "https://eetimes.itmedia.co.jp/ee/articles/2411/11/news059.html"
#         # "https://gepuro.net"
#         # "https://www.sony.com/ja/SonyInfo/IR/library/presen/er/archive.html"
#         # "https://www.nitori.co.jp/about_us/corporate_data.html"
#         # "https://semi-journal.jp/career/company/sony.html"
#         # "https://global.toyota/jp/ir/finance/index.html"
#         "https://dena.com/jp/ir/finance/highlight.html"
#     )
#     with open("response.md", "w") as f:
#         f.write(response["markdown"])


if __name__ == "__main__":
    asyncio.run(main())
