from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.layers.sctp import SCTP

def send(ip, port, data):
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=34443) /
        SCTP(dport=port, sport=44444) /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)