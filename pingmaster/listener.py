from scapy.all import sniff
from scapy.layers.inet import IP

# The unique IP ID you want to filter
TARGET_ID = 34443  

def handle_packet(packet):
    if IP in packet:
        if packet[IP].id == TARGET_ID:
            print(f"Matched packet from {packet[IP].src} -> {packet[IP].dst}, ID={packet[IP].id}")

def main():
    # Listen on a specific interface, e.g., "eth0"
    sniff(iface="eth0", filter="ip", prn=handle_packet)