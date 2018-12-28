import typing
from BitArray_ import BitArray as bitarray
import struct


class Huffman:
    def __init__(self, freq: typing.Optional[typing.List[int]] = None):
        """
        This function initializes the huffman tree with freq as input.
        self.content: a list with lists inside.
            [node_id][0] is its freq (node weight)
            [node_id][1] is its parent id
            [node_id][2] is its left child id
            [node_id][3] is its right child id
        
        :param freq: the frequency of each byte, len(freq) must be 256.
        """

        # assert freq
        self.freq = freq
        # if len(freq) != 256:
        #     assert 0
        self.content = [[0, -1, -1, -1] for i in range(2 * 256 - 1)]
        for i, elem in enumerate(freq):
            if elem:
                self.content[i][0] = elem
        self.root = None
        self.build_huffman()

        self.coding = [None] * 256
        self.build_coding()

    def build_huffman(self):
        """
        This function builds a huffman tree with the existing content of self.content, only for __init__()
        """
        for i in range(256, 2 * 256):
            # 1. select the smallest no-parent nodes, node1.freq <= node2.freq, node1 != node2
            node1 = node2 = None
            for j in range(0, i):
                if self.content[j][1] != -1 or self.content[j][0] == 0:
                    continue
                this_freq = self.content[j][0]
                if node1 is None:
                    node1 = j
                    continue
                node1_freq = self.content[node1][0]

                if node2 is None:
                    node2 = j
                    if node1_freq > self.content[node2][0]:
                        node1, node2 = node2, node1
                    continue
                node2_freq = self.content[node2][0]

                if node1_freq < this_freq < node2_freq:
                    node2 = j
                elif this_freq < node1_freq:
                    node2 = node1
                    node1 = j

            if node1 is None or node2 is None:
                break
            # assert node1 is not None or node2 is not None
            # 2. let's configure node1 & node2
            self.content[node1][1] = self.content[node2][1] = i
            self.content[i][2] = node1
            self.content[i][3] = node2
            self.content[i][0] = self.content[node1][0] + self.content[node2][0]
        for i in range(256, 2 * 256):
            if self.content[i][0] != 0 and self.content[i][1] == -1:
                self.root = i
                return

    def build_coding(self):
        """
        This function builds self.coding according to self.content, only for __init__()
        """
        for i in range(0, 256):
            if self.content[i][0] == 0:
                continue
            coding = ""
            _ = i
            while True:
                parent_id = self.content[i][1]
                if parent_id == -1:
                    break
                if self.content[parent_id][2] == i:
                    # is left child
                    coding += "0"
                elif self.content[parent_id][3] == i:
                    # is right child
                    coding += "1"
                else:
                    # this should never happen
                    assert 0
                i = parent_id
            self.coding[_] = coding[::-1]  # reverse coding string

    def freq_bytecode_export(self) -> bytes:
        ret = bytearray()
        for i in self.freq:
            new_bytes = struct.pack("<I", i)
            for j in range(0, 4):
                ret.append(new_bytes[j])

        return bytes(ret)


class HuffZipFile:
    """
    The structure of huffzip file.
    8 bytes: Magic header "Thuffman"
    4 * 256 bytes: The freq table. byte0 is freq, byte1 is parent, byte2 is left child, byte3 is right child.
        They are all unsigned int.
    1 byte: Unused bits. The decompressed result may have some extra bits, this helps delete them.
    """

    def __init__(self, decompress: bool, file_stream: typing.BinaryIO):
        self.unused_bits = None
        self.freq = []
        self.isDecompress = decompress
        self.huffman = None
        self.file_stream = file_stream
        self.finished = False

        if decompress:
            self.parse_file_header()

    def parse_file_header(self):
        """
        This function checks the integrity of the binary file, and parse file header.
        :return:
        """
        magic = self.file_stream.read(8)
        if magic != b"Thuffman":
            raise TypeError("This file is not a valid huffzip file.")
        content_raw = self.file_stream.read(4 * 256)
        self.unused_bits = self.file_stream.read(1)[0]

        # parse self.content
        for i in range(0, 256):
            new_bytes_int_0 = struct.unpack("<I", content_raw[i * 4: i * 4 + 4])[0]

            self.freq.append(new_bytes_int_0)

    def decompress(self, to_file_stream: typing.BinaryIO):
        """
        a **one-time** decompress
        :param to_file_stream: target file stream (original file)
        :return:
        """
        if not self.isDecompress:
            raise RuntimeError("Mode is not set to \"decompress\"!")
        if self.finished:
            raise RuntimeError("Please create a new class instance to decompress.")
        self.huffman = Huffman(self.freq)
        original_raw = bitarray()
        original_raw.fromfile(self.file_stream)
        if self.unused_bits:
            original_raw.dropbits(self.unused_bits)
        self.file_stream.close()

        decoded_content = original_raw.decode(self.huffman.content, self.huffman.root)
        to_file_stream.write(decoded_content)
        to_file_stream.close()

    def compress(self, to_file_stream: typing.BinaryIO):
        """
        a **one-time** compress
        :param to_file_stream: target file stream (huffzip)
        :return:
        """
        if self.isDecompress:
            raise RuntimeError("Mode is not set to \"compress\"!")
        if self.finished:
            raise RuntimeError("Please create a new class instance to compress.")

        # file stat
        file_content = self.file_stream.read()
        self.file_stream.close()
        freq = [0] * 256
        for i in file_content:
            freq[i] += 1

        self.huffman = Huffman(freq)

        to_file_stream.write(b"Thuffman")
        self.freq = self.huffman.freq_bytecode_export()
        to_file_stream.write(self.freq)

        # start compressing!
        compressed_raw = bitarray()
        compressed_raw.encode(self.huffman.coding, file_content)
        to_file_stream.write(bytes([compressed_raw.buffer_info()]))
        compressed_raw.tofile(to_file_stream)
        to_file_stream.close()


if __name__ == "__main__":
    from ui import Application
    app = Application()
    app.master.title = "Huffman Demo"
    app.mainloop()
