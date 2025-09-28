import argparse
from concurrent.futures import ThreadPoolExecutor
from pingmaster.tcp import send as send_tcp
from pingmaster.udp import send as send_udp
import time
from datetime import datetime

MAX_PORT = 65536

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    args = parser.parse_args()
    target = args.target
    threads = args.threads

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

    now = datetime.now()
    start = time.time()
    print("Starting UDP PING")
    print("Date:", now)
    print("===================")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # TCP S flag test
        for i in range(1, MAX_PORT):
            executor.submit(send_udp, target, i, "pingmaster")
    now = datetime.now()
    print("===================")
    print("ENDING UDP PING")
    print("Date:", now)
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"UDP PING took around {minutes} minutes and {seconds} seconds")
