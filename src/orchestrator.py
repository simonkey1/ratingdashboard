"""
Orchestrator - Clase para coordinar el scraping y almacenamiento de datos
"""
import time
import logging
from pathlib import Path
from rating_scraper import RatingScraper
from transformer import Transformer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Orchestrator:
    """Orquesta el proceso de scraping, transformación y almacenamiento"""
    
    def __init__(self, csv_filepath: str = "ratings_data.csv", headless: bool = True):
        """
        Inicializa el orquestador
        
        Args:
            csv_filepath: Ruta del archivo CSV donde se guardarán los datos
            headless: Si True, ejecuta el navegador en modo headless
        """
        self.csv_filepath = csv_filepath
        self.headless = headless
        self.scraper = None
        self.transformer = Transformer()
        
    def run_single_scrape(self):
        """Ejecuta un ciclo de scraping completo"""
        logger.info("=" * 60)
        logger.info("Iniciando ciclo de scraping...")
        
        try:
            # Usar context manager para manejar el scraper
            with RatingScraper(headless=self.headless) as scraper:
                # 1. Scraping
                ratings = scraper.scrape_all_channels()
                
                # 2. Transformación
                transformed_data = self.transformer.transform_ratings(ratings)
                
                # 3. Almacenamiento
                self.transformer.append_to_csv(transformed_data, self.csv_filepath)
                
                logger.info(f"Ciclo completado exitosamente. Datos guardados en {self.csv_filepath}")
                
        except Exception as e:
            logger.error(f"Error durante el ciclo de scraping: {str(e)}")
            raise
            
    def run_continuous(self, interval_minutes: int = 30):
        """
        Ejecuta el scraping de forma continua con un intervalo específico
        
        Args:
            interval_minutes: Intervalo en minutos entre cada scraping
        """
        interval_seconds = interval_minutes * 60
        
        logger.info(f"Iniciando scraping continuo cada {interval_minutes} minutos...")
        logger.info(f"Los datos se guardarán en: {Path(self.csv_filepath).absolute()}")
        logger.info("Presiona Ctrl+C para detener")
        
        try:
            while True:
                self.run_single_scrape()
                logger.info(f"Esperando {interval_minutes} minutos hasta el próximo scraping...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            logger.info("\nScraping detenido por el usuario")
        except Exception as e:
            logger.error(f"Error fatal: {str(e)}")
            raise


if __name__ == "__main__":
    # Para testing: ejecutar cada 1 minuto
    orchestrator = Orchestrator(csv_filepath="ratings_data.csv", headless=True)
    orchestrator.run_continuous(interval_minutes=1)
