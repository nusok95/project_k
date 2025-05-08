import logging

from message_handler.services.commercial_agent_bot_service import CommercialAgentBotService
from ..models import TwilioMessage
from .twilio_service import TwilioService

logger = logging.getLogger(__name__)

class MessageProcessingService:
    def process_and_reply(self, incoming_message: TwilioMessage, twilio_service: TwilioService, commercial_agent_bot_service: CommercialAgentBotService):
        try:
            reply_to_number = incoming_message.from_number
            reply_from_number = incoming_message.to_number
            
            original_body = incoming_message.body if incoming_message.body else "(no message body)"
            commercial_agent_bot_response = commercial_agent_bot_service.send_message(original_body)
        
            print(f"Generated reply for {reply_to_number}: '{commercial_agent_bot_response}'")

            message_sid = twilio_service.send_message(
                to_number=reply_to_number,
                from_number=reply_from_number,
                body=commercial_agent_bot_response["bot_response"]
            )

            if message_sid:
                logger.info(f"Reply sent successfully via TwilioService to {reply_to_number}, SID: {message_sid}")
            else:
                logger.warning(f"TwilioService reported failure sending reply to {reply_to_number}")

        except Exception as e:
            logger.error(f"Error during message processing or reply for message SID {incoming_message.message_sid}: {e}", exc_info=True) 