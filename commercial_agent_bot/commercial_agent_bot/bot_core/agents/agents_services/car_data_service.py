import uuid
from typing import Dict, Any, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class CarDataService:
    def __init__(self, tracking_id: uuid.UUID, csv_data_path: str):
        self.tracking_id = tracking_id
        self.csv_data_path = csv_data_path
        self.car_data: Optional[pd.DataFrame] = self._load_car_data()
    
    def _load_car_data(self) -> Optional[pd.DataFrame]:
        try:
            df = pd.read_csv(self.csv_data_path)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            df['km'] = pd.to_numeric(df['km'], errors='coerce')
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            for col in ['bluetooth', 'car_play']:
                if col in df.columns:
                    df[col] = df[col].fillna('No').astype(str)
            logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Car data loaded successfully. Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"[{self.__class__.__name__} - {self.tracking_id}] Error loading car data CSV: {e}")
            return None

    def filter_cars(self, preferences: Dict[str, Any]) -> pd.DataFrame:
        if self.car_data is None:
            logger.warning(f"[{self.__class__.__name__} - {self.tracking_id}] Attempted to filter cars, but car_data is None.")
            return pd.DataFrame()

        filtered_df = self.car_data.copy()
        if 'brand' in preferences and preferences['brand']:
            filtered_df = filtered_df[filtered_df['make'].str.contains(preferences['brand'], case=False, na=False)]
        if 'model' in preferences and preferences['model']:
            filtered_df = filtered_df[filtered_df['model'].str.contains(preferences['model'], case=False, na=False)]
        if 'year_min' in preferences and preferences['year_min']:
            try:
                filtered_df = filtered_df[filtered_df['year'] >= int(preferences['year_min'])]
            except ValueError: 
                logger.warning(f"[{self.__class__.__name__} - {self.tracking_id}] ValueError converting year_min: {preferences['year_min']}")
                pass 
        if 'year_max' in preferences and preferences['year_max']:
            try:
                filtered_df = filtered_df[filtered_df['year'] <= int(preferences['year_max'])]
            except ValueError: 
                logger.warning(f"[{self.__class__.__name__} - {self.tracking_id}] ValueError converting year_max: {preferences['year_max']}")
                pass
        if 'price_min' in preferences and preferences['price_min']:
            try:
                filtered_df = filtered_df[filtered_df['price'] >= float(preferences['price_min'])]
            except ValueError: 
                logger.warning(f"[{self.__class__.__name__} - {self.tracking_id}] ValueError converting price_min: {preferences['price_min']}")
                pass
        if 'price_max' in preferences and preferences['price_max']:
            try:
                filtered_df = filtered_df[filtered_df['price'] <= float(preferences['price_max'])]
            except ValueError: 
                logger.warning(f"[{self.__class__.__name__} - {self.tracking_id}] ValueError converting price_max: {preferences['price_max']}")
                pass
        
        features_to_check = {"bluetooth": "bluetooth", "carplay": "car_play"}
        if 'features' in preferences:
            for feature in preferences['features']:
                if feature.lower() in features_to_check:
                    csv_col = features_to_check[feature.lower()]
                    if csv_col in filtered_df.columns:
                         filtered_df = filtered_df[filtered_df[csv_col].str.lower() == 'sí']
        
        logger.info(f"[{self.__class__.__name__} - {self.tracking_id}] Cars filtered. Input preferences: {preferences}. Output shape: {filtered_df.shape}")
        return filtered_df
