import os
import socket
from threading import Lock

from utils import log, Timer
from config import WINDOW_SIZE, USE_SR, TIMEOUT


class BTcpConnection:
    def __init__(self, mode, addr, port):
        # Create a TCP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.remote_addr = None

        if mode == 'send':
            self.remote_addr = addr, port
            self.sock.connect(self.remote_addr)
            self.conn = self.sock

        elif mode == 'recv':
            self.sock.bind((addr, port))
            log('info', f"Listening on {addr} port {port}")
            self.sock.listen(1)
            self.conn, self.remote_addr = self.sock.accept()
            log('info', f"Accepted connection from {self.remote_addr[0]} port {self.remote_addr[1]}")
        else:
            raise ValueError(f"Unexpected mode {mode}")

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.conn.close()
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        # set them to None so other code knows
        self.conn = None
        self.sock = None

    def settimeout(self, timeout):
        self.sock.settimeout(timeout)

    def send(self, packet):
        if packet is None:
            packet = b''
        self.conn.sendall(bytes(packet))

    def recv(self):
        header = self.conn.recv(7)
        try:
            packet = BTcpPacket(
                sport=header[0], dport=header[1], seq=header[2], ack=header[3],
                data_len=header[4], win_size=header[5], flag=header[6]
            )
        except IndexError:
            if not header:
                return None
            log('info', "Get malformed packet: {}".format(header))
            raise ValueError
        return BTcpPacket.from_bytes(header + self.conn.recv(packet.data_len))



class BTcpPacket:
    def __init__(self, sport=0, dport=0, seq=0, ack=0, data_len=0, win_size=WINDOW_SIZE, flag=0, data=b""):
        self.sport = sport
        self.dport = dport
        self.seq = seq
        self.ack = ack
        self.data_len = data_len
        self.win_size = win_size
        self.flag = flag
        self.data = data

    def regulate(self):
        # Make sure the values don't stir up
        self.seq &= 0xFF
        self.ack &= 0xFF
        self.data_len &= 0xFF
        self.win_size &= 0xFF
        self.flag &= 1  # Could be 0xFF, but we only need "retransmission" flag

    def __bytes__(self):
        self.regulate()
        return bytes([
            self.sport, self.dport, self.seq, self.ack,
            self.data_len, self.win_size, self.flag,
        ]) + bytes(self.data)

    @staticmethod
    def from_bytes(data):
        if not data:
            return None
        packet = BTcpPacket(
            sport=data[0], dport=data[1], seq=data[2], ack=data[3],
            data_len=data[4], win_size=data[5], flag=data[6], data=data[7:]
        )
        return packet

    def __repr__(self):
        if len(self.data) > 1:
            s = f"<{len(self.data)} bytes>"
        elif len(self.data) == 0:
            s = "<empty>"
        else:
            s = "<1 byte>"
        return f"BTcpPacket(seq={self.seq}, ack={self.ack}, win_size={self.win_size}, flag={self.flag}, data={s})"


