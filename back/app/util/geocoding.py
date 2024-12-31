import requests


class GeocodingAPI:
    def call(self, address: str | None):
        if address is None:
            return None

        headers = {
            "Content-Type": "application/json",
        }
        res = requests.post(
            # f"{config.GEOCODING_URL}/api/v1/address",
            "http://cr_geocoding:5050/api/v1/address",
            json={"address": address},
            headers=headers,
        )
        return res.json()
