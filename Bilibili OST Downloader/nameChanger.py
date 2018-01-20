import os
import re

f = open("list.txt")
s = f.read()

s = s.strip().split("\n")

flist = [i for i in os.listdir(".") if os.path.splitext(i)[1] == ".mp3"]

for i in flist:
    num = re.findall("\d+", os.path.splitext(i)[0])[-1]
    # bugs!
    for j in s:
        nums = re.findall("\d+", j)[0]
        if num == nums:
            os.rename(i, j + ".mp3")
