"""
a bitarray structure, for huffman tree
"""

import typing


class BitArray:
    def __init__(self, input_string : typing.Optional[str] = None):
        self.bitarray = bytearray()
        self.padding_length = 0
        if input_string:
            for i in input_string:
                self.push_bit(i)

    def push_bit(self, bit : str):
        if bit == '1':
            bit = 1
        else:
            bit = 0
        if self.padding_length == 0:
            if bit == 1:
                self.bitarray.append(0b10000000)
            else:
                self.bitarray.append(0)
            self.padding_length = 7
        else:
            self.bitarray[-1] |= bit << (self.padding_length - 1)
            self.padding_length -= 1

    def pop_bit(self):
        if self.padding_length == 7:
            self.bitarray.pop(-1)
            self.padding_length = 0
        else:
            self.bitarray[-1] &= (0b11111111 << (self.padding_length + 1)) & 0b11111111
            self.padding_length += 1

    def fromfile(self, file_stream : typing.BinaryIO):
        self.bitarray = bytearray(file_stream.read())

    def dropbits(self, cnt : int):
        for i in range(cnt):
            self.pop_bit()

    def encode(self, prefix_list : list, content):
        push_bit = self.push_bit
        for i in content:
            insert_bits_str = prefix_list[i]
            # all(map(self.push_bit, insert_bits_str))
            # push_bits(insert_bits_str)
            for j in insert_bits_str:
                push_bit(j)

    def getbit(self, index : int):
        return (self.bitarray[index // 8] & (1 << (7 - index % 8))) >> (7 - index % 8)

    def __repr__(self):
        s = ""
        for i in self.bitarray:
            s += bin(i)[2:].rjust(8, "0")
        if self.padding_length:
            s = s[:-self.padding_length]
        return "BitArray(" + s + ")"

    def decode(self, huffman_tree : typing.List[typing.List[int]], root : int):
        content = bytearray()
        append = content.append
        begin = 0
        tree_tra = root
        length = len(self.bitarray) * 8 - self.padding_length
        while begin <= length:
            if huffman_tree[tree_tra][2] == -1:
                append(tree_tra)
                tree_tra = root
                if begin == length:
                    break
                continue
            this_bit = self.getbit(begin)
            if this_bit == 1:
                tree_tra = huffman_tree[tree_tra][3]
            else:
                tree_tra = huffman_tree[tree_tra][2]

            begin += 1
        return bytes(content)

    def buffer_info(self):
        return self.padding_length

    def tofile(self, file_stream : typing.BinaryIO):
        file_stream.write(self.bitarray)