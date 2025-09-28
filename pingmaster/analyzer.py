import argparse
from scapy.all import rdpcap
from scapy.layers.inet import IP, TCP
from pingmaster.utility import compress_ranges, create_result

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
                # print(f"  payload={bytes(packet[Raw].load)!r}")

def analyze(file):
    pkts = rdpcap(file)
    for pkt in pkts:
        handle_packet(pkt)

def main():
    parser = argparse.ArgumentParser(description="Analyze pcap.")
    parser.add_argument("file", help="Target filename")
    args = parser.parse_args()
    analyze(args.file)
    create_result("TCP SYN", compress_ranges(tcp_syn_succeeded))