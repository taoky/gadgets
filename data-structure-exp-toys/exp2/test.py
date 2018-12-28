from huffman import HuffZipFile
from os import listdir
from os.path import isfile, join, splitext
import hashlib
import time


def get_md5(path):
    md5 = hashlib.md5()

    with open(path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)

    return md5.hexdigest()


if __name__ == "__main__":
    for f in listdir("testcase/"):
        path = join("testcase/", f)
        if isfile(path) and splitext(path)[1] != ".bak" and splitext(path)[1] != ".huff":
            print("Start {}".format(f))
            start_time = time.time()
            from_file = open(path, "rb")
            to_file = open(join("testcase/", splitext(f)[0] + ".huff"), "wb")
            zip_file = HuffZipFile(decompress=False, file_stream=from_file)
            zip_file.compress(to_file)
            del zip_file
            # quit()
            print("File {} has finished compressing. Time {}. Decompressing...".format(f, time.time() - start_time))
            start_time = time.time()

            from_file = open(join("testcase/", splitext(f)[0] + ".huff"), "rb")
            to_file = open(path + ".bak", "wb")
            zip_file = HuffZipFile(decompress=True, file_stream=from_file)
            zip_file.decompress(to_file)
            del zip_file

            print("File {} finished decompressing! Time {}.".format(f, time.time() - start_time))
            md5_1 = get_md5(path)
            md5_2 = get_md5(path + ".bak")

            print("Result of {}".format(f))
            if md5_1 != md5_2:
                print("Wrong!")
            else:
                print("Right!")
            print("")

