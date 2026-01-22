"""
Transformer - Clase para transformar y formatear datos de ratings
"""
from datetime import datetime
from typing import Dict, Optional, List
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class Transformer:
    """Transforma los datos de ratings al formato requerido"""
    
    @staticmethod
    def generate_timestamp() -> str:
        """
        Genera un timestamp en formato ISO 8601
        
        Returns:
            Timestamp como string
        """
        return datetime.now().isoformat()
    
    @staticmethod
    def transform_ratings(ratings: Dict[str, Optional[float]], timestamp: Optional[str] = None) -> Dict[str, any]:
        """
        Transforma los datos de ratings al formato requerido:
        - Columnas en mayúsculas sin espacios
        - Rating como float (preserva decimales)
        - Timestamp agregado
        
        Args:
            ratings: Diccionario con ratings por canal
            timestamp: Timestamp opcional (se genera si no se proporciona)
            
        Returns:
            Diccionario transformado
        """
        if timestamp is None:
            timestamp = Transformer.generate_timestamp()
            
        transformed = {'TIMESTAMP': timestamp}
        
        for channel, rating in ratings.items():
            # Mantener rating como float (0.0 si es None)
            rating_float = float(rating) if rating is not None else 0.0
            transformed[channel] = rating_float
            
        logger.info(f"Datos transformados: {transformed}")
        return transformed
    
    @staticmethod
    def to_dataframe(transformed_data: Dict[str, any]) -> pd.DataFrame:
        """
        Convierte los datos transformados a DataFrame
        
        Args:
            transformed_data: Datos transformados
            
        Returns:
            DataFrame de pandas
        """
        return pd.DataFrame([transformed_data])
    
    @staticmethod
    def append_to_csv(data: Dict[str, any], filepath: str):
        """
        Agrega los datos al archivo CSV (crea el archivo si no existe)
        
        Args:
            data: Datos transformados
            filepath: Ruta del archivo CSV
        """
        df = Transformer.to_dataframe(data)
        
        try:
            # Intentar leer el CSV existente
            existing_df = pd.read_csv(filepath)
            # Concatenar con los nuevos datos
            combined_df = pd.concat([existing_df, df], ignore_index=True)
            combined_df.to_csv(filepath, index=False)
            logger.info(f"Datos agregados a {filepath}")
        except FileNotFoundError:
            # Si el archivo no existe, crearlo
            df.to_csv(filepath, index=False)
            logger.info(f"Archivo CSV creado: {filepath}")
        except Exception as e:
            logger.error(f"Error al guardar CSV: {str(e)}")
            raise
