from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP, TCP

def send(ip, port, data, flags):
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=34443) /
        TCP(dport=port, sport=44444, flags=flags, seq=1000, ack=1) /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)