import requests
import logging
import time
from include.config import API_URL

logger = logging.getLogger(__name__)


def fetch_data(offset, retries=3, timeout=10):
    url = f"{API_URL}?offset={offset}"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=timeout)

            if response.status_code != 200:
                raise Exception(f"Bad response: {response.status_code}")

            data = response.json()

            return data

        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {str(e)}")

            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # exponential backoff
            else:
                raise