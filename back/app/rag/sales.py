from app.rag import rag
from app.db import session

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "売上高", "year": "2024", "value": ""},
    {"name": "売上高", "year": "2023", "value": ""},
    {"name": "売上高", "year": "2022", "value": ""},
    {"name": "従業員数", "year": "2024", "value": ""},
    {"name": "従業員数", "year": "2023", "value": ""},
    {"name": "従業員数", "year": "2022", "value": ""},
    {"name": "営業利益", "year": "2024", "value": ""},
    {"name": "営業利益", "year": "2023", "value": ""},
    {"name": "営業利益", "year": "2022", "value": ""},
    {"name": "資本金", "year": "2024", "value": ""},
    {"name": "資本金", "year": "2023", "value": ""},
    {"name": "資本金", "year": "2022", "value": ""},
]
"""


async def fetch_sales(COMAPNY_NAME):
    db = session.SessionLocal()
    try:
        response = await rag.rag_with_googlesearch(
            db, f"{COMAPNY_NAME} 売上", OUTPUT_FORMAT
        )
        await db.close()
        return rag.delete_nouse_content(response, ["代表者"])
    except Exception as e:
        await db.close()
        return []
