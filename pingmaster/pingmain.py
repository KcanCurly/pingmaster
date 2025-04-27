import argparse
from scapy.all import send
from scapy.layers.inet import IP

def get_broken_version_packet(target, payload, version = 1):
    return IP(dst=target, version=version) / b"PM_VERSION"

def send_packets_with_all_tos(target):
    for tos_value in range(256):  # TOS values range from 0 to 255
        # Create an IP packet with the current TOS value
        ip_packet = IP(dst=target, tos=tos_value) / b"PM_TOS" + bytes([tos_value])
        
        # Send the packet
        send(ip_packet)

def main():
    parser = argparse.ArgumentParser(description="Send a raw IP packet to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    args = parser.parse_args()

    # Create a raw IP packet
    packet = get_broken_version_packet(args.target, "pingmastertest")
    send_packets_with_all_tos(args.target)

    # Send the packet
    send(packet)