def send(data, addr, port):
    conn = BTcpConnection('send', addr, port)

    chunks = [data[x * 64:x * 64 + 64] for x in range((len(data) - 1) // 64 + 1)]
    packets = [BTcpPacket(
                seq=i & 0xFF, data=chunk, dport=port & 0xFF, sport=233, data_len=len(chunk)
            ) for i, chunk in enumerate(chunks)]

    window_start = 0

    timers = [None] * 256
    lock = Lock()

    log('info', 'we have %d chunks' % len(chunks))

    def sendp(i, flag):
        log('info', 'sending %d.' % i)
        with lock:
            packets[i].flag = flag
            conn.send(packets[i])
    
    for i in range(WINDOW_SIZE):
        if i < len(packets):
            if not USE_SR:
                log('info', 'sending packets[%d]' % i)
                conn.send(packets[i])
            else:
                timers[i] = Timer(TIMEOUT, sendp, args=(i,))
                timers[i].start()
    window_end = min(WINDOW_SIZE, len(packets))

    if not USE_SR:
        # GBN
        while window_start < len(packets):
            conn.settimeout(TIMEOUT)  # 10 ms
            try:
                while True:
                    try:
                        p = conn.recv()
                        break
                    except ValueError:
                        continue
                ack = p.ack
                while ack < window_start:
                    ack += 0xFF + 1
                if ack < window_end:
                    offset = ack - window_start + 1
                    log('info', '(ack = %d, wstart = %d, wend = %d) send window += offset %d' % (p.ack, window_start, window_end, offset))
                    
                    for i in range(window_end, min(window_end + offset, len(packets))):
                        conn.send(packets[i])
                    window_end = min(window_end + offset, len(packets))
                    window_start = min(window_start + offset, len(packets))
                else:
                    log('info', 'get ack = {} ({}), but window_start = {}. Packet: {}'.format(p.ack, ack, window_start, p))
            except socket.timeout:
                log('info', "Timeout occurred in send().")
                for i in range(window_start, window_end):
                    packets[i].flag = 1
                    conn.send(packets[i])
    else:
        # SR
        
        while window_start < len(packets):
            conn.settimeout(TIMEOUT)
            try:
                while True:
                    try:
                        with lock:
                            p = conn.recv()
                        break
                    except ValueError:
                        continue
                ack = p.ack
                log('info', 'get ack %d' % p.ack)
                if timers[p.ack]:
                    timers[p.ack].cancel()
                    timers[p.ack] = None
                while ack < window_start:
                    ack += 0xFF + 1
                if ack < window_end:
                    packets[ack].ack = 1  # not used, and won't be sent again
                    if ack == window_start:
                        while packets[window_start].ack:
                            window_start += 1
                            if window_end < len(packets):
                                log('info', 'sending packets[%d]' % window_end)
                                timers[window_end & 0xFF] = Timer(TIMEOUT, sendp, args=(window_end,))
                                timers[window_end & 0xFF].start()
                            else:
                                log('info', 'no more packets need to be sent, waiting for the last acks')
                            window_end += 1
                            if window_start == len(packets):
                                break
                else:
                    log('info', 'get ack = {} ({}), but window_start = {}. Packet: {}'.format(p.ack, ack, window_start, p))
            except socket.timeout:
                log('info', "Timeout occurred in send() when window_start = {}.".format(window_start))
                


    log('info', 'send() finished his work.')
    return


def recv(addr, port):
    conn = BTcpConnection('recv', addr, port)

    data = b''  # Nothing received yet

    if not USE_SR:
        # GBN
        latest_ack_no = -1
        latest_ack_packet = None
        while True:
            try:
                p = conn.recv()
            except ValueError:
                continue
            if p is None:  # No more packets
                break
            if p.seq == (latest_ack_no + 1) & 0xFF:
                log('info', 'get seq = %d, ok!' % p.seq)
                data += p.data
                latest_ack_no = p.seq
                latest_ack_packet = BTcpPacket(
                        sport=port & 0xFF,
                        dport=p.sport,
                        ack=latest_ack_no,
                    )
                conn.send(latest_ack_packet)
            elif latest_ack_packet is not None:
                log('info', 'get seq = {}, but latest_ack_no = {}. Packet: {}'.format(p.seq, latest_ack_no, p))
                conn.send(latest_ack_packet)
    else:
        # SN
        recvbase = 0
        recvend = WINDOW_SIZE
        dataset = [None] * 256

        while True:
            try:
                p = conn.recv()
            except ValueError:
                continue
            if p is None:  # No more packets
                break
            if recvbase <= p.seq < recvend or recvend < recvbase <= p.seq or p.seq < recvend <= recvbase:
                log('info', 'get seq = %d, ok!' % p.seq)
                conn.send(BTcpPacket(
                        sport=port & 0xFF,
                        dport=p.sport,
                        ack=p.seq,
                    ))
                if dataset[p.seq]:
                    log('info', 'duplicate packet %d' % p.seq)
                dataset[p.seq] = p.data
                if p.seq == recvbase:
                    while dataset[recvbase]:
                        data += dataset[recvbase]
                        dataset[recvbase] = None
                        recvbase = (recvbase + 1) % 0x100
                        recvend = (recvend + 1) % 0x100
            elif (recvbase - WINDOW_SIZE) & 0xFF <= p.seq <= (recvbase - 1) & 0xFF or \
                p.seq <= (recvbase - 1) & 0xFF <= (recvbase - WINDOW_SIZE) & 0xFF or \
                (recvbase - 1) & 0xFF <= (recvbase - WINDOW_SIZE) & 0xFF <= p.seq:
                log('info', 'get seq = %d in [rcvbase-N, rcvbase-1], recvbase = %d, resend ACK.' % (p.seq, recvbase))
                conn.send(BTcpPacket(
                        sport=port & 0xFF,
                        dport=p.sport,
                        ack=p.seq,
                    ))
            else:
                log('info', '{} ignored, recvbase = {}'.format(p, recvbase))

    log('info', 'recv() finished his work.')
    return data