# 计算机网络 backTCP 实验报告

\<REDACTED\>

## 实验内容

实现能够经受乱序和丢包考验的可靠传输协议。不需要三次握手。重传可使用 GBN 或 SR。

这里，本代码实现了 GBN 和 SR（使用时在 `config.py` 中二选一），经过 `testch.py`，在实验环境下测试通过。使用了提供的 Python 代码框架，以最好地和测试信道代码融合。

## 实验环境

Python 3.6.7，macOS 10.14.6。不需要安装其他第三方 Python 模块。

## 实现步骤与说明

### 代码文件

`backTCP.py`: 实现收、发功能的主代码。

`client.py`: 客户端（发送端）的包装代码，未修改。

`config.py`: 配置，包括窗口大小、配置时间、是否使用 SR（如果不使用，则 GBN）

`server.py`: 服务端（接收端）的包装代码，未修改。

`testch.py`: 测试信道代码，未修改。

`utils.py`: 工具函数。在原来的基础上加入了循环 Timer，用于 SR。

### 使用方法

首先配置 `config.py`。

#### 直接收发

先运行服务端 `python server.py output.bin`，再运行客户端 `python client.py testdata.txt`。

#### 经过测试信道收发

运行 `python testch.py` 和 `python server.py output.bin`，然后运行客户端 `python client.py -p 6667 testdata.txt`。

#### 校验

执行后 `diff output.bin testdata.txt`，无输出，代表执行正确。

#### 其他

如果不需要调试，可以修改 logging 等级，不输出 INFO 等级的 `log`，以加快速度。

### 算法

#### GBN

##### 发送端

先发送完一个窗口，维护窗口起始与结束的变量。然后循环等待接收 ACK。收到 ACK 后，观察 ACK 是否在窗口内，不在则忽略，在则滑动窗口，发送未发送的包。

此处对所有的 socket 操作都设置了 timeout，如果收 ACK 的时候抛出了 timeout 异常，就把窗口内的重发一遍。

##### 接收端

如果收到包的序号 = `(latest_ack_no + 1) & 0xFF`，就接受，返回对这个包的 ACK 并更新 `latest_ack_no`。否则就把上个发送的 ACK 包重发一遍。

#### SR

##### 发送端

使用继承了 `threading.Timer` 后修改的循环 Timer，对每个发包都设置定时器。照样，先发送完一个窗口。然后循环等待接收 ACK。收到后更新记录，（如果在窗口内）标记该号码已经收到，并结束对应的 Timer。如果收到了基序号对应的 ACK，滑动窗口，并发送新的包。

如果接收 ACK 时超时，重新循环，继续接收。

##### 接收端

收到窗口内的 ACK 时，存储对应数据，如果序号等于基序号，滑动窗口。将数据接在总数据后面。而如果在窗口开始的后 N 个（N = 窗口大小）中，就仅发送对应的 ACK 确认。

### 坑

#### 1 字节的序号

不够用，会循环。为了处理这样的循环，加入了一些额外的判断等。

#### 接收到的数据包长得不太对

用 Wireshark 抓包，会发现一些 backTCP 包合到了一个 TCP 包里面。在接收时，需要修改默认的代码，将 header 中的 data_off 改成 data_len（payload 的大小）。先读 header，再根据包中的大小读对应 payload。

#### 计时器与多线程

在实现 SR 的时候，每个包都要计时器。`threading.Timer` 是用线程实现的，而单个 socket 分享给多个线程是线程不安全的。需要加锁。使用 `lock = threading.Lock()`，然后每次收发：

```python
with lock:
    ...
```

## 实验结果

以下关闭了 logging 输出以加快速度。测试窗口大小 = 10。

### GBN

不使用测试信道：

```shell
Shell 1:
$ python server.py output.bin

Shell 2:
$ time python client.py testdata.txt
python client.py testdata.txt  0.24s user 0.13s system 82% cpu 0.440 total
$ diff testdata.txt output.bin
$ # 无输出，两文件完全一致。
```

使用测试信道：

```shell
Shell 1:
$ python server.py output.bin

Shell 2:
$ python testch.py

Shell 2:
$ time python client.py -p 6667 testdata.txt
python client.py -p 6667 testdata.txt  2.24s user 1.42s system 11% cpu 31.691 total
$ diff testdata.txt output.bin
$ # 无输出，两文件完全一致。
```

### SR

不使用测试信道：

```shell
Shell 1:
$ python server.py output.bin

Shell 2:
$ time python client.py testdata.txt
python client.py testdata.txt  2.36s user 1.66s system 28% cpu 13.947 total
$ diff testdata.txt output.bin
$ # 无输出，两文件完全一致。
```

使用测试信道：

```shell
Shell 1:
$ python server.py output.bin

Shell 2:
$ python testch.py

Shell 2:
$ time python client.py -p 6667 testdata.txt
python client.py -p 6667 testdata.txt  2.96s user 2.09s system 21% cpu 23.266 total
$ diff testdata.txt output.bin
$ # 无输出，两文件完全一致。
```

可见线程锁带来的开销是昂贵的，尤其是在无丢包和乱序的情况下，使用单 socket + 线程锁的 SR 实现效果远不如 GBN。但即使如此，在网络环境混乱的情况下，SR 的效果比 GBN 好很多。