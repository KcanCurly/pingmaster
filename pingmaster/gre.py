from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP, GRE

def send(ip, data):
    from pingmaster.pingmain import FLOW_ID
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=FLOW_ID) /
        GRE(proto=254) /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)