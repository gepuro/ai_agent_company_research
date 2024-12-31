from app.rag import rag

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "強み", "value": ""},
    {"name": "弱み", "value": ""},
    {"name": "機会", "value": ""},
    {"name": "脅威", "value": ""},
]
"""


async def fetch_company_swot(COMAPNY_NAME):
    return await rag.rag_with_googlesearch(
        f"{COMAPNY_NAME} 事業 強み",
        OUTPUT_FORMAT,
        prompt="SWOT分析を行ってください。",
    )