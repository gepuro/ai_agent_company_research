from app.rag import rag
from app.db import session

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "特色", "value": ""},
    {"name": "電話番号", "value": ""},
    {"name": "メールアドレス", "value": ""},
    {"name": "本社所在地", "value": ""},
    {"name": "従業員数", "year": "2024", "value": ""},
    {"name": "従業員数", "year": "2023", "value": ""},
    {"name": "従業員数", "year": "2022", "value": ""},
]
"""


async def fetch_employee(COMAPNY_NAME):
    try:
        db = session.SessionLocal()
        response = await rag.rag_with_googlesearch(
            db, f"{COMAPNY_NAME} 社員数", OUTPUT_FORMAT
        )
        await db.close()
        return response
    except Exception as e:
        return []
