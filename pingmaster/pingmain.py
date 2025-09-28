import argparse
from concurrent.futures import ThreadPoolExecutor
from pingmaster.tcp import send as send_tcp
from pingmaster.udp import send as send_udp
from pingmaster.icmp import send as send_icmp
from pingmaster.ah import send as send_ah
from pingmaster.esp import send as send_esp
import time
from datetime import datetime

MAX_PORT = 65536
MAX_ICMP_TYPES = 256

def test_tcp(target, threads):
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

def test_udp(target, threads):
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

def test_icmp(target, threads):
    now = datetime.now()
    start = time.time()
    print("Starting ICMP PING")
    print("Date:", now)
    print("===================")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        # TCP S flag test
        for i in range(1, MAX_ICMP_TYPES):
            executor.submit(send_icmp, target, i, "pingmaster")
    now = datetime.now()
    print("===================")
    print("ENDING ICMP PING")
    print("Date:", now)
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"ICMP PING took around {minutes} minutes and {seconds} seconds")

def test_ah(target, threads):
    now = datetime.now()
    start = time.time()
    print("Starting AH PING")
    print("Date:", now)
    print("===================")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_ah, target, "pingmaster")
    now = datetime.now()
    print("===================")
    print("ENDING AH PING")
    print("Date:", now)
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"ICMP AH took around {minutes} minutes and {seconds} seconds")

def test_esp(target, threads):
    now = datetime.now()
    start = time.time()
    print("Starting ESP PING")
    print("Date:", now)
    print("===================")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_esp, target, "pingmaster")
    now = datetime.now()
    print("===================")
    print("ENDING ESP PING")
    print("Date:", now)
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"ICMP ESP took around {minutes} minutes and {seconds} seconds")

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    parser.add_argument("-m", "--method", required=False, choices=["TCP", "UDP", "ICMP", "AH", "ESP"])
    args = parser.parse_args()
    target = args.target
    threads = args.threads

    if args.method:
        if args.method == "TCP":
            test_tcp(target, threads)
        elif args.method == "UDP":
            test_udp(target, threads)
        elif args.method == "ICMP":
            test_icmp(target, threads)
        elif args.method == "AH":
            test_ah(target, threads)
        elif args.method == "ESP":
            test_esp(target, threads)

    else:
        test_tcp(target, threads)
        test_udp(target, threads)
        test_icmp(target, threads)
        test_ah(target, threads)
        test_esp(target, threads)
