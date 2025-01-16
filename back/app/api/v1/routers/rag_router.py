import fastapi
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.rag import (
    company_overview,
    philosophy,
    swot,
    sales,
    competitor,
    business,
    hr,
    employee,
    any_search,
)
from app.util import tidy_response, gemini
import asyncio
from app.db.crud import houjin_bangou, cache
from app.db import session
from loguru import logger
import json

rag_router = r = APIRouter()

sample = {
    "ソニーグループ": {
        "name": {
            "value": "ソニーグループ株式会社",
            "source": "https://www.sony.com/ja/SonyInfo/Jobs/newgrads/",
        },
        "representatives": {
            "value": ["会長 CEO　吉田 憲一郎", "十時裕樹", "吉田憲一郎"],
            "source": "https://www.sony.com/ja/SonyInfo/Jobs/newgrads/",
        },
        "features": {
            "value": "エレクトロニクス、エンタテインメント、金融など幅広い事業を展開するグローバル企業",
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
        },
        "phone_number": {
            "value": "03-6748-1212",
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/data/",
        },
        "email": {
            "value": "問い合わせフォームによる対応",
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/data/",
        },
        "headquarters_location": {
            "value": "東京都港区港南1-7-1",
            "source": "https://www.sony.com/ja/SonyInfo/Jobs/newgrads/",
        },
        "establishment_year": {
            "value": "1946年",
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
        },
        "business_activities": {
            "value": "ゲーム、音楽、映画、金融、エレクトロニクスなど",
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
        },
        "sales": {
            "2024": {
                "value": "13兆207億円",
                "source": "https://www3.nhk.or.jp/news/html/20240514/k10014449021000.html",
            },
            "2023": {
                "value": "8,900,000百万",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2022": {
                "value": "8,500,000百万",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
        },
        "employees": {
            "2024": {
                "value": "",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2023": {
                "value": "110,000",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2022": {
                "value": "110,000",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
        },
        "offices": {
            "2024": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
            "2023": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
            "2022": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
        },
        "factories": {
            "2024": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
            "2023": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
            "2022": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
        },
        "stores": {
            "2024": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
            "2023": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
            "2022": {
                "value": "非公開",
                "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
            },
        },
        "net_profit": {
            "2024": {
                "value": "",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2023": {
                "value": "1,000,000百万",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2022": {
                "value": "1,000,000百万",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
        },
        "capital": {
            "2024": {
                "value": "",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2023": {
                "value": "700,000百万",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
            "2022": {
                "value": "700,000百万",
                "source": "https://www.sony.com/ja/SonyInfo/IR/library/report/index.html",
            },
        },
        "company_history": {
            "value": "1946年創業。戦後日本の復興に貢献し、その後エレクトロニクス業界をリードする企業に成長。",
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
        },
        "philosophy": {
            "value": "ソニーグループは、創造とテクノロジーを通じて、世界の人々に感動を与えることを目指しています。",
            "source": "https://www.sony.com/ja/SonyInfo/csr/vision/",
        },
        "strengths": {
            "value": [
                "グローバルブランド力、多様な製品群、高い技術力、豊富な資金力",
                "圧倒的なブランド力、幅広い事業ポートフォリオ、高い技術力、グローバル展開力",
            ],
            "source": "https://semi-journal.jp/career/company/sony.html",
        },
        "weaknesses": {
            "value": [
                "一部事業の収益性低迷、円高による影響、競争激化、イノベーションのスピード",
                "一部事業の収益性低迷、イノベーションのスピード感、組織の複雑さ",
            ],
            "source": "https://semi-journal.jp/career/company/sony.html",
        },
        "opportunities": {
            "value": [
                "AI、IoT、メタバースなどの新技術活用、サステナビリティへの取り組み、新興市場の開拓、M&Aによる事業拡大",
                "AI、IoT、メタバースなどの新技術活用、サステナビリティへの関心の高まり、新興市場の開拓",
            ],
            "source": "https://semi-journal.jp/career/company/sony.html",
        },
        "threats": {
            "value": [
                "米中貿易摩擦、半導体不足、原材料価格高騰、他企業との競争激化、地政学的リスク",
                "競争激化、円高、半導体不足、サプライチェーンリスク、地政学的リスク",
            ],
            "source": "https://semi-journal.jp/career/company/sony.html",
        },
        "competitors": {
            "value": [
                "オムニビジョン",
                "パナソニック",
                "サムスン電子",
                "パナソニックホールディングス株式会社",
                "三菱電機株式会社",
                "日立製作所",
            ],
            "source": "https://www.onecareer.jp/articles/1136",
        },
        "businesses": {
            "value": ["ゲーム事業", "音楽事業", "映像事業"],
            "source": "https://www.sony.com/ja/SonyInfo/CorporateInfo/",
        },
        "human_resources": {
            "ideal": {
                "value": "ソニーグループは、創造性、好奇心、そして何事にも挑戦しようとする意欲を高く評価しています。変化に柔軟に対応し、多様な文化やバックグラウンドを持つ人々と協力して仕事を進められる方を求めています。また、グローバルな視点と高い倫理観を持つことも重要視しています。具体的には、課題解決能力、コミュニケーション能力、チームワーク力、そして高い学習意欲などが求められます。",
                "source": "https://www.sony.com/ja/SonyInfo/Jobs/newgrads/",
            },
            "skills": {
                "value": [
                    "グローバルな視点・コミュニケーション能力",
                    "創造性と革新力",
                    "高い専門性・技術力",
                    "革新的な発想力・創造力",
                    "問題解決能力",
                    "課題解決能力",
                    "チームワーク力",
                    "コミュニケーション能力",
                ],
                "source": "https://www.sony.com/ja/SonyInfo/Jobs/newgrads/",
            },
        },
        "corporate_number": "5010401067252",
    },
    "ソニー": {
        "name": {
            "value": "ソニー株式会社",
            "source": "https://www.sony.co.jp/corporate/mission-vision/",
        },
        "representatives": {
            "value": ["不明"],
            "source": "https://www.sony.co.jp/corporate/mission-vision/",
        },
        "features": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        "phone_number": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        "email": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        "headquarters_location": {
            "value": "不明",
            "source": "https://www.sony.co.jp/corporate/mission-vision/",
        },
        "establishment_year": {
            "value": "",
            "source": "https://www.sony.co.jp/corporate/",
        },
        "business_activities": {
            "value": "",
            "source": "https://www.sony.co.jp/corporate/",
        },
        "sales": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "employees": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "offices": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "factories": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "stores": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "net_profit": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "capital": {
            "2024": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2023": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
            "2022": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        },
        "company_history": {"value": "", "source": "https://www.sony.co.jp/corporate/"},
        "philosophy": {
            "value": "テクノロジーの力で未来のエンタテインメントをクリエイターと共創する。世界中の人に感動を提供し続ける。",
            "source": "https://www.sony.co.jp/corporate/mission-vision/",
        },
        "strengths": {"value": [], "source": None},
        "weaknesses": {"value": [], "source": None},
        "opportunities": {"value": [], "source": None},
        "threats": {"value": [], "source": None},
        "competitors": {"value": [], "source": None},
        "businesses": {"value": [], "source": None},
        "human_resources": {
            "ideal": {"value": None, "source": None},
            "skills": {"value": [], "source": None},
        },
        "corporate_number": None,
    },
    "ソニー企業": {
        "name": {
            "value": "ソニー企業株式会社",
            "source": "https://www.sonykigyo.jp/company/philosophy2.html",
        },
        "representatives": {"value": [], "source": None},
        "features": {"value": None, "source": None},
        "phone_number": {"value": None, "source": None},
        "email": {"value": None, "source": None},
        "headquarters_location": {
            "value": "",
            "source": "https://www.sonykigyo.jp/company/philosophy2.html",
        },
        "establishment_year": {"value": None, "source": None},
        "business_activities": {"value": None, "source": None},
        "sales": {},
        "employees": {},
        "offices": {},
        "factories": {},
        "stores": {},
        "net_profit": {},
        "capital": {},
        "company_history": {"value": None, "source": None},
        "philosophy": {
            "value": "私たちのミッションは「場」を使った新しいブランドコミュニケーションによりお客様に感動をお届けすることです。このミッションを実現させるためのコンセプトは「3IN」。\n\n* Inviting（招く・誘う・誘惑する）\n* Inspiring（刺激・感動・鼓舞する）\n* Interweaving（織り込む・組み合わす・織り成す）\n\n自由でオープンであり、余白・余地・余裕があること。好奇心を刺激する、未来、発想、遊び、技術で人々を鼓舞すること。モノ・コト・ヒト、複数の価値観が組み合わされていること。\n\n私たちはこれらの考え方を日々の仕事のスタンスや、人々との関わり方に組み入れることで、都市や社会、そして未来を面白くする会社であり続けます。",
            "source": "https://www.sonykigyo.jp/company/philosophy2.html",
        },
        "strengths": {"value": [], "source": None},
        "weaknesses": {"value": [], "source": None},
        "opportunities": {"value": [], "source": None},
        "threats": {"value": [], "source": None},
        "competitors": {"value": [], "source": None},
        "businesses": {"value": [], "source": None},
        "human_resources": {
            "ideal": {"value": None, "source": None},
            "skills": {"value": [], "source": None},
        },
        "corporate_number": None,
    },
}


@r.get("/rag/company", response_class=JSONResponse)
async def rag_company(db=Depends(session.get_db), corporate_number: str | None = None):
    if corporate_number is None:
        return sample

    company = await houjin_bangou.fetch_houjin_bangou_with_condition(
        db=db, corporate_number=corporate_number
    )

    tidied_response = await cache.fetch_cache_company(
        db=db, corporate_number=corporate_number
    )
    logger.info(tidied_response)
    if tidied_response:
        return json.loads(tidied_response[0]["response"])

    COMAPNY_NAME = company[0].get("company_name")
    AREA = company[0].get("prefecture_name")

    defined_tasks = [
        company_overview.fetch_company_overview(f"{COMAPNY_NAME} {AREA}"),
        philosophy.fetch_company_phiolosophy(COMAPNY_NAME),
        swot.fetch_company_swot(COMAPNY_NAME),
        sales.fetch_sales(COMAPNY_NAME),
        competitor.fetch_company_competitor(COMAPNY_NAME),
        business.fetch_business(COMAPNY_NAME),
        hr.fetch_hr(COMAPNY_NAME),
        employee.fetch_employee(COMAPNY_NAME),
    ]
    defined_tasks_response = await asyncio.gather(*defined_tasks)
    flattened_response = [
        item for sublist in defined_tasks_response for item in sublist
    ]
    tidied_response = tidy_response.tidy_response(flattened_response)
    # tidied_response = tidy_response.tidy_with_gemini(tidied_response)

    output_format = """
    [
        {"search_word": ""},
        {"search_word": ""},
        {"search_word": ""},
    ]
    """

    target_key = [
        key
        for key in tidied_response
        if tidied_response[key]["name"]["value"] == COMAPNY_NAME
    ][0]

    try:
        response = await gemini.gemini(
            db=db,
            contents=f"""
            {COMAPNY_NAME}の会社情報を調査しました。

            調査したデータ: ```
            {json.dumps(tidied_response[target_key], ensure_ascii=False)}
            ```

            欠損データを埋めるために、追加で調査をしたいです。
            調査に必要な検索ワードを作成してください。

            出力フォーマット(JSON): ```
            {output_format}
            ```
            """,
        )
        # search_words = json.loads(
        #     json.loads(response.candidates[0].content.parts[0].text)["response"]
        # )
        search_words = json.loads(response)

    except Exception as e:
        logger.error(e)
        search_words = []

    agent_tasks = [
        any_search.fetch_any_data(COMAPNY_NAME, search_word["search_word"], top_n=1)
        for search_word in search_words[0:10]
        # for search_word in search_words[0:1]
    ]
    agent_tasks_response = await asyncio.gather(*agent_tasks)
    total_response = defined_tasks_response + agent_tasks_response
    flattened_response = [item for sublist in total_response for item in sublist]

    tidied_response = tidy_response.tidy_response(flattened_response)

    try:
        tidied_response = tidy_response.tidy_with_gemini(tidied_response)
    except:
        pass

    # import time
    # time.sleep(5)

    # エラーがおきたときは、キャッシュに保存しない
    if tidied_response:
        await cache.add_cache_company(
            db=db,
            corporate_number=corporate_number,
            response=json.dumps(tidied_response, ensure_ascii=False),
        )

    return tidied_response
