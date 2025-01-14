from app.rag import rag
from app.db import session

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "競合企業1", "value": ""}
    {"name": "競合企業2", "value": ""},
    {"name": "競合企業3", "value": ""},
]
"""


async def fetch_company_competitor(COMAPNY_NAME):
    db = session.SessionLocal()
    try:
        response = await rag.rag_with_googlesearch(
            db,
            f"{COMAPNY_NAME} 競合",
            OUTPUT_FORMAT,
            prompt=f"{COMAPNY_NAME}の競合企業を調査してください。",
        )
        await db.close()
        return rag.delete_nouse_content(response, ["代表者"])
    except Exception as e:
        await db.close()
        return []
