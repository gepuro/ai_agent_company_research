from app.util.geocoding import GeocodingAPI
from app.db import models
from app.db import session
from app.db.crud import common
import asyncio
from app.util import domain


async def load_houjin_bangou():
    geocoding_api = GeocodingAPI()

    with open("data/corporate_site.csv") as f:
        for line in f:
            record = line.split(",")
            corporate_number = record[0]
            url = record[1]
            domain_value = domain.get_domain_from_url(url)

            if url.find("http") == -1:
                continue

            model = models.CorporateSite(
                corporate_number=corporate_number,
                url=url,
                domain=domain_value,
            ).__dict__
            model.__delitem__("_sa_instance_state")

            async with session.SessionLocal() as db:
                await common.update_record(
                    db,
                    models.CorporateSite,
                    {"corporate_number": corporate_number},
                    model,
                )


if __name__ == "__main__":
    asyncio.run(load_houjin_bangou())
