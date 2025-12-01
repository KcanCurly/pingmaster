from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.inet6 import IPv6
import argparse

from pingmaster.pingmain import PingTypes, MAX_ICMP_TYPES, MAX_PORT
from pingmaster.tcp import TCP_Type

TARGET_FLOW = 34443

chars = string.ascii_letters + string.digits

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("--ipv4-target", help="Target IPv4 address")
    parser.add_argument("--ipv6-target", help="Target IPv4 address")
    parser.add_argument("--threads", type=int, default=10, help="Amount of threads. (Default: 10)")
    parser.add_argument("--timeout", type=int, default=3, help="Amount of timeout. (Default: 3)")
    parser.add_argument("-m", "--method", required=False, choices=[m.value for m in PingTypes])
    args = parser.parse_args()


    if os.geteuid() != 0:
        print("Run as root, exiting")

    for port in range(0, 65536):
        random_data = bytes(''.join(random.choice(chars) for _ in range(10)), "utf-8")
        packet = (
            IP(dst=args.ipv4_target, id=34443) /
            TCP(dport=port, sport=44444, flags="S") /
            Raw(load=random_data)
        )
        print(f"> [{packet[IP].dst}] | [{packet[IP][Packet][Raw].load}]")

        incoming_packet = sr1(packet, verbose=False, timeout=args.timeout)
        if incoming_packet:
            print(f"< [{incoming_packet[IP].src}] | [{incoming_packet[IP][Packet][Raw].load}]")

