import uuid
from typing import Dict, Any
import logging

from ..data_models import IntentDetail
from .base_agent import BaseAgent 
from ..services.prompt_builder_service import Prompt, PromptBuilderService
from ..prompts.sales_prompts import SalesPrompts # Added import

logger = logging.getLogger(__name__)

class SalesAgent(BaseAgent):
    def __init__(self, tracking_id: uuid.UUID, customer_message: str = None):
        super().__init__(tracking_id, customer_message)
        self.customer_message = customer_message
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Initialized.")

    def handle_intent(self, intent_detail: IntentDetail) -> str:
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Handling intent: {intent_detail.type}")
        
        kavak_prompt: Prompt = self.prompt_builder.create_prompt(
            goal=SalesPrompts.GOAL,
            context_dump=SalesPrompts.CONTEXT_DUMP.format(customer_message=self.customer_message),
            return_format=SalesPrompts.RETURN_FORMAT,
            warnings=SalesPrompts.WARNINGS
          )

        prompt_string = kavak_prompt.to_str()
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Sending prompt to LLM: \n{prompt_string}")
        return self.call_llm(prompt_string)


    def call_llm(self, prompt: str) -> str:
        return self.openai_service.send_prompt(prompt=prompt)