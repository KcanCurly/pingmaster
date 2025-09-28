import argparse
from scapy.all import rdpcap


def analyze(file):
    pkts = rdpcap(file)
    pkts[0].show()

def main():
    parser = argparse.ArgumentParser(description="Analyze pcap.")
    parser.add_argument("file", help="Target filename")
    args = parser.parse_args()
    analyze(args.file)