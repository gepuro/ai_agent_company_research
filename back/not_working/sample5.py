from google import genai
from google.genai import types
import base64


def generate():
    client = genai.Client(
        vertexai=True, project="ai-agent-cr-20241229", location="us-central1"
    )

    # model = "gemini-2.0-flash-exp"
    model = "gemini-1.5-flash-002"

    contents = ["Pythonを学ぶコンテンツを検討してください"]
    tools = [types.Tool(google_search=types.GoogleSearch())]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_LOW_AND_ABOVE",
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_LOW_AND_ABOVE"
            ),
        ],
        tools=tools,
        # response_mime_type="application/json",
        # response_schema={
        #     "type": "OBJECT",
        #     "properties": {"response": {"type": "STRING"}},
        # },
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        # contents="How does AI work?",
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content.parts:
            continue
        print(chunk.text, end="")


generate()
