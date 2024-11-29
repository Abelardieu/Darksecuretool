import os
import platform
import requests
import socket
from scapy.all import *
from stem.control import Controller
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

def display_banner():
    banner = pyfiglet.figlet_format("Dark Secure Tool")
    half = len(banner) // 2
    print(Fore.CYAN + banner[:half] + Style.RESET_ALL, end="")
    print(Fore.GREEN + banner[half:] + Style.RESET_ALL)
    print(Fore.YELLOW + "By: Abelardieu\n" + Style.RESET_ALL)
    print("Protect your anonymity on the darknet by detecting risks and improving your security.\n")
    print("=" * 80)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_red(message):
    print(Fore.RED + message + Style.RESET_ALL)

def pause():
    input(Fore.YELLOW + "\nPress Enter to return to the menu..." + Style.RESET_ALL)

def check_tor_connection():
    print_red("[*] Verifying Tor connection...")
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            status = controller.get_info("status/circuit-established")
            tor_version = controller.get_version()
            if status == "1":
                print_red(f"[+] Tor is configured correctly. Version: {tor_version}\n")
            else:
                print_red("[-] Tor is not connected correctly.\n")
    except Exception as e:
        print_red(f"[-] Error checking Tor: {e}\n")

def check_os_security():
    print_red("[*] Checking operating system security...")
    os_name = platform.system()
    os_version = platform.version()
    print_red(f"[*] OS Detected: {os_name} (version: {os_version})\n")
    if os_name.lower() == "linux":
        print_red("[+] Linux-based OS detected. Ensure it is updated.\n")
    elif os_name.lower() == "windows":
        print_red("[!] Windows detected. Disable unnecessary services for better security.\n")
    else:
        print_red("[!] Unknown OS detected. Take extra precautions.\n")

def check_webrtc_leak():
    print_red("[*] Checking WebRTC leaks...")
    try:
        response = requests.get("https://browserleaks.com/webrtc", timeout=10)
        if "STUN" in response.text:
            print_red("[-] Potential WebRTC leak detected. Disable WebRTC in your browser.\n")
        else:
            print_red("[+] No WebRTC leaks detected.\n")
    except Exception as e:
        print_red(f"[-] Error checking WebRTC leaks: {e}\n")

def check_dns_leaks():
    print_red("[*] Checking DNS leaks...")
    try:
        dns_query = sr1(IP(dst="8.8.8.8")/UDP()/DNS(rd=1, qd=DNSQR(qname="google.com")), timeout=2, verbose=0)
        if dns_query:
            print_red(f"[-] Possible DNS leak detected: {dns_query[IP].src}\n")
        else:
            print_red("[+] No DNS leaks detected.\n")
    except Exception as e:
        print_red(f"[-] Error checking DNS leaks: {e}\n")

def scan_open_ports():
    print_red("[*] Scanning open ports on localhost...")
    for port in range(1, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex(('127.0.0.1', port))
            if result == 0:
                print_red(f"[+] Open port: {port}")
            s.close()
    print()

def check_tor_browser_config():
    print_red("[*] Checking Tor browser configuration...")
    try:
        response = requests.get("https://check.torproject.org/", timeout=10)
        if "Congratulations" in response.text:
            print_red("[+] Tor browser is configured correctly.\n")
        else:
            print_red("[-] Tor browser configuration is not optimized.\n")
    except Exception as e:
        print_red(f"[-] Error checking Tor browser configuration: {e}\n")

def main():
    while True:
        clear_screen()
        display_banner()
        print("Menu:")
        print("1. Check Tor Connection")
        print("2. Check OS Security")
        print("3. Check WebRTC Leaks")
        print("4. Check DNS Leaks")
        print("5. Scan Open Ports")
        print("6. Check Tor Browser Config")
        print("7. Exit")
        choice = input("\nEnter your choice: ")

        if choice == "1":
            clear_screen()
            check_tor_connection()
            pause()
        elif choice == "2":
            clear_screen()
            check_os_security()
            pause()
        elif choice == "3":
            clear_screen()
            check_webrtc_leak()
            pause()
        elif choice == "4":
            clear_screen()
            check_dns_leaks()
            pause()
        elif choice == "5":
            clear_screen()
            scan_open_ports()
            pause()
        elif choice == "6":
            clear_screen()
            check_tor_browser_config()
            pause()
        elif choice == "7":
            clear_screen()
            print_red("\nExiting Dark Secure Tool. Stay safe!\n")
            break
        else:
            clear_screen()
            print_red("Invalid choice. Please try again.\n")
            pause()

if __name__ == "__main__":
    try:
        import pyfiglet
        from colorama import Fore, Style
    except ImportError:
        print("Installing required libraries...")
        os.system("pip install pyfiglet colorama")
    main()
