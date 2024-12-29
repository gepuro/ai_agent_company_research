import base64
import vertexai
from vertexai.preview.generative_models import (
    GenerativeModel,
    SafetySetting,
    Part,
    Tool,
)
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
from vertexai.preview.generative_models import grounding


def gemini_with_grounding(contents):
    vertexai.init(project="ai-agent-cr-20241229", location="asia-northeast1")
    tools = [
        Tool.from_google_search_retrieval(
            google_search_retrieval=grounding.GoogleSearchRetrieval()
        ),
    ]
    model = GenerativeModel(
        "gemini-1.5-flash-002",
        tools=tools,
    )

    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 1,
        "top_p": 0.95,
        "response_modalities": ["TEXT"],
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "OBJECT",
            "properties": {"response": {"type": "STRING"}},
        },
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        ),
    ]

    response = model.generate_content(
        contents=contents,
        generation_config=generation_config,
        safety_settings=safety_settings,
    )
    return response


def gemini(contents):
    model = GenerativeModel("gemini-1.5-flash-002")

    generation_config = GenerationConfig(
        temperature=0,
        top_p=0.95,
        candidate_count=1,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        response_mime_type="application/json",
        response_schema={
            "type": "OBJECT",
            "properties": {"response": {"type": "STRING"}},
        },
    )

    response = model.generate_content(
        contents=contents,
        generation_config=generation_config,
    )
    return response
    # print(response.text)
