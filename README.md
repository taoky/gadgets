# gadgets

It's where my code snippets stored.

放一些小到不适合单独开仓库的代码和项目。除非特殊说明，LICENSE 为 Apache。

## Introduction

- `backTCP`: 我的计网某次实验的代码，实现一个能够应对丢包和乱序的，支持 GBN 和 SR 的传输协议。
- `BeepPlayConverter`: 把 MIDI（和其他一些乐谱格式）转换成音高、八度和持续时间的序列。对一部分乐谱效果很好。我的数电实验大作业也用到了这个脚本。
- `Bilibili OST Downloader`: 在我知道 `you-get`（和其他下载流媒体网站视频的软件）有 `-p` 这个参数，和有更好的地方下载音乐之前写的一系列小脚本，用来从 B 站下音乐，提取音频轨为 MP3，并且加上 metadata。
- `consoleTimer`: 大一上半学期程序设计一的实验。一个五彩缤纷的，可以在你的终端上闪耀的计时器。单文件，支持 Windows 和安装了 ncurses 的 *NIX。
- `data-structure-exp-toys`: 数据结构的实验代码。我个人最推荐 `exp1`（一个离散时间模拟的小游戏）和 `exp2`（哈夫曼树压缩/解压缩，记得用 `pypy` 跑，否则会很慢）。
- `fake-sh`: 提供一个假的 Shell。有当蜜罐的潜质，但我后来发现并没有什么用。
- `HFLC`: 合肥大炮，力学与热学的大作业。
- `KnightTour`: 程序设计二实验，[骑士巡逻问题](https://zh.wikipedia.org/zh-cn/%E9%A8%8E%E5%A3%AB%E5%B7%A1%E9%82%8F)模拟器。也应该是我写的第一个并行来计算的代码，虽然用的是 Service Worker。
- `myBank`: 程序设计一大作业。相对于大家大一时的平均代码质量来说，它应该算是很好的。
- `pwn-dockerfile`: 一个跑 pwn 题的简单 dockerfile。不建议在生产环境使用。
- `PyQt-Sudoku`: 程序设计二实验，用 `PyQt` 写的数独程序。