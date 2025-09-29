from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.contrib.igmp import IGMP

def send(ip, data):
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=34443, ttl=10) /
        IGMP() /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)