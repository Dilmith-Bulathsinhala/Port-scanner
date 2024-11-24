
# Delta Scanner - A Simple Python Port Scanner with OS Fingerprinting

Delta Scanner is a basic yet powerful Python-based tool designed for scanning open ports and performing OS fingerprinting on a remote host. With a few simple command-line options, you can perform various network reconnaissance tasks, including banner grabbing, OS detection, and scanning specific ports for vulnerabilities.

This tool is ideal for users interested in network security, penetration testing, or anyone wanting to quickly assess the security status of a target device or server.

## Features

- **Port Scanning**: Scans a range of ports (default: 1-65535) to identify open services.
- **Banner Grabbing**: Retrieves and displays service banners for detected open ports.
- **OS Fingerprinting**: Tries to detect the operating system of the target machine using raw TCP/IP packet analysis.

## Requirements

- Python 3.x
- Administrator privileges (for OS fingerprinting)
- Internet connection for banner grabbing on common services

## Installation

1. Clone or download the repository to your local machine.
2. Ensure you have Python 3.x installed on your system.
3. Run the script using the following command.

---

## Usage

Run the following command in the terminal to start scanning:

```bash
python scanner.py -t TARGET_IP
```

### Command-Line Options

- `-t`, `--target`:  
  **Required**  
  Specifies the IP address of the target system to scan. Replace `TARGET_IP` with the actual IP you want to scan.
  
  Example:
  ```bash
  python scanner.py -t 192.168.1.100
  ```

- `-s`, `--start`:  
  **Optional**  
  Defines the starting port for the scan (default: 1). The tool will scan all ports starting from this number up to the value specified by `--end`.  
  Example:
  ```bash
  python scanner.py -t 192.168.1.100 -s 80
  ```

- `-e`, `--end`:  
  **Optional**  
  Defines the ending port for the scan (default: 65535). The tool will scan all ports up to this number starting from the value specified by `--start`.  
  Example:
  ```bash
  python scanner.py -t 192.168.1.100 -e 1000
  ```

- `-b`, `--banner`:  
  **Optional**  
  Enables banner grabbing for open ports. This feature retrieves and displays the banner (service details) for open ports, helping you identify the running services.  
  Example:
  ```bash
  python scanner.py -t 192.168.1.100 -b
  ```

- `-os`, `--osdetect`:  
  **Optional**  
  Enables OS fingerprinting. This attempts to determine the operating system running on the target machine based on raw packet analysis. Requires administrator privileges.  
  Example:
  ```bash
  python scanner.py -t 192.168.1.100 -os
  ```

### Example

```bash
python scanner.py -t 192.168.1.100 -s 1 -e 1024 -b -os
```

This will:
1. Scan ports from 1 to 1024.
2. Enable banner grabbing for each open port.
3. Attempt to perform OS fingerprinting on the target machine.

---

## Notes

- **Administrator Privileges**: OS fingerprinting requires raw socket access, which typically requires administrator privileges. Make sure to run the script as an administrator if you're using OS fingerprinting.
  
- **Accuracy**: The OS detection feature relies on the response to raw TCP packets and may not always be 100% accurate. It's a basic method, and results may vary depending on the network environment.

---

## License

This tool is open-source and free to use for educational and research purposes. Use it responsibly and ensure that you have permission to scan the target systems.
