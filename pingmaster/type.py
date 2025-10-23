class PingType:
    def __init__(self, IPv4_host, IPv6_host, data):
        self.IPv4_host = IPv4_host
        self.IPv6_host = IPv6_host
        self.data = data.encode("utf-8", errors="replace")

    def send(self, executor):
        if self.IPv4_host:
            self.send_IPv4(executor)
        if self.IPv6_host:
            self.send_IPv6(executor)

    def send_IPv4(self, executor):
        print("You are calling send_IPv4 of PingType, override this function on child class")

    def send_IPv6(self, executor):
        print("You are calling send_IPv6 of PingType, override this function on child class")