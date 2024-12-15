import requests, json, time

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

while True:
    response = requests.post(f'https://faucet.{config["faucet"]}.sui.io/v1/gas', 
                             headers={'Content-Type': 'application/json'}, 
                             data=json.dumps({"FixedAmountRequest": {"recipient": config["recipient_address"]}}))
    if response.status_code == 429:
        print(f"Failed to request SUI. Status code: {response.status_code}")
    else:
        response_json = response.json()
        task_id = response_json.get('task')
        print(f"SUI request successful! Task ID: {task_id}")
    for remaining in range(int(config['sleep_time']), 0, -1):
        print(f"Time remaining: {remaining}", end="\r")
        time.sleep(1)
    print()
