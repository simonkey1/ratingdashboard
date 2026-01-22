"""
RatingScraper - Clase para extraer ratings de TV desde Zapping
"""
from playwright.sync_api import sync_playwright, Page
from typing import Dict, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RatingScraper:
    """Scraper para obtener ratings de canales de TV chilenos desde Zapping"""
    
    BASE_URL = "https://metrics.zappingtv.com/public/rating"
    
    CHANNELS = {
        'CHV': 'chv',
        'CANAL13': '13',
        'TVM': 'tvm',
        'TVNO': 'tvno',
        'LARED': 'lared',
        'MEGA': 'mega'
    }
    
    def __init__(self, headless: bool = True):
        """
        Inicializa el scraper
        
        Args:
            headless: Si True, ejecuta el navegador en modo headless
        """
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.context = None
        
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        
    def start(self):
        """Inicia el navegador"""
        logger.info("Iniciando navegador Playwright...")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        logger.info("Navegador iniciado correctamente")
        
    def close(self):
        """Cierra el navegador"""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("Navegador cerrado")
        
    def _fetch_channel_rating(self, page: Page, channel_slug: str) -> Optional[float]:
        """
        Obtiene el rating de un canal específico
        
        Args:
            page: Página de Playwright
            channel_slug: Slug del canal (ej: 'mega', 'chv')
            
        Returns:
            Rating como float o None si hay error
        """
        url = f"{self.BASE_URL}/{channel_slug}"
        
        try:
            logger.info(f"Obteniendo rating de {channel_slug}...")
            page.goto(url, wait_until="networkidle", timeout=30000)
            
            # El rating está en un div con id="channel_rating"
            rating_element = page.locator("#channel_rating")
            
            if rating_element.count() > 0:
                rating_text = rating_element.inner_text().strip()
                rating_value = float(rating_text)
                logger.info(f"Rating de {channel_slug}: {rating_value}")
                return rating_value
            else:
                logger.warning(f"No se encontró el elemento de rating para {channel_slug}")
                return None
                
        except Exception as e:
            logger.error(f"Error al obtener rating de {channel_slug}: {str(e)}")
            return None
            
    def scrape_all_channels(self) -> Dict[str, Optional[float]]:
        """
        Obtiene los ratings de todos los canales
        
        Returns:
            Diccionario con los ratings de cada canal
        """
        if not self.context:
            raise RuntimeError("El navegador no está iniciado. Llama a start() primero.")
            
        page = self.context.new_page()
        ratings = {}
        
        try:
            for channel_name, channel_slug in self.CHANNELS.items():
                rating = self._fetch_channel_rating(page, channel_slug)
                ratings[channel_name] = rating
                
        finally:
            page.close()
            
        return ratings
