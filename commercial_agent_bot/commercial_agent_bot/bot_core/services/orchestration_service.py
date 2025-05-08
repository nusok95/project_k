import uuid
from typing import List, Optional, Any
import logging

from ..data_models import UserIntentionResponse
from ..agents.base_agent import BaseAgent
from ..agents.car_recommendation_agent import CarRecommendationAgent
from ..agents.kavak_general_info_agent import KavakGeneralInfoAgent
from ..agents.sales_agent import SalesAgent
from ..agents.financing_agent import FinancingAgent
from ..agents.greeting_agent import GreetingAgent

logger = logging.getLogger(__name__)

class OrchestrationService:
    def __init__(self, user_intention: UserIntentionResponse, customer_message: str = None):
        self.user_intention = user_intention
        self.customer_message = customer_message
        logger.info(f"[{self.__class__.__name__}] Initialized.")

    def _get_agent_for_intent(self, intent_type: str, tracking_id: uuid.UUID) -> Optional[BaseAgent]:
        if intent_type == "car_recommendation":
            return CarRecommendationAgent(tracking_id=tracking_id, customer_message=self.customer_message)
        elif intent_type == "financing_info":
           return FinancingAgent(tracking_id=tracking_id, customer_message=self.customer_message)
        elif intent_type == "greetings":
            return GreetingAgent(tracking_id=tracking_id, customer_message=self.customer_message)
        elif intent_type == "general_info":
             return KavakGeneralInfoAgent(tracking_id=tracking_id, customer_message=self.customer_message)
        elif intent_type == "sales_agent":
            return SalesAgent(tracking_id=tracking_id, customer_message=self.customer_message)
        else:
            logger.warning(f"Warning: No agent found for intent type '{intent_type}'")
            return None
        
    def synthesize_responses(self, responses: List[str], tracking_id: uuid.UUID) -> str:
        return "\n---\n".join(responses)

    def process_user_message(self, tracking_id: uuid.UUID) -> str:
        logger.info(f"[{self.__class__.__name__} - {tracking_id}] Processing: '{self.customer_message}'")

        agent_responses = []
        
        for intent_detail in self.user_intention.intents:
            agent = self._get_agent_for_intent(intent_detail.type, tracking_id)
            if agent:
                try:
                    response = agent.handle_intent(intent_detail)
                    agent_responses.append(response)
                except Exception as e:
                    logger.error(f"Error in agent {intent_detail.type}: {e}")
                    agent_responses.append(f"Sorry, there was an issue handling your {intent_detail.type} request.")
            else:
                agent_responses.append(f"I can't handle '{intent_detail.type}' requests yet.")

        if len(agent_responses) == 1:
            return agent_responses[0]
        else:
            return self.synthesize_responses(agent_responses, tracking_id) 