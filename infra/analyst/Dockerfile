FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    dnstwist nmap tcpdump python3-scapy curl iproute2 iputils-ping ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /home/analyst
CMD ["bash"]
