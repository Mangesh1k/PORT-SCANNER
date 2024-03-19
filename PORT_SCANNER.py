import socket

def scan_ports(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set timeout to 1 second for connection attempt
            s.settimeout(1)
            # Attempt to connect to the target IP address and port
            result = s.connect_ex((target, port))
            # If the connection was successful, the port is open
            if result == 0:
                open_ports.append(port)
            # Close the socket
            s.close()
        except KeyboardInterrupt:
            print("\nExiting scan.")
            exit()
        except socket.gaierror:
            print("Hostname could not be resolved.")
            exit()
        except socket.error:
            print("Couldn't connect to server.")
            exit()
    return open_ports

def detect_services(target, open_ports):
    for port in open_ports:
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set timeout to 1 second for connection attempt
            s.settimeout(1)
            # Connect to the target IP address and port
            s.connect((target, port))
            # Send a message to request service information
            s.send(b'HELLO\r\n')
            # Receive up to 1024 bytes of response
            response = s.recv(1024)
            # Print the service information received
            print(f"Port {port} : {response.decode().strip()}")
            # Close the socket
            s.close()
        except KeyboardInterrupt:
            print("\nExiting scan.")
            exit()
        except socket.gaierror:
            print("Hostname could not be resolved.")
            exit()
        except socket.error:
            print("Couldn't connect to server.")
            exit()

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter start port number: "))
    end_port = int(input("Enter end port number: "))

    open_ports = scan_ports(target_ip, start_port, end_port)
    if open_ports:
        print("Open ports:", open_ports)
        detect_services(target_ip, open_ports)
    else:
        print("No open ports found on the target.")
