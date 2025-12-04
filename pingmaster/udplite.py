from scapy.all import Raw
from scapy.all import send as scapy_send
from scapy.layers.inet import IP, UDP
from scapy.layers.inet6 import IPv6
from pingmaster.type import PingType

class UDPLite_Type(PingType):
    def _send_IPv4(self, target, data, dport, sport):
        from pingmaster.pingmain import FLOW_ID
        packet = (
            IP(dst=target, id=FLOW_ID, proto=136) /
            UDP(dport=dport, sport=sport) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def _send_IPv6(self, target, data, dport, sport):
        from pingmaster.pingmain import FLOW_ID
        packet = (
            IPv6(dst=target, fl=FLOW_ID, proto=136) /
            UDP(dport=dport, sport=sport) /
            Raw(load=data)
        )

        scapy_send(packet, verbose=False)

    def send_IPv4(self, executor):
        from pingmaster.pingmain import FLOW_ID
        if executor:
            for sport in self.source_ports:
                for dport in self.ports:
                    executor.submit(self._send_IPv4, self.IPv4_host, self.data, dport, sport)
        else:
            for sport in self.source_ports:
                for dport in self.ports:
                    packet = (
                        IP(dst=self.IPv4_host, id=FLOW_ID, proto=136) /
                        UDP(dport=dport, sport=sport) /
                        Raw(load=self.data)
                    )

                    scapy_send(packet, verbose=False)

    def send_IPv6(self, executor):
        from pingmaster.pingmain import FLOW_ID
        if executor:
            for sport in self.source_ports:
                for dport in self.ports:
                    executor.submit(self._send_IPv6, self.IPv6_host, self.data, dport, sport)
        else:
            for sport in self.source_ports:
                for dport in self.ports:
                    packet = (
                        IPv6(dst=self.IPv6_host, fl=FLOW_ID, proto=136) /
                        UDP(dport=dport, sport=sport) /
                        Raw(load=self.data)
                    )

                    scapy_send(packet, verbose=False)

