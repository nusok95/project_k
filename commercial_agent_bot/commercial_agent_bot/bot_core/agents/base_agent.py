from abc import ABC, abstractmethod
from typing import Any
import uuid
from django.conf import settings
import logging

from ..services.prompt_builder_service import PromptBuilderService

from ..services.openai_service import OpenAIService

from ..data_models import IntentDetail

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    def __init__(self, customer_message: str, tracking_id: uuid.UUID):
        self.tracking_id = tracking_id
        self.customer_message = customer_message
        self.openai_service = OpenAIService(api_key=settings.OPENAI_API_KEY)
        self.prompt_builder = PromptBuilderService()

    @abstractmethod
    def handle_intent(self, intent_detail: IntentDetail) -> str:
        pass

    @abstractmethod
    def call_llm(self, prompt: str) -> str:
        pass