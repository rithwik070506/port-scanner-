# Simple Multithreaded Port Scanner
# Educational use only

import socket
import threading
from queue import Queue

target = input("Enter Target IP or Website: ")
start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

queue = Queue()
open_ports = []

print_lock = threading.Lock()

# Convert website to IP
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid target")
    exit()

print(f"\nScanning Target: {target_ip}\n")


def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        result = s.connect_ex((target_ip, port))

        if result == 0:
            try:
                banner = s.recv(1024).decode().strip()
            except:
                banner = "No Banner"

            with print_lock:
                print(f"[OPEN] Port {port} | Service: {banner}")

            open_ports.append(port)

        s.close()

    except:
        pass


def threader():
    while True:
        port = queue.get()
        scan_port(port)
        queue.task_done()


# Create threads
for _ in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# Add ports to queue
for port in range(start_port, end_port + 1):
    queue.put(port)

queue.join()

print("\nScan Completed!")
print("Open Ports:", open_ports)