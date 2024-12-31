from app.util.geocoding import GeocodingAPI
from app.db import models
from app.db import session
from app.db.crud import common
import asyncio


async def load_houjin_bangou():
    geocoding_api = GeocodingAPI()

    with open("data/00_zenkoku_all_20241227.csv") as f:
        for line in f:
            record = line.split(",")
            corporate_number = record[1]
            company_name = record[6].replace('"', "")
            concatenation_address = (record[9] + record[10] + record[11]).replace(
                '"', ""
            )
            geocoding = geocoding_api.call(concatenation_address)
            # sample: {'pref': '北海道', 'city': '釧路市', 'town': '柏木町', 'addr': '4-7', 'lat': 42.972016, 'lng': 144.392831, 'level': 3}

            model = models.HoujinBangou(
                corporate_number=corporate_number,
                company_name=company_name,
                concatenation_address=concatenation_address,
                prefecture_name=geocoding["pref"],
                city_name=geocoding["city"],
                town_name=geocoding["town"],
                address_number=geocoding["addr"],
                lat=str(geocoding["lat"]),
                lon=str(geocoding["lng"]),
                post_code="",
            ).__dict__
            model.__delitem__("_sa_instance_state")

            async with session.SessionLocal() as db:
                await common.update_record(
                    db,
                    models.HoujinBangou,
                    {"corporate_number": corporate_number},
                    model,
                )


if __name__ == "__main__":
    asyncio.run(load_houjin_bangou())
