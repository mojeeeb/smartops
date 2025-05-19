import os
import json
import time
import requests
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
TRIVY_RESULTS_PATH = "/data/trivy-results.json"
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
CHECK_INTERVAL = 60  # seconds

def read_trivy_results():
    try:
        with open(TRIVY_RESULTS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning(f"Trivy results file not found at {TRIVY_RESULTS_PATH}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in {TRIVY_RESULTS_PATH}")
        return None

def send_to_n8n(data):
    if not N8N_WEBHOOK_URL:
        logger.error("N8N_WEBHOOK_URL environment variable not set")
        return False
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        response.raise_for_status()
        logger.info("Successfully sent data to n8n")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send data to n8n: {str(e)}")
        return False

def main():
    logger.info("Starting SmartOps bot")
    last_processed = None

    while True:
        try:
            current_data = read_trivy_results()
            
            if current_data and current_data != last_processed:
                if send_to_n8n(current_data):
                    last_processed = current_data
                    logger.info("Successfully processed new Trivy results")
                else:
                    logger.error("Failed to process Trivy results")
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main() 