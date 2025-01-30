import requests
import time

def check_server(url, interval=5):
    """
    Continuously checks if the server is working.
    
    Args:
        url (str): The URL of the server to check.
        interval (int): Time interval (in seconds) between checks.
    """
    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Server works fine.")
            else:
                print(f"Server is not working. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print("Server is not working. Error:", e)
        
        time.sleep(interval)  # Wait for the specified interval before checking again


check_server("https://ientrada.raccoon-ai.io/api", interval=5)
