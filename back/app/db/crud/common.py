import traceback

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.future import select


async def insert_record(db: AsyncSession, record):
    try:
        db.add(record)
        await db.commit()
        await db.refresh(record)
        # logger.info(f"{record.__tablename__}: {record.__dict__}")
    except Exception as e:
        await db.rollback()
        raise e
    return record


async def delete_record(db: AsyncSession, model, condition):
    try:
        record = (await db.execute(select(model).filter_by(**condition))).scalar()
        if record is None:
            return False
        await db.delete(record)
        await db.commit()
        # logger.info(f"{record.__tablename__}: {record.__dict__}")
        return True
    except Exception as e:
        await db.rollback()
        raise e


async def update_record(db: AsyncSession, model, condition, update_value):
    try:
        record = (await db.execute(select(model).filter_by(**condition))).scalar()
        if record is None:
            return await insert_record(db, model(**{**condition, **update_value}))

        for key, value in update_value.items():
            setattr(record, key, value)
        await db.commit()
        await db.refresh(record)
        # logger.info(
        #     f"update {model.__tablename__} where {condition} set {update_value}"
        # )
        return record
    except Exception as e:
        await db.rollback()
        raise e


def db_persist(func):
    async def persist(db: AsyncSession, record, *args, **kwargs):
        await func(db, record, *args, **kwargs)
        try:
            await db.commit()
            # logger.info("success calling db func: " + func.__name__)
            return True
        except SQLAlchemyError as e:
            # logger.error(e.args)
            await db.rollback()
            raise e
            # return False

    return persist


@db_persist
async def upsert(db: AsyncSession, record):
    # logger.info(f"{record.__tablename__}: {record.__dict__}")
    return await db.merge(record)
