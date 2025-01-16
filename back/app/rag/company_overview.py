from app.rag import rag
from app.db import session
from pydantic import BaseModel

OUTPUT_FORMAT = """
[
    {"name": "会社名", "value": ""},
    {"name": "代表者", "value": ""}
    {"name": "特色", "value": ""},
    {"name": "電話番号", "value": ""},
    {"name": "メールアドレス", "value": ""},
    {"name": "本社所在地", "value": ""},
    {"name": "設立年", "value": ""},
    {"name": "事業概要", "value": ""}
    {"name": "売上高", "year": "2024", "value": ""},
    {"name": "売上高", "year": "2023", "value": ""},
    {"name": "売上高", "year": "2022", "value": ""},
    {"name": "従業員数", "year": "2024", "value": ""},
    {"name": "従業員数", "year": "2023", "value": ""},
    {"name": "従業員数", "year": "2022", "value": ""},
    {"name": "店舗数", "year": "2024", "value": ""},
    {"name": "店舗数", "year": "2023", "value": ""},
    {"name": "店舗数", "year": "2022", "value": ""},
    {"name": "事業所数", "year": "2024", "value": ""},
    {"name": "事業所数", "year": "2023", "value": ""},
    {"name": "事業所数", "year": "2022", "value": ""},
    {"name": "工場数", "year": "2024", "value": ""},
    {"name": "工場数", "year": "2023", "value": ""},
    {"name": "工場数", "year": "2022", "value": ""},
    {"name": "営業利益", "year": "2024", "value": ""},
    {"name": "営業利益", "year": "2023", "value": ""},
    {"name": "営業利益", "year": "2022", "value": ""},
    {"name": "資本金", "year": "2024", "value": ""},
    {"name": "資本金", "year": "2023", "value": ""},
    {"name": "資本金", "year": "2022", "value": ""},
    {"name": "企業の沿革", "value": ""},
    {"name": "理念", "value": ""},
]
"""


# class Sales(BaseModel):
#     year: str
#     value: str


# class Employees(BaseModel):
#     year: str
#     value: str


# class Stores(BaseModel):
#     year: str
#     value: str


# class Offices(BaseModel):
#     year: str
#     value: str


# class Factories(BaseModel):
#     year: str
#     value: str


# class NetProfit(BaseModel):
#     year: str
#     value: str


# class Capital(BaseModel):
#     year: str
#     value: str


# class CompanyHistory(BaseModel):
#     year: str
#     value: str


# class CompanyOverview(BaseModel):
#     company_name: str  # 会社名
#     representatives: str  # 代表者
#     features: str  # 特色
#     phone_number: str  # 電話番号
#     email: str  # メールアドレス
#     headquarters_location: str  # 本社所在地
#     establishment_year: str  # 設立年
#     business_overview: str  # 事業概要
#     sales: list[Sales]  # 売上高
#     employees: list[Employees]  # 従業員数
#     stores: list[Stores]  # 店舗数
#     offices: list[Offices]  # 事業所数
#     factories: list[Factories]  # 工場数
#     net_profit: list[NetProfit]  # 営業利益
#     capital: list[Capital]  # 資本金
#     company_history: str  # 企業の沿革


async def fetch_company_overview(COMAPNY_NAME):
    db = session.SessionLocal()
    try:
        db = session.SessionLocal()
        response = await rag.rag_with_googlesearch(
            db,
            f"{COMAPNY_NAME} 会社概要",
            output_format=OUTPUT_FORMAT,
            prompt=f"{COMAPNY_NAME}の事業内容を調査してください。",
            # response_schema=CompanyOverview,
        )
        await db.close()
        return response
    except Exception as e:
        await db.close()
        return []
