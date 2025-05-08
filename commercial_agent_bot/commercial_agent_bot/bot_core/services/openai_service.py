from openai import OpenAI
import logging
import os

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        logger.info("OpenAI client initialized.")

    def send_prompt(self, prompt: str, model: str = "gpt-3.5-turbo", max_tokens: int = 2000) -> str | None:
        try:
            response = self.client.chat.completions.create(
              model=model,
              messages=[{"role": "user", "content": prompt}],
              max_tokens=max_tokens
            )
            logger.info(f"Prompt sent successfully to OpenAI model {model}.")

            return response.choices[0].message.content
        except Exception as e:
            error = f"An unexpected error occurred while sending prompt to OpenAI: {e}"
            logger.error(error)
            raise Exception(error)
