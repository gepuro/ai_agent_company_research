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
    {"name": "事業概要", "value": ""}
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
    {"name": "事業1", "value": ""}
    {"name": "事業2", "value": ""},
    {"name": "事業3", "value": ""},
    {"name": "競合企業1", "value": ""},
    {"name": "競合企業2", "value": ""},
    {"name": "競合企業3", "value": ""},
    {"name": "求める人材像", "value": ""}
    {"name": "スキル1", "value": ""},
    {"name": "スキル2", "value": ""},
    {"name": "スキル3", "value": ""},
    {"name": "強み", "value": ""},
    {"name": "弱み", "value": ""},
    {"name": "機会", "value": ""},
    {"name": "脅威", "value": ""},
]
"""


async def fetch_any_data(COMAPNY_NAME, search_word, top_n=3):
    db = session.SessionLocal()
    try:
        response = await rag.rag_with_googlesearch(
            db,
            f"{search_word}",
            OUTPUT_FORMAT,
            prompt=f"{COMAPNY_NAME}を調査してください。",
            top_n=top_n,
        )
        await db.close()
        return rag.delete_nouse_content(response, ["代表者"])
    except Exception as e:
        await db.close()
        return []
