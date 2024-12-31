from app.util import gemini
from app.util import search
import json
import asyncio
from app.nayose import nayose
from loguru import logger


def get_value_from_output_format(output_format, name, year=None):
    for item in output_format:
        if item.get("name") == name:
            if year is not None:
                if item.get("year") == year:
                    return item.get("value")
            else:
                return item.get("value")
    return None


async def rag_with_googlesearch(search_word, output_format, prompt=""):
    search_results = await search.google(f"{search_word}")
    responses = []
    for search_result in search_results:
        response = gemini.gemini(
            contents=f"""
            {prompt}

            Webサイト: ```
            {search_result["markdown"]}
            ```

            出力フォーマット(JSON): ```
            {output_format}
            ```
            """
        )
        try:
            # strict=Falseでエラーを無視

            response_dict = json.loads(
                response.candidates[0].content.parts[0].text, strict=False
            )["response"]

            if isinstance(response_dict, str):
                response_dict = json.loads(response_dict, strict=False)

            corporate_number = await nayose.identify_corporate_number(
                company_name=get_value_from_output_format(response_dict, "会社名"),
                address=get_value_from_output_format(response_dict, "本社所在地"),
                url=search_result.get("link"),
            )

            data = {
                "response": response_dict,
                "source": search_result["link"],
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

    with open("response.json", "w") as f:
        f.write(json.dumps(responses, ensure_ascii=False, indent=4))

    return responses
