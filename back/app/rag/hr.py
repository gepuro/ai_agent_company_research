from app.rag import rag

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "求める人材像", "value": ""}
    {"name": "スキル1", "value": ""},
    {"name": "スキル2", "value": ""},
    {"name": "スキル3", "value": ""},
]
"""


async def fetch_hr(COMAPNY_NAME):
    return await rag.rag_with_googlesearch(
        f"{COMAPNY_NAME} 採用",
        OUTPUT_FORMAT,
        prompt=f"{COMAPNY_NAME}の求める人材像を調査してください。",
    )
