import requests
import time
import logging
import json
import os

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

def get_new_token(config):
    url = "https://gateway-run.bls.dev/api/v1/auth/sign"
    payload = {
        "walletType": config['walletType'],
        "publicAddress": config['publicAddress'],
        "signature": config['signature'],
        "publicKey": config['publicKey']
    }
    headers = {
        "Accept": "*/*",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    token = response.json().get('token')
    logging.info("New token acquired.")
    return token

def get_headers(token):
    return {
        "Accept": "*/*",
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }

def verify_token(token):
    verify_url = "https://gateway-run.bls.dev/api/v1/auth/verify"
    response = requests.get(verify_url, headers=get_headers(token))
    if response.status_code == 401:
        logging.warning("Token expired, acquiring new token...")
        return get_new_token(config)
    else:
        logging.info("Token is valid.")
        return token

def get_node_info(token, node_id):
    node_url = f"https://gateway-run.bls.dev/api/v1/nodes/{node_id}"
    response = requests.get(node_url, headers=get_headers(token))
    response.raise_for_status()
    node_info = response.json()
    
    node_id = node_info.get('_id')
    ip_address = node_info.get('ipAddress')
    total_reward = node_info.get('totalReward')
    today_reward = node_info.get('todayReward')
    is_connected = node_info.get('isConnected')

    connection_status = "Connected" if is_connected else "Disconnected"

    clear_screen()
    logging.info("\n--- Node Information ---\n"
                 f"ID: {node_id}\n"
                 f"IP: {ip_address}\n"
                 f"Total Reward: {total_reward}\n"
                 f"Today's Reward: {today_reward}\n"
                 f"Status: {connection_status}\n"
                 "------------------------")
    
    return node_info

def ping_node(token, node_id):
    ping_url = f"https://gateway-run.bls.dev/api/v1/nodes/{node_id}/ping"
    response = requests.post(ping_url, headers=get_headers(token))
    if response.status_code == 401:
        logging.warning("Token expired during ping, acquiring new token...")
        return get_new_token(config), False
    else:
        logging.info("Ping successful.")
        return token, True

def start_node_session(token, node_id):
    start_session_url = f"https://gateway-run.bls.dev/api/v1/nodes/{node_id}/start-session"
    response = requests.post(start_session_url, headers=get_headers(token))
    if response.status_code == 401:
        logging.warning("Token expired during session start, acquiring new token...")
        return get_new_token(config), False
    else:
        logging.info("Session started successfully.")
        return token, True

def check_health():
    health_url = "https://gateway-run.bls.dev/health"
    response = requests.get(health_url)
    response.raise_for_status()
    health_status = response.json().get('status', 'Unknown')
    logging.info(f"System Health: {health_status}")

def display_myig():
    myig = "@xxiv.uname"
    clear_screen()
    print("========================================")
    print(f"               {myig}")
    print("========================================")

def main_loop():
    config = load_config()
    token = get_new_token(config)
    node_id = config['nodeId']
    last_session_time = 0
    session_interval = 60

    while True:
        try:
            current_time = time.time()

            token = verify_token(token)

            get_node_info(token, node_id)

            check_health()
            
            token, ping_success = ping_node(token, node_id)

            if current_time - last_session_time >= session_interval or not ping_success:
                token, session_success = start_node_session(token, node_id)
                if session_success:
                    last_session_time = current_time

            time.sleep(7)
        
        except requests.exceptions.RequestException as e:
            logging.error(f"Connection error occurred: {e}. Retrying in 10 seconds...")
            time.sleep(10)
        except Exception as e:
            logging.critical(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    display_myig()
    main_loop()