This project is to send all kinds of pings to test for tunnel and data exfil tests

# On server
We use tshark to capture the IP packets with given ID on given interface
```bash
sudo apt install tshark
tshark -i INTERFACE -f "ip[4:2] == ID" -w pingmaster.pcap
```

# On client
```bash
pipx install "git+https://github.com/kcancurly/pingmaster" 
pm IP
```