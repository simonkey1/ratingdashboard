"""
Test script - Ejecuta un scraping único para verificar que todo funciona
"""
from orchestrator import Orchestrator
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    print("=" * 60)
    print("TEST: Ejecutando un scraping único...")
    print("=" * 60)
    
    orchestrator = Orchestrator(csv_filepath="ratings_data.csv", headless=True)
    
    try:
        orchestrator.run_single_scrape()
        print("\n" + "=" * 60)
        print("✓ TEST EXITOSO - Revisa el archivo ratings_data.csv")
        print("=" * 60)
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ TEST FALLIDO: {str(e)}")
        print("=" * 60)
        raise
