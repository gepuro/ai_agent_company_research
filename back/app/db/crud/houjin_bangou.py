from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession


async def fetch_houjin_bangou_with_condition(
    db: AsyncSession,
    company_name: str | None = None,
    corporate_number: str | None = None,
    prefecture_name: str | None = None,
    city_name: str | None = None,
    town_name: str | None = None,
):
    # データ取得の条件のいずれもNoneの場合は、Noneを返す
    if (
        company_name is None
        and corporate_number is None
        and (prefecture_name is None or city_name is None or town_name is None)
    ):
        return None

    query = select(models.HoujinBangou.corporate_number)

    if company_name is not None:
        query = query.filter(models.HoujinBangou.company_name == company_name)
    if corporate_number is not None:
        query = query.filter(models.HoujinBangou.corporate_number == corporate_number)
    if prefecture_name is not None and city_name is not None and town_name is not None:
        query = query.filter(
            models.HoujinBangou.prefecture_name == prefecture_name,
            models.HoujinBangou.city_name == city_name,
            models.HoujinBangou.town_name == town_name,
        )

    result = await db.execute(query)
    return result.mappings().fetchall()


# 法人番号を1000件ずつ取得する。法人番号順にならべて、paginationを指定することで、指定したページのデータを取得する
async def fetch_houjin_bangou_with_pagination(db: AsyncSession, pagination: int):
    query = select(models.HoujinBangou.corporate_number).order_by(
        models.HoujinBangou.corporate_number
    )
    page_size = 1000
    result = await db.execute(
        query.limit(page_size).offset(int(page_size * (pagination - 1)))
    )
    return result.mappings().fetchall()
