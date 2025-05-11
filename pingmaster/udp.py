from scapy.all import sniff, send
from scapy.layers.inet import IP, UDP
import argparse

def handle_packet(packet):
    if UDP in packet:
        print(f"{packet[IP].src}:{packet[UDP].sport} → {packet[IP].dst}:{packet[UDP].dport}")
        print(f"Payload: {bytes(packet[UDP].payload)}")

def server():
    sniff(filter="udp", prn=handle_packet, store=False)

def client():
    parser = argparse.ArgumentParser(description="Send UDP packets using Scapy.")
    parser.add_argument("-t", "--target", required=True, help="Destination IP address")
    parser.add_argument("-s", "--start-port", type=int, required=True, help="Start of destination port range")
    parser.add_argument("-e", "--end-port", type=int, required=True, help="End of destination port range")
    parser.add_argument("-d", "--data", default="Hello from Scapy", help="Payload/message to send")

    args = parser.parse_args()

    # Convert payload to bytes
    payload = args.data.encode()

    for dst_port in range(args.start_port, args.end_port + 1):
        packet = IP(dst=args.target) / UDP(dport=dst_port, sport=44444) / payload
        send(packet)