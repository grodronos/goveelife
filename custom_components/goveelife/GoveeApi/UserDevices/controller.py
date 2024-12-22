# GoveeApi/UserDevices/controller.py

import requests
from typing import List, Dict
from .models import Response, Device
import logging

# Konfigurace loggeru
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Controller:
    def __init__(self, api_key: str, timeout: int = 10):
        """
        Inicializuje Controller s přednastavenou URL, hlavičkami a timeoutem.

        Args:
            api_key (str): API klíč pro Govee API.
            timeout (int, optional): Timeout pro HTTP požadavky v sekundách. Defaults to 10.
        """
        self.base_url = "https://openapi.api.govee.com/router/api/v1"
        self.timeout = timeout
        self.headers={
            "Content-Type":"application/json",
            "Govee-API-Key": api_key
        }

    async def getDevices(self, hass) -> List[Device]:
        """
        Asynchronně získá seznam zařízení z API.

        Args:
            hass: Instance Home Assistant (předpokládá se, že metoda je volána v kontextu Home Assistant).

        Returns:
            List[Device]: Seznam zařízení.
        """
        path = 'user/devices'
        url = f"{self.base_url}/{path.strip('/')}"
        logger.info(f"Request URL: {url}")

        try:
            # Definujte lambda funkci pro požadavek
            request_func = lambda: requests.get(url, headers=self.headers, timeout=self.timeout)

            # Spusťte požadavek v executor job (blokující operace mimo hlavní vlákno)
            response = await hass.async_add_executor_job(request_func)

            # Zkontrolujte HTTP status kód
            if response.status_code != 200:
                logger.error(f"HTTP Error: {response.status_code} - {response.text}")
                response.raise_for_status()

            # Získejte JSON data
            response_json = response.json()
            logger.debug(f"Response JSON: {response_json}")

            # Parsování odpovědi pomocí metody parse_api_response
            api_response = self.parse_api_response(response_json)

            if api_response.code != 200:
                logger.error(f"API Error: {api_response.code} - {api_response.message}")
                raise Exception(f"API Error: {api_response.message}")

            logger.info(f"Successfully retrieved {len(api_response.data)} devices.")
            return api_response.data

        except requests.exceptions.RequestException as e:
            logger.error(f"Request Exception: {e}")
            raise
        except Exception as e:
            logger.error(f"General Exception: {e}")
            raise

    def parse_api_response(self, response: Dict) -> Response:
        """
        Parsuje API odpověď a vrací instanci Response.

        Args:
            response (Dict): API odpověď ve formě slovníku.

        Returns:
            Response: Parsovaný model odpovědi.
        """
        try:
            api_response = Response(**response)
            return api_response
        except Exception as e:
            logger.error(f"Chyba při parsování odpovědi: {e}")
            raise
