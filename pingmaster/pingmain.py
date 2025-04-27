import argparse
from scapy.all import send
from scapy.layers.inet import IP

def get_broken_version_packet(target, payload, version = 1):
    return IP(dst=target, version=version, ihl=15) / bytes(payload, "utf-8")

def main():
    parser = argparse.ArgumentParser(description="Send a raw IP packet to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    args = parser.parse_args()

    # Create a raw IP packet
    packet = get_broken_version_packet(args.target, "pingmastertest")

    # Send the packet
    send(packet)