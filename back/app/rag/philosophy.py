from app.rag import rag
from app.db import session
from loguru import logger

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "本社所在地", "value": ""},
    {"name": "理念", "value": ""},
]
"""


async def fetch_company_phiolosophy(COMAPNY_NAME):
    db = session.SessionLocal()
    try:
        response = await rag.rag_with_googlesearch(
            db, f"{COMAPNY_NAME} 理念", OUTPUT_FORMAT
        )
        await db.close()
        return rag.delete_nouse_content(response, ["代表者"])
    except Exception as e:
        logger.error(e)
        await db.close()
        return []
