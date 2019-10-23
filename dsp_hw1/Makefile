.PHONY: all clean run
CC= g++

#CFLAGS= -std=c++11 -Wall
CFLAGS = -g -Wall -std=c++11
OPTFLAGS = -O3

LDFLAGS=-lm
TARGET=train test
DBG_TARGET = dbg_train

all: $(TARGET)

train: src/train.cpp src/BWalg.o
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(OPTFLAGS) -Iinc

test: src/test.cpp src/viterbi.o
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(OPTFLAGS) -Iinc

BWalg.o: src/BWalg.h src/BWalg.cpp
	$(CC) -c src/BWalg.h src/BWalg.cpp $(CFLAGS)

viterbi.o: src/viterbi.h src/viterbi.cpp
	$(CC) -c src/viterbi.h src/viterbi.cpp $(CFLAGS)

clean:
	rm -f $(TARGET) $(DBG_TARGET) src/*.o
