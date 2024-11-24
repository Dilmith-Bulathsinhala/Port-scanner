import argparse
import socket
import time
import random
import struct

# Define common ports for faster scans or special focus
COMMON_PORTS = {
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
}

# Perform banner grabbing to identify services
def banner_grab(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=3) as s:
            s.send(b'HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n'.format(ip.encode()))
            return s.recv(1024).decode(errors="ignore").strip()
    except Exception:
        return None

# Scan a single port
def scan_port(ip, port):
    try:
        with socket.create_connection((ip, port), timeout=1) as sock:
            return True  # Port is open
    except:
        return False  # Port is closed

# Perform OS fingerprinting
def os_fingerprinting(ip):
    sock = None  # Initialize the sock variable to avoid UnboundLocalError
    try:
        # Create a raw socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        sock.settimeout(3)

        # Construct a TCP SYN packet
        source_port = random.randint(1024, 65535)
        dest_port = 80
        seq_num = random.randint(0, 4294967295)

        ip_header = struct.pack(
            '!BBHHHBBH4s4s',
            69, 0, 40, 54321, 0, 64, socket.IPPROTO_TCP, 0,
            socket.inet_aton("192.168.1.1"),  # Replace with your machine's IP
            socket.inet_aton(ip)
        )

        tcp_header = struct.pack(
            '!HHLLBBHHH',
            source_port, dest_port, seq_num, 0, 80, 2, 0, 0, 0
        )

        # Send the packet
        sock.sendto(ip_header + tcp_header, (ip, 0))

        # Wait for a response
        response = sock.recv(1024)

        if response:
            # Analyze the response (simplified logic)
            if b"Windows" in response:
                print("Detected OS: Windows")
            elif b"Linux" in response:
                print("Detected OS: Linux")
            else:
                print("OS detection inconclusive")
        else:
            print("No response received. OS fingerprinting failed.")
    except PermissionError:
        print("OS Fingerprinting failed: Raw sockets require administrator privileges.")
    except Exception as e:
        print(f"OS Fingerprinting failed: {e}")
    finally:
        if sock:
            sock.close()

# Full scan function
def full_scan(ip, start_port, end_port, grab_banner=False):
    print(f"Starting scan on {ip}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            service = COMMON_PORTS.get(port, "Unknown Service")
            print(f"Port {port}: Open ({service})")
            if grab_banner:
                banner = banner_grab(ip, port)
                if banner:
                    print(f"  Banner: {banner}")
            open_ports.append(port)
        # Add a small delay for stealth
        time.sleep(random.uniform(0.1, 0.5))
    if not open_ports:
        print("No open ports detected.")
    else:
        print("\nOpen Ports Summary:")
        for port in open_ports:
            print(f"  Port {port}")
    print("Scan completed.")

# Main entry point for CLI interface
def main():
    # Styled banner for Delta Scanner
    print("-" * 50)
    print(" " * 10 + "Delta Scanner".center(30))
    print("-" * 50)
    
    parser = argparse.ArgumentParser(description="Simple Python Port Scanner with OS Fingerprinting")
    parser.add_argument("-t", "--target", required=True, help="Target IP address to scan")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port (default: 1)")
    parser.add_argument("-e", "--end", type=int, default=65535, help="End port (default: 65535)")
    parser.add_argument("-b", "--banner", action="store_true", help="Enable banner grabbing")
    parser.add_argument("-os", "--osdetect", action="store_true", help="Enable OS fingerprinting")
    args = parser.parse_args()

    print(f"Target: {args.target}, Banner Grabbing: {args.banner}, OS Detection: {args.osdetect}")

    if args.osdetect:
        os_fingerprinting(args.target)

    full_scan(args.target, args.start, args.end, args.banner)

if __name__ == "__main__":
    main()
