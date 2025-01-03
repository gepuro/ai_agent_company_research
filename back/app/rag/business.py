from app.rag import rag
from app.db import session

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "事業1", "value": ""}
    {"name": "事業2", "value": ""},
    {"name": "事業3", "value": ""},
]
"""


async def fetch_business(COMAPNY_NAME):
    try:
        db = session.SessionLocal()
        response = await rag.rag_with_googlesearch(
            db,
            f"{COMAPNY_NAME} 事業",
            OUTPUT_FORMAT,
            prompt=f"{COMAPNY_NAME}の事業内容を調査してください。",
        )
        await db.close()
        # return response
        return rag.delete_nouse_content(response, ["代表者"])
    except Exception as e:
        return []
