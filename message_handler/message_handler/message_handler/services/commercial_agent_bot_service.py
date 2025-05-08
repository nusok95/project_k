import requests
import logging

logger = logging.getLogger(__name__)

class CommercialAgentBotService:
    def __init__(self, commercial_agent_bot_url: str):
        self.commercial_agent_bot_url = commercial_agent_bot_url

    def send_message(self, customer_message: str) -> str | None:
        try:
            response = requests.post(self.commercial_agent_bot_url+"/api/customer_message/", json={
                'message_content': customer_message,
            })
            logger.info(f"Response from commercial agent bot: {response.json()}")
            return response.json()
        except Exception as e:
            logger.error(f"Error sending message to commercial agent bot: {e}")
            return None
        
