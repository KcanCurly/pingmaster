import argparse
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from pingmaster.tcp import TCP_Type
from pingmaster.udp import UDP_Type
from pingmaster.udplite import UDPLite_Type
from pingmaster.sctp import SCTP_Type
from pingmaster.icmp import ICMP_Type
from pingmaster.ah import send as send_ah
from pingmaster.esp import send as send_esp
from pingmaster.gre import send as send_gre
from pingmaster.igmp import send as send_igmp
from pingmaster.pim import send as send_pim
from pingmaster.ospf import send as send_ospf
from pingmaster.carp import send as send_carp
from pingmaster.utility import parse_ports, CustomAction
import time
from datetime import datetime
import os

# Src ports: 53, 80, 135, 443, 50000

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
    UDPL = "UDPLite"

MAX_PORT = 65536
MAX_ICMP_TYPES = 256
SOURCE_PORT = 44444
FLOW_ID = 34443

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
    print("ENDING", name)
    print("Date:", now)
    global start, end
    end = time.time()
    minutes, seconds = map(int,divmod(end - start, 60))
    print(f"{name} took around {minutes} minutes and {seconds} seconds")
    print("===================")

def test_tcp(ipv4_target, ipv6_target, threads, data, ports, source_ports):
    test_text_pre("TCP PING")
    i = TCP_Type(ipv4_target, ipv6_target, data, ports, source_ports)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        i.send(executor)
    test_text_post("TCP PING")

def test_udp(ipv4_target, ipv6_target, threads, data, ports, source_ports):
    test_text_pre("UDP PING")
    i = UDP_Type(ipv4_target, ipv6_target, data, ports, source_ports)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        i.send(executor)
    test_text_post("UDP PING")

def test_udplite(ipv4_target, ipv6_target, threads, data, ports, source_ports):
    test_text_pre("UDPLite PING")
    i = UDPLite_Type(ipv4_target, ipv6_target, data, ports, source_ports)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        i.send(executor)
    test_text_post("UDPLite PING")

def test_sctp(ipv4_target, ipv6_target, threads, data, ports, source_ports):
    test_text_pre("SCTP PING")
    i = SCTP_Type(ipv4_target, ipv6_target, data, ports, source_ports)
    with ThreadPoolExecutor(max_workers=threads) as executor:
        i.send(executor)
    test_text_post("SCTP PING")

def test_icmp(ipv4_target, ipv6_target, threads, data):
    i = ICMP_Type(ipv4_target, ipv6_target, data, None)
    test_text_pre("ICMP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        i.send(executor)
    test_text_post("ICMP PING")

def test_ah(target, threads, data):
    test_text_pre("AH PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_ah, target, data, None)
    test_text_post("AH PING")

def test_esp(target, threads, data):
    test_text_pre("ESP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_esp, target, data, None)
    test_text_post("ESP PING")

def test_gre(target, threads, data):
    test_text_pre("GRE PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_gre, target, data, None)
    test_text_post("GRE PING")

def test_igmp(target, threads, data):
    test_text_pre("IGMP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_igmp, target, data, None)
    test_text_post("IGMP PING")

def test_pim(target, threads, data):
    test_text_pre("PIM PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_pim, target, data, None)
    test_text_post("PIM PING")

def test_ospf(target, threads, data):
    test_text_pre("OSPF PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_ospf, target, data, None)
    test_text_post("OSPF PING")

def test_carp(target, threads, data):
    test_text_pre("CARP PING")
    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.submit(send_carp, target, data, None)
    test_text_post("CARP PING")

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("--ipv4", help="Target IPv4 address")
    parser.add_argument("--ipv6", help="Target IPv6 address")
    parser.add_argument(
    "-p", "--ports",
    action=CustomAction,
    nargs="+",
    help="Destination ports or ranges (e.g., 80 443 1000-2000)"
    )
    parser.add_argument(
    "--source-port",
    action=CustomAction,
    nargs="+",
    default=[44444],
    help="Source ports or ranges (e.g., 80 443 1000-2000)"
    )
    parser.add_argument("-t", "--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    parser.add_argument("-m", "--method", required=False, choices=[m.value for m in PingTypes])
    parser.add_argument("-d", "--data", type=str, default="pingmaster", help="Data to send. (Default: pingmaster)")
    args = parser.parse_args()

    if os.geteuid() != 0:
        print("Run as root, exiting")
        os._exit(1)

    if not (args.ipv4 or args.ipv6):
        parser.error("You must specify at least --ipv4 or --ipv6")

    threads = args.threads
    data = args.data
    global SOURCE_PORT
    SOURCE_PORT = args.source_port

    if args.ports:
        ports = []
        for a in args.ports:
            ports += parse_ports(a)
    else:
        ports = [i for i in range(0, MAX_PORT)]

    if args.source_port:
        source_ports = []
        for a in args.source_port:
            source_ports += parse_ports(a)
    else:
        source_ports = [44444]



    if args.method:
        if args.method == PingTypes.TCP.value:
            test_tcp(args.ipv4, args.ipv6, threads, data, ports, args.source_ports)
        elif args.method == PingTypes.UDP.value:
            test_udp(args.ipv4, args.ipv6, threads, data, ports, args.source_ports)
        elif args.method == PingTypes.UDPL.value:
            test_udplite(args.ipv4, args.ipv6, threads, data, ports, args.source_ports)
        elif args.method == PingTypes.SCTP.value:
            test_sctp(args.ipv4, args.ipv6, threads, data, ports, args.source_ports)
        elif args.method == PingTypes.ICMP.value:
            test_icmp(args.ipv4, args.ipv6, threads, data)
        elif args.method == PingTypes.AH.value:
            test_ah(args.ipv4, threads, data)
        elif args.method == PingTypes.ESP.value:
            test_esp(args.ipv4, threads, data)
        elif args.method == PingTypes.GRE.value:
            test_gre(args.ipv4, threads, data)
        elif args.method == PingTypes.IGMP.value:
            test_igmp(args.ipv4, threads, data)
        elif args.method == PingTypes.PIM.value:
            test_pim(args.ipv4, threads, data)
        elif args.method == PingTypes.OSPF.value:
            test_ospf(args.ipv4, threads, data)

        elif args.method == PingTypes.CARP.value:
            test_carp(args.ipv4, threads, data)
    else:
        test_tcp(args.ipv4, args.ipv6, threads, data)
        test_udp(args.ipv4, args.ipv6, threads, data)
        test_sctp(args.ipv4, args.ipv6, threads, data)
        test_icmp(args.ipv4, args.ipv6, threads, data)
        test_ah(args.ipv4, threads, data)
        test_esp(args.ipv4, threads, data)
        test_gre(args.ipv4, threads, data)
        test_igmp(args.ipv4, threads, data)
        test_pim(args.ipv4, threads, data)
        test_ospf(args.ipv4, threads, data)
        test_carp(args.ipv4, threads, data)

