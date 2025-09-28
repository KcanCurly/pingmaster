from scapy.all import Raw, send
from scapy.layers.inet import IP, TCP

def send_tcp(ip, port, data, flags):
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=34443) /
        TCP(dport=port, sport=44444, flags=flags, seq=1000, ack=1) /
        Raw(load=b)
    )

    # Send packet
    send(packet, verbose=False)