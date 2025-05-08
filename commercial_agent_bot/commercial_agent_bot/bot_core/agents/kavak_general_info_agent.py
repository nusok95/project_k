import uuid
from typing import Dict, Any
from bs4 import BeautifulSoup
import logging
from pathlib import Path

from ..data_models import IntentDetail
from .base_agent import BaseAgent 
from ..services.prompt_builder_service import Prompt
from ..prompts.kavak_general_info_prompts import KavakGeneralInfoPrompts

logger = logging.getLogger(__name__)

class KavakGeneralInfoAgent(BaseAgent):
    HTML_CONTEXT_FILE_PATH = (Path(__file__).parent / 'agents_data' / 'kavak_landing.html').resolve()

    def __init__(self, tracking_id: uuid.UUID, customer_message: str = None):
        super().__init__(tracking_id, customer_message)
        self.customer_message = customer_message
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Initialized.")

    def _build_context_dump(self) -> str:
        try:
            with open(self.HTML_CONTEXT_FILE_PATH, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            for script_or_style in soup(["script", "style"]):
                script_or_style.decompose()
            
            text = soup.get_text(separator=' ', strip=True)
            
            return text
        except Exception as e:
            logger.error(f"[{self.__class__.__name__} - {self.tracking_id}] Error reading or parsing HTML context file '{self.HTML_CONTEXT_FILE_PATH}': {e}")
            return ""

    def handle_intent(self, intent_detail: IntentDetail) -> str:
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Handling intent: {intent_detail.type}")

        general_kavak_context = self._build_context_dump()
        
        combined_context = f"User's specific question: '{self.customer_message}'"
        if general_kavak_context:
            combined_context = f"General Information about Kavak (from internal document):\n{general_kavak_context}\n\n{combined_context}. You can use this information to answer the user's question. about Kavak garanty, satisfaction guarantee, etc, general information of payments, post bought, etc"
        
        kavak_prompt: Prompt = self.prompt_builder.create_prompt(
            goal=KavakGeneralInfoPrompts.GOAL,
            context_dump=KavakGeneralInfoPrompts.CONTEXT_DUMP.format(combined_context=combined_context),
            return_format=KavakGeneralInfoPrompts.RETURN_FORMAT,
            warnings=KavakGeneralInfoPrompts.WARNINGS
          )

        prompt_string = kavak_prompt.to_str()
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Sending prompt to LLM: \n{prompt_string}")
        return self.call_llm(prompt_string)

    def call_llm(self, prompt: str) -> str:
        return self.openai_service.send_prompt(prompt=prompt)