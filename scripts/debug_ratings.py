"""
Debug script - Muestra los valores RAW sin transformar
"""
from rating_scraper import RatingScraper
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    print("=" * 60)
    print("DEBUG: Mostrando valores RAW (sin transformar)")
    print("=" * 60)
    
    with RatingScraper(headless=True) as scraper:
        ratings = scraper.scrape_all_channels()
        
        print("\nRATINGS ORIGINALES (float):")
        print("-" * 60)
        for channel, rating in ratings.items():
            print(f"{channel:12} = {rating} (tipo: {type(rating).__name__})")
        
        print("\nRATINGS CONVERTIDOS A INT:")
        print("-" * 60)
        for channel, rating in ratings.items():
            converted = int(rating) if rating is not None else 0
            print(f"{channel:12} = {converted} (original: {rating})")
