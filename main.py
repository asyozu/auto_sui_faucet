import requests
import json
import time

def load_config(filename='config.json'):
    try:
        with open(filename, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file '{filename}' not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error parsing the configuration file '{filename}'.")
        raise

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
        print(f"Error during request: {e}")
        return None

def process_response(response):
    if response.status_code == 429:
        print(f"Rate limit exceeded. Status code: {response.status_code}")
    elif response.status_code == 202:
        try:
            response_json = response.json()
            task_id = response_json.get('task')
            print(f"SUI request successful! Task ID: {task_id}")
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
    else:
        print(f"Failed to request SUI. Status code: {response.status_code}")

def main():
    config = load_config()
    
    if "faucet" not in config or "recipient_address" not in config or "sleep_time" not in config:
        print("Missing necessary configuration values. Exiting...")
        return

    while True:
        response = request_sui(config)
        
        if response:
            process_response(response)
        
        for remaining in range(int(config['sleep_time']), 0, -1):
            print(f"Time remaining: {remaining} seconds", end="\r")
            time.sleep(1)
        print("")

if __name__ == "__main__":
    main()
