from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.contrib.ospf import OSPF_Hdr

def send(ip, data):
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=34443, ttl=64) /
        OSPF_Hdr() /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)