import argparse
from scapy.all import rdpcap, Raw
from scapy.layers.inet6 import IPv6, ICMPv6Unknown
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.sctp import SCTP
from scapy.layers.ipsec import AH, ESP
from scapy.contrib.carp import CARP
from scapy.contrib.igmp import IGMP
from scapy.contrib.ospf import OSPF_Hdr
from scapy.contrib.pim import PIMv2Hdr
from pingmaster.utility import compress_ranges, create_result, create_result_single, create_result_for_icmp

# The unique IP ID you want to filter
TARGET_ID = 34443

tcp_list = []
udp_list = []
sctp_list = []
icmp_list = []
tcp_list_ipv6 = []
udp_list_ipv6 = []
sctp_list_ipv6 = []
icmp_list_ipv6 = []
ah_s = False
carp_s = False
esp_s = False
gre_s = False
igmp_s = False
ospf_s = False
pim_s = False

def handle_packet(packet, data):
    global ah_s, carp_s, esp_s, gre_s, igmp_s, ospf_s, pim_s
    data = bytes(data, "utf-8")
    if IP in packet and packet[IP].id == TARGET_ID:
        if TCP in packet and Raw in packet[TCP] and packet[TCP][Raw].load == data:
            tcp_list.append(packet[TCP].dport)
        elif UDP in packet and Raw in packet[UDP] and packet[UDP][Raw].load == data:
            udp_list.append(packet[UDP].dport)
        elif SCTP in packet and Raw in packet[SCTP] and packet[SCTP][Raw].load == data:
            sctp_list.append(packet[SCTP].dport)
        elif ICMP in packet and Raw in packet[ICMP] and packet[ICMP][Raw].load == data:
            icmp_list.append(packet[ICMP].type)
        elif ESP in packet and Raw in packet[ESP] and packet[ESP][Raw].load == data:
            esp_s = True
        elif AH in packet and Raw in packet[AH] and packet[AH][Raw].load == data:
            ah_s = True
        elif CARP in packet and Raw in packet[CARP] and packet[CARP][Raw].load == data:
            carp_s = True
        elif IGMP in packet and Raw in packet[IGMP] and packet[IGMP][Raw].load == data:
            igmp_s = True
        elif OSPF_Hdr in packet and Raw in packet[OSPF_Hdr] and packet[OSPF_Hdr][Raw].load == data:
            ospf_s = True
        elif PIMv2Hdr in packet and Raw in packet[PIMv2Hdr] and packet[PIMv2Hdr][Raw].load == data:
            pim_s = True
    elif IPv6 in packet and packet[IPv6].fl == TARGET_ID:
        if TCP in packet and Raw in packet[TCP] and packet[TCP][Raw].load == data:
            tcp_list_ipv6.append(packet[TCP].dport)
        elif UDP in packet and Raw in packet[UDP] and packet[UDP][Raw].load == data:
            udp_list_ipv6.append(packet[UDP].dport)
        elif SCTP in packet and Raw in packet[SCTP] and packet[SCTP][Raw].load == data:
            sctp_list_ipv6.append(packet[SCTP].dport)
        elif ICMP in packet and Raw in packet[ICMP] and packet[ICMP][Raw].load == data:
            icmp_list_ipv6.append(packet[ICMPv6Unknown].type)


def analyze(file, data):
    pkts = rdpcap(file)
    for pkt in pkts:
        try:
            handle_packet(pkt, data)
        except Exception as e:
            print(e)
            pass

def main():
    parser = argparse.ArgumentParser(description="Analyze pcap.")
    parser.add_argument("file", help="Target filename")
    parser.add_argument("data", help="Data to look for in packets")
    args = parser.parse_args()
    analyze(args.file, args.data)
    if tcp_list: create_result("TCP", compress_ranges(tcp_list))
    if udp_list: create_result("UDP", compress_ranges(udp_list))
    if sctp_list: create_result("SCTP", compress_ranges(sctp_list))
    if icmp_list: create_result_for_icmp("ICMP", compress_ranges(icmp_list))
    if tcp_list_ipv6: create_result("TCP IPv6", compress_ranges(tcp_list_ipv6))
    if udp_list_ipv6: create_result("UDP IPv6", compress_ranges(udp_list_ipv6))
    if sctp_list_ipv6: create_result("SCTP IPv6", compress_ranges(sctp_list_ipv6))
    if icmp_list_ipv6: create_result_for_icmp("ICMP IPv6", compress_ranges(icmp_list_ipv6))
    if esp_s: create_result_single("ESP", esp_s)
    if ah_s: create_result_single("AH", ah_s)
    if carp_s: create_result_single("CARP", carp_s)
    if gre_s: create_result_single("GRE", gre_s)
    if igmp_s: create_result_single("IGMP", igmp_s)
    if ospf_s: create_result_single("OSPF", ospf_s)
    if pim_s: create_result_single("PIM", pim_s)