from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.layers.ipsec import AH

def send(ip, data):
    from pingmaster.pingmain import FLOW_ID
    b = data.encode("utf-8", errors="replace")
    # Craft TCP packet
    packet = (
        IP(dst=ip, id=FLOW_ID) /
        AH(spi=0x100, seq=1) /
        Raw(load=b)
    )

    # Send packet
    scapy_send(packet, verbose=False)