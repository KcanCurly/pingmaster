from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP, ICMP
from scapy.layers.inet6 import IPv6, ICMPv6Unknown
from pingmaster.type import PingType
from pingmaster.pingmain import FLOW_ID

MAX_ICMP_TYPE = 256

class ICMP_Type(PingType):
    def _send_IPv4(self, target, data, t):

        packet = (
            IP(dst=target, id=FLOW_ID) /
            ICMP(type=t) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def _send_IPv6(self, target, data, t):

        packet = (
            IPv6(dst=target, fl=FLOW_ID) /
            ICMPv6Unknown(type=t) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def send_IPv4(self, executor):
        if executor:
            for t in range(0, MAX_ICMP_TYPE):
                executor.submit(self._send_IPv4, self.IPv4_host, self.data, t)
        else:
            for t in range(0, MAX_ICMP_TYPE):
                packet = (
                    IP(dst=self.IPv4_host, id=FLOW_ID) /
                    ICMP(type=t) /
                    Raw(load=self.data)
                )

                scapy_send(packet, verbose=False)

    def send_IPv6(self, executor):
        if executor:
            for t in range(0, MAX_ICMP_TYPE):
                executor.submit(self._send_IPv6, self.IPv6_host, self.data, t)
        else:
            for t in range(0, MAX_ICMP_TYPE):
                packet = (
                    IPv6(dst=self.IPv6_host, fl=FLOW_ID) /
                    ICMPv6Unknown(type=t) /
                    Raw(load=self.data)
                )

                scapy_send(packet, verbose=False)