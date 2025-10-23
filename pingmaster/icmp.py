from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP, ICMP
from scapy.layers.inet6 import IPv6, _ICMPv6
from pingmaster.type import PingType

class ICMP_Type(PingType):
    def _send_IPv4(self, target, data, t):
        packet = (
            IP(dst=target, id=34443) /
            ICMP(type=t) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def _send_IPv6(self, target, data, t):
        packet = (
            IPv6(dst=target, id=34443) /
            _ICMPv6(type=t) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def send_IPv4(self, executor):
        if executor:
            for t in range(0, 256):
                executor.submit(self._send_IPv4, self.IPv4_host, self.data, t)
        else:
            for t in range(0, 256):
                packet = (
                    IP(dst=self.IPv4_host, id=34443) /
                    ICMP(type=t) /
                    Raw(load=self.data)
                )

                scapy_send(packet, verbose=False)

    def send_IPv6(self, executor):
        if executor:
            for t in range(0, 256):
                executor.submit(self._send_IPv6, self.IPv6_host, self.data, t)
        else:
            for t in range(0, 256):
                packet = (
                    IP(dst=self.IPv6_host, id=34443) /
                    ICMP(type=t) /
                    Raw(load=self.data)
                )

                scapy_send(packet, verbose=False)