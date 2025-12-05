This project is to send all kinds of packets to test for tunnel and data exfil

# Implemented Protocols
- TCP
- UDP
- UDPLite
- SCTP
- ICMP
- AH
- ESP
- GRE
- IGMP
- PIM
- OSPF
- CARP

# Hint
Try using --source-port 25 (SMTP) 53 (DNS) 485 (SMTP) 587 (SMTP) 2525 (SMTP)

# On server
```bash
sudo apt update && sudo apt install tshark pipx python3-pip iptables
sudo iptables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
sudo iptables -A OUTPUT -p icmp -j DROP
sudo ip6tables -A OUTPUT -p tcp --tcp-flags RST RST -j DROP
sudo ip6tables -A OUTPUT -p icmpv6 -j DROP
pip install netifaces --break-system-packages
pipx install "git+https://github.com/kcancurly/pingmaster" 
sudo tcpdump -i eth0 'ip[4:2] = 34443 or (ip6 && (((ip6[1] & 0x0F) << 16) | (ip6[2] << 8) | ip6[3]) == 34443)' -w pingmaster.pcap
# Press Ctrl+C when finished
pm-analyzer pingmaster.pcap pingmaster
```

# On client
```bash
sudo apt install python3-dev
pipx install "git+https://github.com/kcancurly/pingmaster" 
sudo $(where pm) --ipv4 IPV4 --ipv6 IPV6
```

# Example Client Result
```bash
sudo $(where pm) --ipv4 192.168.1.110 -t 50     
```
```                        
WARNING: CARP overwrites VRRP !
Starting TCP PING
Date: 2025-09-30 20:24:11.446319
===================
===================
ENDING TCP PING
Date: 2025-09-30 20:27:02.827215
TCP PING took around 2 minutes and 51 seconds
Starting UDP PING
Date: 2025-09-30 20:27:02.828763
===================
===================
ENDING UDP PING
Date: 2025-09-30 20:29:32.868312
UDP PING took around 2 minutes and 30 seconds
Starting SCTP PING
Date: 2025-09-30 20:29:32.868747
===================
===================
ENDING SCTP PING
Date: 2025-09-30 20:31:59.754148
SCTP PING took around 2 minutes and 26 seconds
Starting ICMP PING
Date: 2025-09-30 20:31:59.754451
===================
===================
ENDING ICMP PING
Date: 2025-09-30 20:32:00.295917
ICMP PING took around 0 minutes and 0 seconds
Starting AH PING
Date: 2025-09-30 20:32:00.296206
===================
===================
ENDING AH PING
Date: 2025-09-30 20:32:00.330359
AH PING took around 0 minutes and 0 seconds
Starting ESP PING
Date: 2025-09-30 20:32:00.330447
===================
===================
ENDING ESP PING
Date: 2025-09-30 20:32:00.370454
ESP PING took around 0 minutes and 0 seconds
Starting GRE PING
Date: 2025-09-30 20:32:00.370536
===================
===================
ENDING GRE PING
Date: 2025-09-30 20:32:00.418283
GRE PING took around 0 minutes and 0 seconds
Starting IGMP PING
Date: 2025-09-30 20:32:00.418362
===================
===================
ENDING IGMP PING
Date: 2025-09-30 20:32:00.458738
IGMP PING took around 0 minutes and 0 seconds
Starting PIM PING
Date: 2025-09-30 20:32:00.458820
===================
===================
ENDING PIM PING
Date: 2025-09-30 20:32:00.494702
PIM PING took around 0 minutes and 0 seconds
Starting OSPF PING
Date: 2025-09-30 20:32:00.494874
===================
===================
ENDING OSPF PING
Date: 2025-09-30 20:32:00.526252
OSPF PING took around 0 minutes and 0 seconds
Starting CARP PING
Date: 2025-09-30 20:32:00.526330
===================
===================
ENDING CARP PING
Date: 2025-09-30 20:32:00.578814
CARP PING took around 0 minutes and 0 seconds
```

# Example Server Result
```bash
pm-analyzer pingmaster.pcap pingmaster
```
```
WARNING: CARP overwrites VRRP !
===============
TEST: TCP
===============
Ports succeeded:
    1-65535

===============
TEST: UDP
===============
Ports succeeded:
    1-65535

===============
TEST: SCTP
===============
Ports succeeded:
    1-65535

===============
TEST: ICMP
===============
Types succeeded:
    1-255

===============
TEST: ESP
===============
Succes: True

===============
TEST: AH
===============
Succes: True

===============
TEST: CARP
===============
Succes: False

===============
TEST: GRE
===============
Succes: False

===============
TEST: IGMP
===============
Succes: False

===============
TEST: OSPF
===============
Succes: True

===============
TEST: PIM
===============
Succes: True
```

# Access Test
You can use pm-client and pm-server to test access if its one way or two way
Client sends packets with chosen packet type and adds Raw packet with random value starting with "pm-", when server detects it, it prints the value and sends same packet type with random value starting with "pm-" as well if client detects it, it prints the value. This can help you figure out if access is one way or two way.

# Example Client Result
```bash
sudo $(which pm-client) --ipv4 192.168.10.101 -p 100-105        
,WARNING: CARP overwrites VRRP !
> [192.168.10.101] | [100] | [b'pm-YSl3l']
< [192.168.10.101] | [44444] | [b'pm-klfQ8']
> [192.168.10.101] | [101] | [b'pm-oEkn5']
< [192.168.10.101] | [44444] | [b'pm-Wcrbb']
> [192.168.10.101] | [102] | [b'pm-8eZXS']
< [192.168.10.101] | [44444] | [b'pm-Q8jKZ']
> [192.168.10.101] | [103] | [b'pm-l6Xyw']
< [192.168.10.101] | [44444] | [b'pm-GtgaX']
> [192.168.10.101] | [104] | [b'pm-rMtQW']
< [192.168.10.101] | [44444] | [b'pm-vFkcx']
> [192.168.10.101] | [105] | [b'pm-tDmYu']
< [192.168.10.101] | [44444] | [b'pm-HBqpG']
```

# Example Server Result
```bash
sudo $(where pm-server)
< [192.168.10.100] | [b'pm-YSl3l']
> [192.168.10.101] | [b'pm-klfQ8']
< [192.168.10.100] | [b'pm-oEkn5']
> [192.168.10.101] | [b'pm-Wcrbb']
< [192.168.10.100] | [b'pm-8eZXS']
> [192.168.10.101] | [b'pm-Q8jKZ']
< [192.168.10.100] | [b'pm-l6Xyw']
> [192.168.10.101] | [b'pm-GtgaX']
< [192.168.10.100] | [b'pm-rMtQW']
> [192.168.10.101] | [b'pm-vFkcx']
< [192.168.10.100] | [b'pm-tDmYu']
> [192.168.10.101] | [b'pm-HBqpG']
```