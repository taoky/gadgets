graph: main.o
	$(CC) $(CFLAGS) $^ -o $@

main.o: main.cpp
	$(CC) $(CFLAGS) -c $^

CC = clang++
CFLAGS = -Wall -O3 -std=c++1y

clean:
	-rm graph *.o

.PHONY: clean

