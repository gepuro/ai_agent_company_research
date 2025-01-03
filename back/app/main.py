from app.util import gemini
from app.util import search
import json
import asyncio
from app.nayose import nayose
from loguru import logger
from app.rag import company_overview, philosophy, swot, sales, competitor, business, hr
from app.util import search
import asyncio
import traceback
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.routers.rag_router import rag_router
from app.api.v1.routers.company_router import company_router
from app.core import config

app = FastAPI(docs_url="/api/docs", openapi_url="/api")


origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5137",
    "http://cr_front:3000",
    "http://cr_svelte:5137",
    "http://localhost:5173",  # フロントエンドのオリジン
    "http://localhost:3030",  # 必要であればバックエンド自身のオリジンも追加
    config.FRONT_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(rag_router, prefix="/api/v1", tags=["rag"])
app.include_router(company_router, prefix="/api/v1", tags=["company"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=3030, log_level="debug")


# if __name__ == "__main__":
#     COMAPNY_NAME = "ソニーグループ株式会社"
#     print(asyncio.run(company_overview.fetch_company_overview(f"{COMAPNY_NAME} 東京")))
#     print(asyncio.run(philosophy.fetch_company_phiolosophy(COMAPNY_NAME)))
#     print(asyncio.run(swot.fetch_company_swot(COMAPNY_NAME)))
#     print(asyncio.run(sales.fetch_sales(COMAPNY_NAME)))
#     print(asyncio.run(competitor.fetch_company_competitor(COMAPNY_NAME)))
#     print(asyncio.run(business.fetch_business(COMAPNY_NAME)))
#     print(asyncio.run(hr.fetch_hr(COMAPNY_NAME)))
#     print(asyncio.run(search.duckduckgo_news(COMAPNY_NAME)))
