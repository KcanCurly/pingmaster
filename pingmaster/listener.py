from scapy.all import sniff, Raw
from scapy.layers.inet import IP, TCP
import signal
import sys

# The unique IP ID you want to filter
TARGET_ID = 34443

tcp_syn_succeeded = []

def handle_packet(packet):
    if IP in packet and packet[IP].id == TARGET_ID:
        # print(f"Matched packet from {packet[IP].src} -> {packet[IP].dst}, ID={packet[IP].id}")
        if TCP in packet:
            tcp = packet[TCP]
            flags = tcp.sprintf("%flags%")
            tcp_syn_succeeded.append(tcp.dport)
            # print(f"  TCP sport={tcp.sport} dport={tcp.dport} seq={tcp.seq} ack={tcp.ack} flags={flags}")
            # if Raw in packet:
                #print(f"  payload={bytes(packet[Raw].load)!r}")

def signal_handler(sig, frame):
    print("\n")
    print("You pressed Ctrl+C!")
    print("Results")
    print(tcp_syn_succeeded)
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)

    # Listen on a specific interface, e.g., "eth0"
    sniff(iface="eth0", filter="ip", prn=handle_packet)