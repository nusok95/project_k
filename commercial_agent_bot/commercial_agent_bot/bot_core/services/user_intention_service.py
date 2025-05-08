

from django.conf import settings
from bot_core.data_models import UserIntentionResponse
from bot_core.prompts.user_intention_prompts import UserIntentionPrompts
from bot_core.services.openai_service import OpenAIService
from bot_core.services.prompt_builder_service import PromptBuilderService


class UserIntentionService:
    def __init__(self, customer_message: str):
        self.customer_message = customer_message
        self.openai_service = OpenAIService(api_key=settings.OPENAI_API_KEY)
        self.prompt_builder = PromptBuilderService()

    def build_context(self) -> str:
        return UserIntentionPrompts.CONTEXT_DUMP.format(
            customer_message=self.customer_message,
            intent_types=UserIntentionPrompts.INTENT_TYPES,
            json_example=UserIntentionPrompts.example_json_structure
            )

    def get_user_intention(self) -> UserIntentionResponse:
        prompt = self.prompt_builder.create_prompt(
            goal=UserIntentionPrompts.GOAL,
            return_format=UserIntentionPrompts.RETURN_FORMAT,
            warnings=UserIntentionPrompts.WARNINGS,
            context_dump=self.build_context()
        )
        response = self.openai_service.send_prompt(prompt.to_str())

        return UserIntentionResponse.model_validate_json(response)
