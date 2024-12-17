import requests
import json
import time
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
        print(f"Error: Configuration file '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse the configuration file '{filename}'. Ensure it's valid JSON. Details: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
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
        if not response.ok:
            print(f"Error: Request failed with status code {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: Network or request error occurred. Details: {e}")
        return None

def process_response(response):
    if response is None:
        print("Error: No response received.")
        return

    if response.status_code == 429:
        print("Error: Rate limit exceeded. Please try again later.")
    elif response.status_code == 202:
        try:
            response_json = response.json()
            task_id = response_json.get('task')
            print(f"SUI request successful! Task ID: {task_id}")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse JSON response. Details: {e}")
    else:
        print(f"Error: Request failed. Status code: {response.status_code}, Response: {response.text}")

def main():
    config = load_config()

    try:
        while True:
            response = request_sui(config)
            process_response(response)

            sleep_time = int(config['sleep_time'])
            for remaining in range(sleep_time, 0, -1):
                print(f"\rNext request in {remaining} seconds", end=" ")
                time.sleep(1)
            print("")
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully.")
        sys.exit(0)

if __name__ == "__main__":
    main()
