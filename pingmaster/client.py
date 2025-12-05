import os
import random
import string
from scapy.all import Raw, sr
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.inet6 import IPv6
from scapy.layers.sctp import SCTP
import argparse
import sys, signal

from pingmaster.pingmain import PingTypes, MAX_ICMP_TYPES, MAX_PORT
from pingmaster.tcp import TCP_Type
from pingmaster.utility import parse_ports

chars = string.ascii_letters + string.digits

def signal_handler(signal, frame):
    sys.exit(0)

def main():
    from pingmaster.pingmain import FLOW_ID
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("--ipv4", help="Target IPv4 address")
    parser.add_argument("--ipv6", help="Target IPv6 address")
    parser.add_argument(
    "-p", "--ports",
    nargs="+",
    action="extend",
    help="Destination ports or ranges (e.g., 80 443 1000-2000) (default: all ports)"
    )
    parser.add_argument(
    "--source-port",
    nargs="+",
    action="extend",
    help="Source ports or ranges (e.g., 80 443 1000-2000) (default: 44444)"
    )
    parser.add_argument("--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    parser.add_argument("--timeout", type=int, default=3, help="Amount of timeout to wait for packets. (Default: 3)")
    parser.add_argument("-m", "--method", required=True, choices=[m.value for m in PingTypes])
    args = parser.parse_args()

    if os.geteuid() != 0:
        print("Run as root, exiting")
        os._exit(1)

    if not (args.ipv4 or args.ipv6):
        parser.error("You must specify at least --ipv4 or --ipv6")


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

    signal.signal(signal.SIGINT, signal_handler)

    t = {}
    if args.ipv4:
        t[IP] = args.ipv4
    if args.ipv6:
        t[IPv6] = args.ipv6
    m = PingTypes[args.method]

    for ipv, target in t.items():
        if m in [PingTypes.TCP, PingTypes.UDP, PingTypes.UDPL, PingTypes.SCTP]:
            for sport in source_ports:
                for dport in ports:
                    random_data = b"pm-" + bytes(''.join(random.choice(chars) for _ in range(5)), "utf-8")
                    i = ipv(dst=target, id=FLOW_ID)
                    if m == PingTypes.TCP:
                        i2 = TCP(dport=dport, sport=sport, flags="S")
                    elif m == PingTypes.UDP:
                        i2 = UDP(dport=dport, sport=sport)
                    elif m == PingTypes.UDPL:
                        i2 = UDP(dport=dport, sport=sport, proto=136)
                    elif m == PingTypes.SCTP:
                        i2 = SCTP(dport=dport, sport=sport)
                    packet = (
                        i /
                        i2 /
                        Raw(load=random_data)   
                    )
                    print(f"> [{packet[ipv].dst}] | [{dport}] | [{packet[Raw].load}]")

                    ans, _ = sr(packet, promisc=True, verbose=False, timeout=args.timeout)

                    for _,a in ans:
                        if Raw in a and a[Raw].load.startswith(b"pm") and a[ipv].src == packet[ipv].dst:
                            print(f"< [{a[ipv].src}] | [{a[ipv].dport}] | [{a[Raw].load}]")
