import requests
import json
import warnings
import argparse
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

URL_BASE = "https://192.168.0.160:8443"
LOGIN_ENDPOINT = "/api/login"
HEADERS = {
    "Content-Type": "application/json"
}
VERIFY_SSL = False
USERNAME = os.environ.get("UNIFI_USERNAME")
PASSWORD = os.environ.get("UNIFI_PASSWORD")

if not USERNAME or not PASSWORD:
    raise ValueError("The environment variables UNIFI_USERNAME and UNIFI_PASSWORD must be defined.")

session = requests.Session()


def login():
    login_payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    response = session.post(URL_BASE + LOGIN_ENDPOINT, headers=HEADERS, data=json.dumps(login_payload), verify=VERIFY_SSL)
    if response.status_code != 200:
        print("Login Error!")
        exit(3)


def check_users():
    login()
    STAT_SITES_ENDPOINT = "/api/stat/sites"
    response = session.get(URL_BASE + STAT_SITES_ENDPOINT, headers=HEADERS, verify=VERIFY_SSL)

    if response.status_code != 200:
        print(f"Error fetching data! Error: {response.text}")
        exit(3)

    data = response.json()["data"]
    if not data:
        print("No site found!")
        exit(3)

    num_users = data[0]["health"][0]["num_user"]
    
    if num_users <= 100:
        print(f"OK! Number of connected devices: {num_users} | users={num_users}")
        exit(0)
    elif 100 < num_users <= 150:
        print(f"WARN! Number of connected devices: {num_users} | users={num_users}")
        exit(1)
    else:
        print(f"CRITICAL! Number of connected devices: {num_users} | users={num_users}")
        exit(2)

def check_aps():
    login()
    STAT_SITES_ENDPOINT = "/api/stat/sites"
    response = session.get(URL_BASE + STAT_SITES_ENDPOINT, headers=HEADERS, verify=VERIFY_SSL)

    if response.status_code != 200:
        print(f"Error fetching data! Erroe: {response.text}")
        exit(3)

    data = response.json()["data"]
    if not data:
        print("No site found!")
        exit(3)

    num_aps = data[0]["health"][0]["num_ap"]
    num_adopted = data[0]["health"][0]["num_adopted"]
    
    if num_aps != num_adopted:
        print(f"WARN! Number of APs: {num_aps}, number of adopted: {num_adopted} | aps={num_aps}")
        exit(1)
    else:
        print(f"OK! Number of APs: {num_aps}, number of adopted: {num_adopted} | aps={num_aps}")
        exit(0)

def check_status():
    login()
    STAT_HEALTH_ENDPOINT = "/api/s/default/stat/health"
    response = session.get(URL_BASE + STAT_HEALTH_ENDPOINT, headers=HEADERS, verify=VERIFY_SSL)

    if response.status_code != 200:
        print(f"CRITICAL! Error fetching data! Error: {response.text}")
        exit(3)

    data = response.json()["data"]
    if not data:
        print("CRITICAL!  No health data found!")
        exit(3)

    wlan_status = next((subsystem["status"] for subsystem in data if subsystem["subsystem"] == "wlan"), None )

    if wlan_status == "ok":
        print("OK! All subsystems are operational.")
        exit(0)
    else:
        print("WARN! Not all subsystems are operational.")
        exit(1)


def main():
    parser = argparse.ArgumentParser(description="UniFi Monitoring.")
    parser.add_argument("command", choices=["users","aps","status"], help="The command to be executed.")
    args = parser.parse_args()

    if args.command == "users":
        check_users()
    if args.command == "aps":
        check_aps()
    if args.command == "status":
        check_status()


if __name__ == "__main__":
    main()
