from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from bot_core.services.user_intention_service import UserIntentionService

from .serializers import CustomerMessageRequestSerializer

from bot_core.services.orchestration_service import OrchestrationService 

logger = logging.getLogger(__name__)

class CustomerInteractionView(APIView):
    def post(self, request, *args, **kwargs):
        tracking_id_str = request.headers.get('X-Tracking-ID') 
        serializer = CustomerMessageRequestSerializer(data=request.data)
        if serializer.is_valid():
            message_content = serializer.validated_data['message_content']
            
            try:
                
                user_intention_service = UserIntentionService(customer_message=message_content)
                user_intention_response = user_intention_service.get_user_intention()
                
                orchestration_service_instance = OrchestrationService(user_intention=user_intention_response, customer_message=message_content)
                bot_response_text = orchestration_service_instance.process_user_message(
                    tracking_id=tracking_id_str
                )

                logger.info(f"Bot response text: {bot_response_text}")
                
                response_data = {
                    "status": "success",
                    "received_message": message_content,
                    "tracking_id": str("tracking_id"),
                    "bot_response": bot_response_text
                }
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error(f"Error calling OrchestrationService: {str(e)}") 
                return Response(
                    {"error_code": "BOT_PROCESSING_ERROR", "message": "An error occurred while processing your request with the bot."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {"error_code": "INVALID_REQUEST_BODY", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            ) 