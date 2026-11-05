import base64
import sys
from scapy.all import rdpcap, UDP, Raw

pcap = sys.argv[1] if len(sys.argv) > 1 else "relay.pcap"

fragments = {}
for pkt in rdpcap(pcap):
    if UDP in pkt and Raw in pkt and pkt[UDP].dport == 5140:
        sport = pkt[UDP].sport
        if sport >= 40000:
            fragments[sport] = bytes(pkt[Raw].load)

ordered = b"".join(fragments[port] for port in sorted(fragments))

print("fragments found:", len(fragments))
print("base64:", ordered.decode())
print("flag:", base64.b64decode(ordered).decode())
