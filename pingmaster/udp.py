from scapy.all import sniff, send, Raw
from scapy.layers.inet import IP, UDP
import argparse
import socket
import time

target_payload = b""

def handle_packet(packet):
    print(bytes(packet[UDP].payload))
    if UDP in packet and bytes(packet[UDP].payload) in target_payload:
        print(f"{packet[IP].src}:{packet[UDP].sport} → {packet[IP].dst}:{packet[UDP].dport}")
        print(f"Payload: {bytes(packet[UDP].payload)}")


def server():
    parser = argparse.ArgumentParser(description="Listen to UDP packets using Scapy.")
    parser.add_argument("-d", "--data", default="Hello from pingmaster", help="Payload/message to listen to")
    args = parser.parse_args()
    global target_payload
    target_payload = bytes(args.data, "utf-8")
    sniff(filter="udp", prn=handle_packet, store=False)

def client():
    parser = argparse.ArgumentParser(description="Send UDP packets using Scapy.")
    parser.add_argument("-t", "--target", required=True, help="Destination IP address")
    parser.add_argument("-s", "--start-port", type=int, required=True, help="Start of destination port range")
    parser.add_argument("-e", "--end-port", type=int, required=True, help="End of destination port range")
    parser.add_argument("-d", "--data", default="Hello from pingmaster", help="Payload/message to send")

    args = parser.parse_args()

    for dst_port in range(args.start_port, args.end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)  # Timeout if no reply

        # Send to server
        sock.sendto(bytes(args.data, "utf-8"), (args.target, dst_port))
        print(f"[>] Sent: {args.data}")

        # Wait for reply
        try:
            data, addr = sock.recvfrom(4096)
            print(f"[<] Reply from {addr}: {data.decode(errors='replace')}")
        except socket.timeout:
            print("[!] No response — possibly one-way UDP communication.")