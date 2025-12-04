from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.contrib.igmp import IGMP

def send(ip, data):
    from pingmaster.pingmain import FLOW_ID
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=FLOW_ID, ttl=64) / # For some reason if we don't specify ttl, it will have ttl of 0
        IGMP() /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)