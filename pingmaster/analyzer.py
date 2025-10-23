import argparse
from scapy.all import rdpcap
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

def handle_packet(packet):
    global ah_s, carp_s, esp_s, gre_s, igmp_s, ospf_s, pim_s
    if (IP in packet and packet[IP].id == TARGET_ID):
        if TCP in packet:
            tcp = packet[TCP]
            tcp_list.append(tcp.dport)
        elif UDP in packet:
            udp = packet[UDP]
            udp_list.append(udp.dport)
        elif SCTP in packet:
            sctp = packet[SCTP]
            sctp_list.append(sctp.dport)
        elif ICMP in packet:
            icmp = packet[ICMP]
            icmp_list.append(icmp.type)
        elif ESP in packet:
            esp_s = True
        elif AH in packet:
            ah_s = True
        elif CARP in packet:
            carp_s = True
        elif IGMP in packet:
            igmp_s = True
        elif OSPF_Hdr in packet:
            ospf_s = True
        elif PIMv2Hdr in packet:
            pim_s = True
    elif IPv6 in packet and packet[IPv6].fl == TARGET_ID:
        if TCP in packet:
            tcp = packet[TCP]
            tcp_list_ipv6.append(tcp.dport)
        elif UDP in packet:
            udp = packet[UDP]
            udp_list_ipv6.append(udp.dport)
        elif SCTP in packet:
            sctp = packet[SCTP]
            sctp_list_ipv6.append(sctp.dport)
        elif ICMP in packet:
            icmp = packet[ICMPv6Unknown]
            icmp_list_ipv6.append(icmp.type)


def analyze(file):
    pkts = rdpcap(file)
    for pkt in pkts:
        handle_packet(pkt)

def main():
    parser = argparse.ArgumentParser(description="Analyze pcap.")
    parser.add_argument("file", help="Target filename")
    args = parser.parse_args()
    analyze(args.file)
    create_result("TCP", compress_ranges(tcp_list))
    create_result("UDP", compress_ranges(udp_list))
    create_result("SCTP", compress_ranges(sctp_list))
    create_result_for_icmp("ICMP", compress_ranges(icmp_list))
    create_result("TCP IPv6", compress_ranges(tcp_list_ipv6))
    create_result("UDP IPv6", compress_ranges(udp_list_ipv6))
    create_result("SCTP IPv6", compress_ranges(sctp_list_ipv6))
    create_result_for_icmp("ICMP IPv6", compress_ranges(icmp_list_ipv6))
    create_result_single("ESP", esp_s)
    create_result_single("AH", ah_s)
    create_result_single("CARP", carp_s)
    create_result_single("GRE", gre_s)
    create_result_single("IGMP", igmp_s)
    create_result_single("OSPF", ospf_s)
    create_result_single("PIM", pim_s)