import requests
import logging
import random # <--- 1. Importar random

class BaseScraper:
    def __init__(self):
        self.session = requests.Session()
        
        # Configuración de Headers (Anti-bot básico)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
        })
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(self.__class__.__name__)

        # --- 2. CONFIGURACIÓN DE PROXIES ---
        # En producción, esto debería venir de tu .env o de una API de proxies
        self.proxies_disponibles = [
            None # También agregamos None para usar mi IP real a veces
        ]

        # 3. Asignar un proxy inicial al arrancar
        self.rotar_proxy()

    def rotar_proxy(self):
        """Elige un proxy al azar y lo aplica a la sesión actual"""
        if not self.proxies_disponibles:
            return

        proxy_elegido = random.choice(self.proxies_disponibles)
        
        if proxy_elegido:
            self.session.proxies = {
                "http": proxy_elegido,
                "https": proxy_elegido
            }
            self.logger.info(f"🔄 Proxy cambiado a: {proxy_elegido}")
        else:
            # Si sale None, limpiamos los proxies (usa tu IP real)
            self.session.proxies = {}
            self.logger.info("🏠 Usando IP local (Sin proxy)")

    def scrape(self):
        raise NotImplementedError("Implementar en clase hija")