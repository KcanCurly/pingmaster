This project is to send all kinds of packets to test for tunnel and data exfil

# Implemented Protocols
- TCP
- UDP
- SCTP
- ICMP
- AH
- ESP
- GRE
- IGMP
- PIM
- OSPF
- CARP

# On server
```bash
sudo apt install tshark
pipx install "git+https://github.com/kcancurly/pingmaster" 
tshark -i eth0 -f "ip[4:2] == 34443" -w pingmaster.pcap # Press Ctrl+C when finished
pm-analyzer pingmaster.pcap
```

# On client
```bash
sudo apt install python3-dev
pipx install "git+https://github.com/kcancurly/pingmaster" 
sudo $(where pm)  IP
```

# Example Client Result
```bash
sudo $(where pm) 192.168.1.110 -t 100     
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
tshark -i eth0 -f "ip[4:2] == 34443" -w pingmaster.pcap
Capturing on 'eth0'
196870
```
```bash
pm-analyzer pingmaster.pcap 
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