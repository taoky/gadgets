url="https://www.bilibili.com/video/av2520368/" # change it to what you want to download
pcount=15 # how many sub-videos do this link have
software="you-get"
page="#page="

for i in `seq 1 $pcount`; do $software "$url$page$i"; done
