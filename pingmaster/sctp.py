from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP
from scapy.layers.sctp import SCTP
from scapy.layers.inet6 import IPv6
from pingmaster.type import PingType
from pingmaster.pingmain import FLOW_ID

class SCTP_Type(PingType):
    def _send_IPv4(self, target, data, dport, sport):
        packet = (
            IP(dst=target, id=FLOW_ID) /
            SCTP(dport=dport, sport=sport) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def _send_IPv6(self, target, data, dport, sport):
        packet = (
            IPv6(dst=target, fl=FLOW_ID) /
            SCTP(dport=dport, sport=sport) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def send_IPv4(self, executor):
        if executor:
            for sport in self.source_ports:
                for dport in self.ports:
                    executor.submit(self._send_IPv4, self.IPv4_host, self.data, dport, sport)
        else:
            for sport in self.source_ports:
                for dport in self.ports:
                    packet = (
                        IP(dst=self.IPv4_host, id=FLOW_ID) /
                        SCTP(dport=dport, sport=sport) /
                        Raw(load=self.data)
                    )

                    scapy_send(packet, verbose=False)

    def send_IPv6(self, executor):
        if executor:
            for sport in self.source_ports:
                for dport in self.ports:
                    executor.submit(self._send_IPv6, self.IPv6_host, self.data, dport, sport)
        else:
            for sport in self.source_ports:
                for dport in self.ports:
                    packet = (
                        IPv6(dst=self.IPv6_host, fl=FLOW_ID) /
                        SCTP(dport=dport, sport=sport) /
                        Raw(load=self.data)
                    )

                    scapy_send(packet, verbose=False)
