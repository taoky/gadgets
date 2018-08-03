# FROM i386/debian:stretch
FROM debian:stretch

EXPOSE 12345

# install socat
RUN apt update && apt install -y socat

# configure user & permission
RUN useradd -M -s /usr/sbin/nologin -d /dev/null pwn && mkdir /home/pwn && chown root:root /home/pwn && chmod 1770 /tmp

WORKDIR /home/pwn

COPY exe .
COPY flag .
USER pwn

ENTRYPOINT socat tcp-l:12345,fork,reuseaddr exec:./exe && /bin/bash
