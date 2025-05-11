from scapy.all import sniff, send, Raw
from scapy.layers.inet import IP, UDP
import argparse
import socket
import netifaces as ni

target_payload = b""
send_payload = b""
received = False

def handle_packet(packet):
    if UDP in packet and bytes(packet[UDP].payload) in target_payload:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        print(f"{src_ip}:{src_port} → {dst_ip}:{dst_port}")

        response = IP(dst=src_ip) / UDP(sport=dst_port, dport=src_port) / Raw(load=send_payload)
        send(response, verbose=False)




def server():
    parser = argparse.ArgumentParser(description="Listen to UDP packets using Scapy.")
    parser.add_argument("-i", "--interface", default="eth0", help="Interface to listen to")
    parser.add_argument("-l", "--listen-data", default="Hello from pingmaster", help="Payload/message to listen to")
    parser.add_argument("-l", "--data", default="Hello from pingmaster", help="Payload/message to send")
    args = parser.parse_args()
    global target_payload, send_payload
    target_payload = bytes(args.listen_data, "utf-8")
    send_payload = bytes(args.data, "utf-8")

    sniff(iface=args.interface, filter=f"udp and dst host {ni.ifaddresses(args.interface)[ni.AF_INET][0]['addr']}", prn=handle_packet, store=False)

def client():
    parser = argparse.ArgumentParser(description="Send UDP packets using Scapy.")
    parser.add_argument("-t", "--target", required=True, help="Destination IP address")
    parser.add_argument("-s", "--start-port", type=int, required=True, help="Start of destination port range")
    parser.add_argument("-e", "--end-port", type=int, required=True, help="End of destination port range")
    parser.add_argument("-d", "--data", default="Hello from pingmaster", help="Payload/message to send")
    parser.add_argument("-w", "--wait-for", default=3, help="How much to wait for an answer back (Default = 3)")

    args = parser.parse_args()

    for dst_port in range(args.start_port, args.end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(args.wait_for)

        # Send to server
        sock.sendto(bytes(args.data, "utf-8"), (args.target, dst_port))
        print(f"[>] Sent: {args.data}")

        # Wait for reply
        try:
            data, addr = sock.recvfrom(4096)
            print(f"[<] Reply from {addr}: {data.decode(errors='replace')}")
        except socket.timeout:
            print("[!] No response — possibly one-way UDP communication.")