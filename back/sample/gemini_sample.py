# これは動く
import vertexai

PROJECT_ID = "ai-agent-cr-20241229"  # @param {type:"string"}
REGION = "asia-northeast1"  # @param {type:"string"}

vertexai.init(project=PROJECT_ID, location=REGION)

from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

model = GenerativeModel("gemini-1.5-flash-002")

generation_config = GenerationConfig(
    temperature=0,
    top_p=0.95,
    candidate_count=1,
    max_output_tokens=8192,
)

response = model.generate_content(
    "Pythonを学ぶコンテンツを検討してください",
    generation_config=generation_config,
)

print(response.text)
