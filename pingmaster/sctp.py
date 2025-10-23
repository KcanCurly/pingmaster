from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.layers.sctp import SCTP
from scapy.layers.inet6 import IPv6
from pingmaster.type import PingType

class SCTP_Type(PingType):
    def _send_IPv4(self, target, data, port):
        packet = (
            IP(dst=target, id=34443) /
            SCTP(dport=port, sport=44444) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def _send_IPv6(self, target, data, port):
        packet = (
            IPv6(dst=target, fl=34443) /
            SCTP(dport=port, sport=44444) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def send_IPv4(self, executor):
        if executor:
            for port in range(0, 65536):
                executor.submit(self._send_IPv4, self.IPv4_host, self.data, port)
        else:
            for port in range(0, 65536):
                packet = (
                    IP(dst=self.IPv4_host, id=34443) /
                    SCTP(dport=port, sport=44444) /
                    Raw(load=self.data)
                )

                scapy_send(packet, verbose=False)

    def send_IPv6(self, executor):
        if executor:
            for port in range(0, 65536):
                executor.submit(self._send_IPv6, self.IPv6_host, self.data, port)
        else:
            for port in range(0, 65536):
                packet = (
                    IPv6(dst=self.IPv6_host, fl=34443) /
                    SCTP(dport=port, sport=44444) /
                    Raw(load=self.data)
                )

                scapy_send(packet, verbose=False)
