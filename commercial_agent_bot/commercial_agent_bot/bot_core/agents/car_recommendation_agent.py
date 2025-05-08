from pathlib import Path
import uuid
from typing import Dict, Any, List, Optional
import pandas as pd
import logging

from ..services.prompt_builder_service import PromptBuilderService

from .base_agent import BaseAgent
from ..data_models import IntentDetail
from .agents_services.car_data_service import CarDataService
from ..prompts.car_recommendation_prompts import CarRecommendationPrompts

logger = logging.getLogger(__name__)

class CarRecommendationAgent(BaseAgent):
    CSV_DATA_PATH = (Path(__file__).parent / 'agents_data' / 'cars_recommendation.csv').resolve()

    def __init__(self, tracking_id: uuid.UUID, customer_message: str = None):
        super().__init__(tracking_id, customer_message)
        self.customer_message = customer_message
        self.car_data_service = CarDataService(tracking_id, self.CSV_DATA_PATH)
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Initialized.")
        
    def _format_car_details_for_prompt(self, cars_df: pd.DataFrame, max_cars: int = 3) -> str:
        selected_cars = cars_df.head(max_cars)
        details_list = []
        for index, car in selected_cars.iterrows():
            detail = (
                f"Opción {index + 1}: {car.get('make', 'N/A')} {car.get('model', 'N/A')} {int(car.get('year', 0)) if pd.notna(car.get('year')) else 'N/A'}. "
                f"Precio: ${car.get('price', 0):,.0f} MXN, Kilometraje: {car.get('km', 0):,.0f} km. "
                f"Versión: {car.get('version', 'N/A')}. "
                f"Bluetooth: {car.get('bluetooth', 'No')}. CarPlay: {car.get('car_play', 'No')}. "
                f"Stock ID: {car.get('stock_id', 'N/A')}."
            )
            details_list.append(detail)
        return "\n".join(details_list)

    def handle_intent(self, intent_detail: IntentDetail) -> str:
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Handling intent: {intent_detail.type}")

        preferences = intent_detail.entities
        
        filtered_cars_dataframe = self.car_data_service.filter_cars(preferences)
        
        car_details_for_prompt = self._format_car_details_for_prompt(filtered_cars_dataframe, max_cars=5)
        
        recommendation_prompt_text = self.prompt_builder.create_prompt(
            goal=CarRecommendationPrompts.GOAL,
            context_dump=self._build_context_dump(preferences, car_details_for_prompt),
            return_format=CarRecommendationPrompts.RETURN_FORMAT,
            warnings=CarRecommendationPrompts.WARNINGS
        )
        prompt_string = recommendation_prompt_text.to_str()

        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Sending prompt to LLM: \n{prompt_string}")

        return self.call_llm(prompt_string)

        
    def _build_context_dump(self, preferences: Dict[str, Any], car_details_for_prompt: str) -> str:
        preferences_str = preferences if preferences else 'generales, basadas en el mensaje'
        return CarRecommendationPrompts.CONTEXT_DUMP.format(
            preferences=preferences_str,
            customer_message=self.customer_message,
            car_details_for_prompt=car_details_for_prompt
        )
    
    def call_llm(self, prompt: str) -> str:
        return self.openai_service.send_prompt(prompt=prompt)
