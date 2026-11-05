# Walkthrough - Phishing Infrastructure Investigation

Flag: `QMCTF{rn_l00ks_l1k3_m}`

All commands run inside the analyst container (`docker exec -it qm-analyst bash`).

## 1. Find the look-alike domain (dnstwist)
Generate every look-alike of the real domain, extract the sender domains from
the mail log, and keep only the ones that appear in both lists.
~~~
dnstwist --format list quillmarsh.test > perms.txt
grep -oE 'from=[^ ]+' challenge/mail_gateway.log | cut -d@ -f2 | sort -u > senders.txt
grep -Fxf perms.txt senders.txt
~~~
Result: `quillmarsh.test` (the company's real domain, since dnstwist includes the
original) and `quillrnarsh.test`. The suspect uses a homoglyph: "rn" looks like "m".
The mail log shows it sent three "re-verify your account" emails to staff.

## 2. Find the attacker's server (passive DNS)
~~~
grep quillrnarsh challenge/passive_dns.csv
~~~
Result: `quillrnarsh.test` and `mail.quillrnarsh.test` resolve to `10.10.0.66`,
which is inside the in-scope lab range `10.10.0.0/24`. The domain was first seen
on 2026-10-18, two days before the first phishing email, which is a typical sign of a
newly registered phishing domain.

## 3. Scan the server (Nmap)
~~~
nmap -sV 10.10.0.66
curl http://10.10.0.66/
~~~
Result: only port 80 is open, serving a default page. The page source contains a
hidden comment saying the collector was moved off the standard ports, so scan all ports:
~~~
nmap -p- 10.10.0.66
~~~
Result: port `47820/tcp` is also open. A version scan (`-sV`) on it returns an
unrecognized service whose fingerprint shows the header `Server: QCollector/0.3`.

## 4. Explore the hidden collector
~~~
curl http://10.10.0.66:47820/
curl http://10.10.0.66:47820/status
~~~
Result: `/` lists `/status`, and `/status` reveals `relay: enabled (test with GET /relay)`.

## 5. Capture the relay traffic (tcpdump / Wireshark)
Start recording before triggering the relay:
~~~
tcpdump -i eth0 -w capture.pcap udp &
curl http://10.10.0.66:47820/relay
sleep 6
kill %1
~~~
Result: 11 UDP packets from `10.10.0.66` to port 5140. In Wireshark (filter
`udp.port == 5140`):
- 5 noise packets from source port 39999 with payload `HB`
- 6 fragment packets from source ports 40000-40005, each carrying part of a base64 string
- Packets arrive in random order, and the order changes on every run

Trap: the last fragment (`==`) is only 2 bytes, the same length as the noise packets.
Filtering by packet length drops it. Filter by source port instead.

## 6. Reassemble the flag (Scapy)
Keep fragments from source ports 40000 and above, sort by source port, join, and
base64-decode. See `solve.py`:
~~~
python3 solve.py capture.pcap
~~~
Result:
~~~
fragments found: 6
base64: UU1DVEZ7cm5fbDAwa3NfbDFrM19tfQ==
flag: QMCTF{rn_l00ks_l1k3_m}
~~~
