import argparse
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pingmaster.tcp import send as send_tcp
from pingmaster.udp import send as send_udp
from pingmaster.sctp import send as send_sctp
from pingmaster.icmp import send as send_icmp
from pingmaster.ah import send as send_ah
from pingmaster.esp import send as send_esp
from pingmaster.gre import send as send_gre
from pingmaster.igmp import send as send_igmp
from pingmaster.pim import send as send_pim
from pingmaster.ospf import send as send_ospf
from pingmaster.carp import send as send_carp
import time
from datetime import datetime

class PingTypes(Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    AH = "AH"
    ESP = "ESP"
    GRE = "GRE"
    IGMP = "IGMP"
    PIM = "PIM"
    OSPF = "OSPF"
    SCTP = "SCTP"
    CARP = "CARP"

MAX_PORT = 65536
MAX_ICMP_TYPES = 256

start = None
end = None

def test_text_pre(name):
    now = datetime.now()
    global start
    start = time.time()
    print("Starting", name)
    print("Date:", now)
    print("===================")

def test_text_post(name):
    now = datetime.now()
    print("===================")
    print("ENDING", name)
    print("Date:", now)
    global start, end
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"{name} took around {minutes} minutes and {seconds} seconds")

def test_tcp(target, threads, data):
    test_text_pre("TCP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:

        for i in range(1, MAX_PORT):
            executor.submit(send_tcp, target, i, data, "S")

    test_text_post("TCP PING")

def test_udp(target, threads, data):
    test_text_pre("UDP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(1, MAX_PORT):
            executor.submit(send_udp, target, i, data)
    test_text_post("UDP PING")

def test_sctp(target, threads, data):
    test_text_pre("SCTP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(1, MAX_PORT):
            executor.submit(send_sctp, target, i, data)
    test_text_post("SCTP PING")

def test_icmp(target, threads, data):
    test_text_pre("ICMP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(1, MAX_ICMP_TYPES):
            executor.submit(send_icmp, target, i, data)
    test_text_post("ICMP PING")

def test_ah(target, threads, data):
    test_text_pre("AH PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_ah, target, data)
    test_text_post("AH PING")

def test_esp(target, threads, data):
    test_text_pre("ESP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_esp, target, data)
    test_text_post("ESP PING")

def test_gre(target, threads, data):
    test_text_pre("GRE PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_gre, target, data)
    test_text_post("GRE PING")

def test_igmp(target, threads, data):
    test_text_pre("IGMP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_igmp, target, data)
    test_text_post("IGMP PING")

def test_pim(target, threads, data):
    test_text_pre("PIM PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_pim, target, data)
    test_text_post("PIM PING")

def test_ospf(target, threads, data):
    test_text_pre("OSPF PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_ospf, target, data)
    test_text_post("OSPF PING")

def test_carp(target, threads, data):
    test_text_pre("CARP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_carp, target, data)
    test_text_post("CARP PING")

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    parser.add_argument("-m", "--method", required=False, type= PingTypes, choices=[m.value for m in PingTypes])
    parser.add_argument("-d", "--data", type=str, default="pingmaster", help="Data to send. (Default: pingmaster)")
    args = parser.parse_args()
    target = args.target
    threads = args.threads
    data = args.data

    if args.method:
        if args.method == PingTypes.TCP:
            test_tcp(target, threads, data)
        elif args.method == PingTypes.UDP:
            test_udp(target, threads, data)
        elif args.method == PingTypes.ICMP:
            test_icmp(target, threads, data)
        elif args.method == PingTypes.AH:
            test_ah(target, threads, data)
        elif args.method == PingTypes.ESP:
            test_esp(target, threads, data)
        elif args.method == PingTypes.GRE:
            test_gre(target, threads, data)
        elif args.method == PingTypes.IGMP:
            test_igmp(target, threads, data)
        elif args.method == PingTypes.PIM:
            test_pim(target, threads, data)
        elif args.method == PingTypes.OSPF:
            test_ospf(target, threads, data)
        elif args.method == PingTypes.SCTP:
            test_sctp(target, threads, data)
        elif args.method == PingTypes.CARP:
            test_carp(target, threads, data)

    else:
        test_tcp(target, threads, data)
        test_udp(target, threads, data)
        test_sctp(target, threads, data)
        test_icmp(target, threads, data)
        test_ah(target, threads, data)
        test_esp(target, threads, data)
        test_gre(target, threads, data)
        test_igmp(target, threads, data)
        test_pim(target, threads, data)
        test_ospf(target, threads, data)
        test_carp(target, threads, data)

