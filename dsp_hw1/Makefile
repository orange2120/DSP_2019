.PHONY: all clean run
CC= g++

CFLAGS= -std=c++11
DBGFLAGS = -g -Wall -std=c++11
OPTFLAGS = -O2

LDFLAGS=-lm
TARGET=train test

all: $(TARGET)

train: src/train.c
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(OPTFLAGS) -Iinc

test: src/test.c
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(OPTFLAGS) -Iinc


dbg_train: src/train.c
	$(CC) $(DBGFLAGS)  -o $@ $^ -Iinc

clean:
	rm -f $(TARGET)
