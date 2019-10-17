.PHONY: all clean run
CC= gcc

CFLAGS= -std=c11
DBGFLAGS = -g -Wall -std=c11
OPTFLAGS = -O3

LDFLAGS=-lm
TARGET=train test
DBG_TARGET = dbg_train

all: $(TARGET)

train: src/train.c
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(OPTFLAGS) -Iinc

test: src/test.c
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(OPTFLAGS) -Iinc


dbg_train: src/train.c
	$(CC) -o $@ $^ $(LDFLAGS) $(DBGFLAGS) -Iinc

clean:
	rm -f $(TARGET) $(DBG_TARGET)
