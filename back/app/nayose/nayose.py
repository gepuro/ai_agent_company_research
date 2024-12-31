from app.db import models, session
from app.db.crud import common, houjin_bangou, corporate_site
from app.util import domain
from app.util import geocoding
from collections import defaultdict


async def identify_corporate_number(
    company_name: str | None, address: str | None, url: str | None
) -> str:
    """
    この関数は、企業名、住所、URLから法人番号を特定する関数です。
    FIXME: どれか一つでも見つかれば、それを返すようにしていますが、精度が低い可能性があるため、修正対応が必要
    """

    match_score = defaultdict(int)

    async with session.SessionLocal() as db:

        # 企業名
        houjin_bangou_data = await houjin_bangou.fetch_houjin_bangou_with_condition(
            db, company_name=company_name
        )
        if houjin_bangou_data is not None:
            for record in houjin_bangou_data:
                corporate_number = record["corporate_number"]
                match_score[corporate_number] += 20

        # 住所
        geocoding_api = geocoding.GeocodingAPI()
        geocoding_data = geocoding_api.call(address)
        if geocoding_data is not None:
            houjin_bangou_data = await houjin_bangou.fetch_houjin_bangou_with_condition(
                db,
                prefecture_name=geocoding_data["pref"],
                city_name=geocoding_data["city"],
                town_name=geocoding_data["town"],
            )
            if houjin_bangou_data is not None:
                for record in houjin_bangou_data:
                    corporate_number = record["corporate_number"]
                    match_score[corporate_number] += 30

        # サイトURL
        corporate_site_data = await corporate_site.fetch_corporate_site(db, url=url)
        if corporate_site_data is not None:
            for record in corporate_site_data:
                corporate_number = record["corporate_number"]
                match_score[corporate_number] += 100

        # ドメイン
        domain_value = domain.get_domain_from_url(url)
        corporate_site_data = await corporate_site.fetch_corporate_site(
            db, domain=domain_value
        )
        if corporate_site_data is not None:
            for record in corporate_site_data:
                corporate_number = record["corporate_number"]
                match_score[corporate_number] += 50

        # gbizのデータを参照

        # スコアが50以上なら、法人番号を返す
        for corporate_number, score in match_score.items():
            if score >= 50:
                return corporate_number

        return None
