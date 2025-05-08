from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import parse_qs
from .serializers import TwilioMessageSerializer
from .services.twilio_service import TwilioService
from message_handler.services.commercial_agent_bot_service import CommercialAgentBotService
from .services.message_processing_service import MessageProcessingService
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class TwilioWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json' and 'postData' in request.data and 'text' in request.data['postData']:
            raw_data = request.data['postData']['text']
            parsed_data_list = parse_qs(raw_data)
            parsed_data = {k: v[0] for k, v in parsed_data_list.items()}
        elif request.content_type == 'application/x-www-form-urlencoded':
            parsed_data = request.data.dict()
        else:
             return Response({"error": f"Unsupported content type: {request.content_type}"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        mapped_data = {
            'message_sid': parsed_data.get('SmsMessageSid'),
            'account_sid': parsed_data.get('AccountSid'),
            'from_number': parsed_data.get('From'),
            'to_number': parsed_data.get('To'),
            'body': parsed_data.get('Body'),
            'status': parsed_data.get('SmsStatus'),
            'profile_name': parsed_data.get('ProfileName'),
        }
        mapped_data = {k: v for k, v in mapped_data.items() if v is not None}

        serializer = TwilioMessageSerializer(data=mapped_data)

        if serializer.is_valid():
            saved_message = serializer.save()
            logger.info(f"Incoming message saved: SID {saved_message.message_sid}")

            try:
                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                
                twilio_service = TwilioService(account_sid, auth_token)
                commercial_agent_bot_service = CommercialAgentBotService(commercial_agent_bot_url=settings.KAVAK_COMMERCIAL_AGENT_BOT)
                processing_service = MessageProcessingService()
                
                processing_service.process_and_reply(saved_message, twilio_service,commercial_agent_bot_service)
                
            except AttributeError:
                 logger.error("TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not found in Django settings. Cannot initialize TwilioService.")
            except Exception as e:
                logger.error(f"Error initializing services or calling message processing: {e}", exc_info=True)
            
            return Response("{success: true}", content_type='text/json', status=status.HTTP_200_OK)
        else:
            logger.error(f"Serializer Errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
