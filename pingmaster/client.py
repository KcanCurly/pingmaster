from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.inet6 import IPv6
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
    help="Destination ports or ranges (e.g., 80 443 1000-2000)"
    )
    parser.add_argument(
    "--source-port",
    nargs="+",
    action="extend",
    default=[44444],
    help="Source ports or ranges (e.g., 80 443 1000-2000)"
    )
    parser.add_argument("--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    parser.add_argument("--timeout", type=int, default=3, help="Amount of timeout to wait for packets. (Default: 3)")
    parser.add_argument("-m", "--method", required=False, choices=[m.value for m in PingTypes])
    args = parser.parse_args()
    if not (args.ipv4 or args.ipv6):
        parser.error("You must specify at least --ipv4 or --ipv6")


    if args.ports:
        ports = [parse_ports(a) for a in args.ports]
    else:
        ports = [i for i in range(0, MAX_PORT)]

    if os.geteuid() != 0:
        print("Run as root, exiting")

    signal.signal(signal.SIGINT, signal_handler)

    for sport in args.source_port:
        for dport in ports:
            
            random_data = b"pm-" + bytes(''.join(random.choice(chars) for _ in range(5)), "utf-8")
            packet = (
                IP(dst=args.ipv4, id=FLOW_ID) /
                TCP(dport=dport, sport=sport, flags="S") /
                Raw(load=random_data)
            )
            print(f"> [{packet[IP].dst}] | [{packet[TCP].dport}] | [{packet[Raw].load}]")

            ans, _ = sr(packet, verbose=False, timeout=args.timeout)

            for _,a in ans:
                if Raw in a and a[Raw].load.startswith(b"pm") and a[IP].src == packet[IP].dst:
                    print(f"< [{a[IP].src}] | [{a[IP].dport}] | [{a[Raw].load}]")


