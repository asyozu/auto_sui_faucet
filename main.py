import requests
import json
import time
import logging
import sys

def load_config(filename='config.json'):
    try:
        with open(filename, 'r') as config_file:
            config = json.load(config_file)
            required_keys = ["faucet", "recipient_address", "sleep_time"]
            if not all(key in config for key in required_keys):
                raise ValueError(f"Missing required keys in config file: {', '.join(required_keys)}")
            return config
    except FileNotFoundError:
        logging.error(f"Configuration file '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        logging.error(f"Error parsing the configuration file '{filename}'. Ensure it's valid JSON.")
        sys.exit(1)
    except ValueError as e:
        logging.error(e)
        sys.exit(1)

def request_sui(config):
    url = f'https://faucet.{config["faucet"]}.sui.io/v1/gas'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "FixedAmountRequest": {
            "recipient": config["recipient_address"]
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        return response
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during request: {e}")
        return None

def process_response(response):
    if response.status_code == 429:
        logging.warning("Rate limit exceeded. Please try again later.")
    elif response.status_code == 202:
        try:
            response_json = response.json()
            task_id = response_json.get('task')
            logging.info(f"SUI request successful! Task ID: {task_id}")
        except json.JSONDecodeError:
            logging.error("Failed to parse JSON response.")
    else:
        logging.error(f"Failed to request SUI. Status code: {response.status_code}, Response: {response.text}")

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    config = load_config()

    try:
        while True:
            response = request_sui(config)
            if response:
                process_response(response)

            sleep_time = int(config['sleep_time'])
            for remaining in range(sleep_time, 0, -1):
                print(f"Next request in {remaining}", end="\r")
                time.sleep(1)
            print("")
    except KeyboardInterrupt:
        logging.info("\nProcess interrupted by user. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
