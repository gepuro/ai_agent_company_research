import fastapi
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.rag import company_overview, philosophy, swot, sales, competitor, business, hr
from app.util import tidy_response
import asyncio
from app.db.crud import houjin_bangou
from app.db import session

company_router = r = APIRouter()


@r.get("/company/search", response_class=JSONResponse)
async def company_search(db=Depends(session.get_db), company_name: str | None = None):
    if company_name is None:
        raise HTTPException(status_code=400, detail="company_name is required")

    return await houjin_bangou.fetch_houjin_bangou_with_company_name(
        db=db, company_name=company_name
    )
