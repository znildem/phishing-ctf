\# Phishing Infrastructure Investigation



\## Scenario

You are a security analyst at \*\*Quillmarsh Logistics\*\*, a fictional freight company.



Several employees reported emails that looked like they came from the IT department,

asking them to "re-verify" their accounts. The Security team suspects an attacker has

registered a domain that looks like the company's own domain.



\## What you know

Quillmarsh's legitimate domain is: `quillmarsh.test`



You have been given an export of recent sender domains from the company's mail gateway:

`mail\_gateway.log`

The Threat Intel team also provided a passive DNS export for domains seen in recent traffic:
`passive_dns.csv`

The CTF lab network in scope is: `10.10.0.0/24`



\## Your task

1\. Find the look-alike domain the attacker is using.

2\. Follow the evidence to investigate the attacker's infrastructure.

3\. Recover the flag.



Flag format: `QMCTF{...}`



\## Rules

\- Only scan and interact with systems inside the provided CTF environment.

\- Do not scan or contact any external systems.



\## Suggested tools

dnstwist, Nmap, Wireshark, Scapy

