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
    {"name": "設立年", "value": ""},
    {"name": "事業内容", "value": ""}
    {"name": "売上高", "year": "2024", "value": ""},
    {"name": "売上高", "year": "2023", "value": ""},
    {"name": "売上高", "year": "2022", "value": ""},
    {"name": "従業員数", "year": "2024", "value": ""},
    {"name": "従業員数", "year": "2023", "value": ""},
    {"name": "従業員数", "year": "2022", "value": ""},
    {"name": "店舗数", "year": "2024", "value": ""},
    {"name": "店舗数", "year": "2023", "value": ""},
    {"name": "店舗数", "year": "2022", "value": ""},
    {"name": "事業所数", "year": "2024", "value": ""},
    {"name": "事業所数", "year": "2023", "value": ""},
    {"name": "事業所数", "year": "2022", "value": ""},
    {"name": "工場数", "year": "2024", "value": ""},
    {"name": "工場数", "year": "2023", "value": ""},
    {"name": "工場数", "year": "2022", "value": ""},
    {"name": "営業利益", "year": "2024", "value": ""},
    {"name": "営業利益", "year": "2023", "value": ""},
    {"name": "営業利益", "year": "2022", "value": ""},
    {"name": "資本金", "year": "2024", "value": ""},
    {"name": "資本金", "year": "2023", "value": ""},
    {"name": "資本金", "year": "2022", "value": ""},
    {"name": "企業の沿革", "value": ""},
    {"name": "理念", "value": ""},
]
"""


async def fetch_company_overview(COMAPNY_NAME):
    try:
        db = session.SessionLocal()
        response = await rag.rag_with_googlesearch(
            db,
            f"{COMAPNY_NAME} 会社概要",
            OUTPUT_FORMAT,
            prompt=f"{COMAPNY_NAME}の事業内容を調査してください。",
        )
        await db.close()
        return response
    except Exception as e:
        return []
