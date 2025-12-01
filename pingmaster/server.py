from scapy.all import *
from scapy.layers.inet import IP, UDP, TCP
from scapy.layers.inet6 import IPv6
from scapy.all import send
from scapy.layers.sctp import SCTP
import random
import string

TARGET_FLOW = 34443

chars = string.ascii_letters + string.digits

def handle(pkt):
    if IP in pkt and pkt[IP].id == TARGET_FLOW:
        send_pkt = None
        print(f"< [{pkt[IP].src}] | [{pkt[IP][Packet][Raw].load}]")
        random_data = bytes(''.join(random.choice(chars) for _ in range(10)), "utf-8")
        if TCP in pkt[IP]:
            send_pkt = IP(src=pkt[IP].dst, dst=pkt[IP].src)/TCP(sport=pkt[IP][TCP].dport, dport=pkt[IP][TCP].sport, flags="A", seq=pkt[IP][TCP].ack, ack=pkt[IP][TCP].seq + 1)/Raw(load=random_data)
        elif UDP in pkt[IP]:
            send_pkt = IP(src=pkt[IP].dst, dst=pkt[IP].src)/UDP(sport=pkt[IP][UDP].dport, dport=pkt[IP][UDP].sport)/Raw(load=random_data)
        elif SCTP in pkt[IP]:
            send_pkt = IP(src=pkt[IP].dst, dst=pkt[IP].src)/SCTP(sport=pkt[IP][SCTP].dport, dport=pkt[IP][SCTP].sport)/Raw(load=random_data)
        else:
            send_pkt = IP(src=pkt[IP].dst, dst=pkt[IP].src)/pkt[IP][Packet]/Raw(load=random_data)

        send(send_pkt, verbose=False)
        print(f"> [{pkt[IP].src}] | [{send_pkt[IP][Packet][Raw].load}]")


    elif IPv6 in pkt and pkt[IPv6].fl == TARGET_FLOW:
        send_pkt = None
        print(f"> [{pkt[IPv6].src}] | [{pkt[IPv6][Packet][Raw].load}]")
        random_data = bytes(''.join(random.choice(chars) for _ in range(10)), "utf-8")
        if TCP in pkt[IPv6]:
            send_pkt = IPv6(src=pkt[IPv6].dst, dst=pkt[IPv6].src)/TCP(sport=pkt[IPv6][TCP].dport, dport=pkt[IPv6][TCP].sport, flags="A", seq=pkt[IPv6][TCP].ack, ack=pkt[IPv6][TCP].seq + 1)/Raw(load=random_data)
        elif UDP in pkt[IPv6]:
            send_pkt = IPv6(src=pkt[IPv6].dst, dst=pkt[IPv6].src)/UDP(sport=pkt[IPv6][UDP].dport, dport=pkt[IPv6][UDP].sport)/Raw(load=random_data)
        elif SCTP in pkt[IPv6]:
            send_pkt = IPv6(src=pkt[IPv6].dst, dst=pkt[IPv6].src)/SCTP(sport=pkt[IPv6][SCTP].dport, dport=pkt[IPv6][SCTP].sport)/Raw(load=random_data)
        else:
            send_pkt = IPv6(src=pkt[IPv6].dst, dst=pkt[IPv6].src)/pkt[IPv6][Packet]/Raw(load=random_data)

        send(send_pkt, verbose=False)
        print(f"> [{pkt[IPv6].src}] | [{send_pkt[IPv6][Packet][Raw].load}]")

def main():
    sniff(filter="ip or ip6", prn=handle)