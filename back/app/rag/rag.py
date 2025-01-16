from app.util import gemini
from app.util import search
import json
from tenacity import retry, stop_after_attempt, RetryError
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.nayose import nayose
from loguru import logger
from app.db.crud import cache
import json
from tenacity import retry, stop_after_attempt, stop_after_delay
from app import rag


def get_value_from_output_format(output_format, name, year=None):
    for item in output_format:
        if item.get("name") == name:
            if year is not None:
                if item.get("year") == year:
                    return item.get("value")
            else:
                return item.get("value")
    return None


@retry(stop=(stop_after_attempt(1) | stop_after_delay(100)))
async def rag_with_googlesearch(
    db: AsyncSession, search_word, output_format, prompt="", top_n=3
):
    # キャッシュがあればそれを返す
    cache_google = await cache.fetch_cache_google(db=db, search_word=search_word)
    if cache_google:
        return json.loads(cache_google[0]["response"])

    search_results = await search.google(f"{search_word}", top_n=top_n)
    responses = []
    for search_result in search_results:
        content = search_result["markdown"]
        if len(content) == 0 or len(content) > 20000:
            # markdownが取得できない or 長すぎて結果が怪しい場合は、スニペットを利用する
            content = search_result["snippet"]

        response = await gemini.gemini(
            db=db,
            contents=f"""
            {prompt}

            Webサイト: ```
            {content}
            ```

            情報がない項目は、空文字''にしてください。
            出力フォーマット(JSON): ```
            {output_format}
            ```
            """,
        )

        try:
            # strict=Falseでエラーを無視

            # response_dict = json.loads(
            #     response.candidates[0].content.parts[0].text, strict=False
            # )["response"]
            response_dict = json.loads(response, strict=False)

            # if isinstance(response_dict, str):
            #     response_dict = json.loads(response_dict, strict=False)

            corporate_number = await nayose.identify_corporate_number(
                db,
                company_name=get_value_from_output_format(response_dict, "会社名"),
                address=get_value_from_output_format(response_dict, "本社所在地"),
                url=search_result.get("link"),
            )

            data = {
                "response": response_dict,
                "source": search_result["link"],
                "markdown_length": len(search_result["markdown"]),
                "snippet_length": len(search_result["snippet"]),
                "content_length": len(content),
                "corporate_number": corporate_number,
            }

            responses.append(data)
        except Exception as e:
            logger.debug(e)
            logger.debug(f"Error: {search_result['link']}")
            # logger.debug(response.candidates[0].content.parts[0].text)
            # logger.debug(
            #     json.loads(response.candidates[0].content.parts[0].text)["response"]
            # )
            pass

    # with open("response.json", "w") as f:
    #     f.write(json.dumps(responses, ensure_ascii=False, indent=4))

    # キャッシュを追加
    await cache.add_cache_google(
        db=db,
        search_word=search_word,
        response=json.dumps(responses, ensure_ascii=False),
    )
    return responses


def delete_nouse_content(response, names):
    for item in response:
        for record in item.get("response", []):
            if record.get("name") in names:
                record["value"] = ""
    return response
