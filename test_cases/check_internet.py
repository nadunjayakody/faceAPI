import socket

host = "8.8.8.8"  # Google DNS
port = 53  # DNS service port
timeout = 3  # Timeout in seconds

def check_internet():
    try:
        socket.setdefaulttimeout(timeout)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print("Internet is connected")
        s.close()
        return True
    except socket.error as ex:
        print(f"No internet connection. Error: {ex}")
        return False

if __name__ == "__main__":
    check_internet()
