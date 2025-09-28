import argparse
from concurrent.futures import ThreadPoolExecutor
from scapy.all import send
from scapy.layers.inet import IP
from pingmaster.tcp import send as send_tcp
import time
from datetime import datetime

def send_safe(target):
    ip_packet = IP(dst=target)
    send(ip_packet, verbose=False)

def send_broken_version_packet(target, version = 1):
    ip_packet = IP(dst=target, version=version) / b"PM_VERSION"
    send(ip_packet, verbose=False)

def send_packets_with_all_tos(target):
    for tos_value in range(256):  # TOS values range from 0 to 255
        # Create an IP packet with the current TOS value

        ip_packet = IP(dst=target, tos=tos_value) / (bytes(f"PM_TOS_{tos_value}", "utf-8"))
        
        # Send the packet
        send(ip_packet)

def send_do_not_fragment(target):
    ip_packet = IP(dst=target, flags="DF") / b"PM_DF"
    send(ip_packet, verbose=False)

MAX_PORT = 65536

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    args = parser.parse_args()
    target = args.target
    threads = args.threads

    # Create a raw IP packet
    # send_safe(target)
    # send_broken_version_packet(target)
    # send_packets_with_all_tos(target)
    # send_do_not_fragment(target)

    now = datetime.now()
    start = time.time()
    print("Starting TCP SYN PING")
    print("Date:", now)
    print("===================")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # TCP S flag test
        for i in range(1, MAX_PORT):
            executor.submit(send_tcp, target, i, "pingmaster", "S")
    now = datetime.now()
    print("===================")
    print("ENDING TCP SYN PING")
    print("Date:", now)
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"TCP SYN PING took around {minutes} minutes and {seconds} seconds")
