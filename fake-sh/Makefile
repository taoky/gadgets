.PHONY: all clean

CC := gcc
CFLAGS := -O2 -Wall -static

OBJS = main.o
BIN = sh

all: $(BIN)

main.o: main.c
	$(CC) $(CFLAGS) -c -o $@ $<

$(BIN): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f $(BIN) $(OBJS)
