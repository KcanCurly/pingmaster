from scapy.all import *
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.inet6 import IPv6
from scapy.all import send
from scapy.layers.sctp import SCTP
import random
import string
import netifaces

TARGET_FLOW = 34443

chars = string.ascii_letters + string.digits

def handle(pkt):

    if (IP in pkt and pkt[IP].id == TARGET_FLOW and Raw in pkt and pkt[Raw].load.startswith(b"pm")) or (IPv6 in pkt and pkt[IPv6].fl == TARGET_FLOW and Raw in pkt and pkt[Raw].load.startswith(b"pm")):
        t = IPv6 if pkt.haslayer(IPv6) else IP
        send_pkt = None
        print(f"< [{pkt[t].src}] | [{pkt[Raw].load}]")
        random_data = b"pm-" + bytes(''.join(random.choice(chars) for _ in range(5)), "utf-8")
        if TCP in pkt[t]:
            send_pkt = t(src=pkt[t].dst, dst=pkt[t].src, id=TARGET_FLOW)/TCP(sport=pkt[t][TCP].dport, dport=pkt[t][TCP].sport, flags="A", seq=pkt[t][TCP].ack, ack=pkt[t][TCP].seq + 1)/Raw(load=random_data)
        elif UDP in pkt[t]:
            send_pkt = t(src=pkt[t].dst, dst=pkt[t].src, id=TARGET_FLOW)/UDP(sport=pkt[t][UDP].dport, dport=pkt[t][UDP].sport, proto=pkt[t].proto)/Raw(load=random_data)
        elif SCTP in pkt[t]:
            send_pkt = t(src=pkt[t].dst, dst=pkt[t].src, id=TARGET_FLOW)/SCTP(sport=pkt[t][SCTP].dport, dport=pkt[t][SCTP].sport)/Raw(load=random_data)
        else:
            send_pkt = t(src=pkt[t].dst, dst=pkt[t].src, id=TARGET_FLOW)/pkt[t][Packet]/Raw(load=random_data)

        send(send_pkt, verbose=False)
        print(f"> [{send_pkt[t].dst}] | [{send_pkt[Raw].load}]")

def get_my_ips():
    ips4 = []
    ips6 = []

    for iface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(iface)

        if netifaces.AF_INET in addrs:
            for a in addrs[netifaces.AF_INET]:
                ips4.append(a["addr"])

        if netifaces.AF_INET6 in addrs:
            for a in addrs[netifaces.AF_INET6]:
                # remove %eth0 zone index
                ips6.append(a["addr"].split("%")[0])

    return ips4, ips6




def main():
    if os.geteuid() != 0:
        print("Run as root, exiting")
        os._exit(1)
    my_ipv4, my_ipv6 = get_my_ips()

    bpf_parts = []

    for ip in my_ipv4:
        bpf_parts.append(f"ip dst host {ip}")

    for ip6 in my_ipv6:
        bpf_parts.append(f"ip6 dst {ip6}")
    
    bpf_filter = " or ".join(bpf_parts)

    sniff(filter=f"(ip or ip6) and ({bpf_filter})", prn=handle)