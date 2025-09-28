from scapy.all import sniff, Raw
from scapy.layers.inet import IP, TCP

# The unique IP ID you want to filter
TARGET_ID = 34443  

def handle_packet(packet):
    if IP in packet and packet[IP].id == TARGET_ID:
        print(f"Matched packet from {packet[IP].src} -> {packet[IP].dst}, ID={packet[IP].id}")
        if TCP in packet:
            tcp = packet[TCP]
            flags = tcp.sprintf("%flags%")
            print(f"  TCP sport={tcp.sport} dport={tcp.dport} seq={tcp.seq} ack={tcp.ack} flags={flags}")
            if Raw in packet:
                print(f"  payload={bytes(packet[Raw].load)!r}")

def main():
    # Listen on a specific interface, e.g., "eth0"
    sniff(iface="eth0", filter="ip", prn=handle_packet)