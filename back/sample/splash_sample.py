import requests
import httpx
import asyncio


async def main():
    async with httpx.AsyncClient() as client:
        res = await client.get(
            "http://splash:8050/render.html",
            params={"url": "https://gepuro.net", "wait": 0.5},
        )
        print(res.text)


if __name__ == "__main__":
    asyncio.run(main())

# url = "https://gepuro.net"
# res = requests.get("http://splash:8050/render.html", params={"url": url, "wait": 0.5})
# print(res.content.decode("utf-8"))
