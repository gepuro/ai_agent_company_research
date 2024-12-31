from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_corporate_site(
    db: AsyncSession,
    url: str | None = None,
    domain: str | None = None,
):
    if url is None and domain is None:
        return None

    query = select(models.CorporateSite.url)
    if url is not None:
        query = query.filter(models.CorporateSite.url == url)
    if domain is not None:
        query = query.filter(models.CorporateSite.domain == domain)

    result = await db.execute(query)
    return result.mappings().fetchall()
