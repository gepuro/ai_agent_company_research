from app.db import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.crud.common import insert_record, update_record
import hashlib


async def fetch_cache_url(db: AsyncSession, url: str):
    query = select(models.CacheUrl.url, models.CacheUrl.response).filter(
        models.CacheUrl.url == url
    )
    result = await db.execute(query)
    return result.mappings().fetchall()


async def add_cache_url(db: AsyncSession, url: str, response: str):
    cache = models.CacheUrl(url=url, response=response)
    return await insert_record(db, cache)


async def fetch_cache_gemini(db: AsyncSession, prompt: str):
    query = select(models.CacheGemini.prompt_hash, models.CacheGemini.response).filter(
        models.CacheGemini.prompt_hash == hashlib.sha256(prompt.encode()).hexdigest()
    )
    result = await db.execute(query)
    record = result.mappings().fetchall()
    if record:
        return record[0]
    return None


async def add_cache_gemini(
    db: AsyncSession, prompt: str, response: str, model="gemini-1.5-flash-002"
):
    cache = models.CacheGemini(
        prompt_hash=hashlib.sha256(prompt.encode()).hexdigest(),
        response=response,
        model=model,
    )
    return await insert_record(db, cache)


async def fetch_cache_google(db: AsyncSession, search_word: str):
    query = select(models.CacheGoogle.search_word, models.CacheGoogle.response).filter(
        models.CacheGoogle.search_word == search_word
    )
    result = await db.execute(query)
    return result.mappings().fetchall()


async def add_cache_google(db: AsyncSession, search_word: str, response: str):
    cache = models.CacheGoogle(search_word=search_word, response=response)
    return await insert_record(db, cache)


async def fetch_cache_company(db: AsyncSession, corporate_number: str):
    query = select(
        models.CacheCompany.corporate_number, models.CacheCompany.response
    ).filter(models.CacheCompany.corporate_number == corporate_number)
    result = await db.execute(query)
    return result.mappings().fetchall()


async def add_cache_company(db: AsyncSession, corporate_number: str, response: str):
    cache = models.CacheCompany(
        corporate_number=corporate_number, response=response
    ).__dict__
    cache.__delitem__("_sa_instance_state")
    return await update_record(
        db, models.CacheCompany, {"corporate_number": corporate_number}, cache
    )
