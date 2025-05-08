from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import logging

logger = logging.getLogger(__name__)

class TwilioService:
    def __init__(self, account_sid: str, auth_token: str):
        if not account_sid or not auth_token:
            raise ValueError("Twilio Account SID and Auth Token are required.")
        self.client = Client(account_sid, auth_token)
        logger.info("Twilio client initialized.")

    def send_message(self, to_number: str, from_number: str, body: str) -> str | None:
        try:
            message = self.client.messages.create(
                from_=from_number,
                body=body,
                to=to_number
            )
            logger.info(f"Message sent successfully to {to_number}. SID: {message.sid}")
            return message.sid
        except TwilioRestException as e:
            logger.error(f"Failed to send message to {to_number}: {e}")
            return None
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending message to {to_number}: {e}")
            return None
