import requests
from app.core import config


class GeocodingAPI:
    def call(self, address: str | None):
        if address is None:
            return None

        headers = {
            "Content-Type": "application/json",
        }
        res = requests.post(
            # f"{config.GEOCODING_URL}/api/v1/address",
            # "http://cr_geocoding:5050/api/v1/address",
            config.GEOCODING_URL,
            json={"address": address},
            headers=headers,
        )
        return res.json()
