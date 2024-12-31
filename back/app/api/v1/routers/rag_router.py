import fastapi
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.rag import company_overview, philosophy, swot, sales, competitor, business, hr
from app.util import tidy_response
import asyncio

rag_router = r = APIRouter()


@r.get("/rag/company", response_class=JSONResponse)
async def rag_company():
    COMAPNY_NAME = "ソニーグループ株式会社"

    tasks = [
        asyncio.ensure_future(
            company_overview.fetch_company_overview(f"{COMAPNY_NAME} 東京")
        ),
        philosophy.fetch_company_phiolosophy(COMAPNY_NAME),
        swot.fetch_company_swot(COMAPNY_NAME),
        sales.fetch_sales(COMAPNY_NAME),
        competitor.fetch_company_competitor(COMAPNY_NAME),
        business.fetch_business(COMAPNY_NAME),
        hr.fetch_hr(COMAPNY_NAME),
    ]
    response = await asyncio.gather(*tasks)
    flattened_response = [item for sublist in response for item in sublist]
    return tidy_response.tidy_response(flattened_response)
