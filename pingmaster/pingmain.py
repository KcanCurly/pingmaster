import argparse
from scapy.all import send
from scapy.layers.inet import IP

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

def main():
    parser = argparse.ArgumentParser(description="Send series of packets to a target host.")
    parser.add_argument("target", help="Target IP address or hostname")
    args = parser.parse_args()
    target = args.target

    # Create a raw IP packet
    send_safe(target)
    send_broken_version_packet(target)
    send_packets_with_all_tos(target)
    send_do_not_fragment(target)