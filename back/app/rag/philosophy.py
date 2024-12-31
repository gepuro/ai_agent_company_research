from app.rag import rag

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "理念", "value": ""},
]
"""


async def fetch_company_phiolosophy(COMAPNY_NAME):
    return await rag.rag_with_googlesearch(f"{COMAPNY_NAME} 理念", OUTPUT_FORMAT)
