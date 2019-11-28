SRIPATH ?= /root/srilm-1.5.10
MACHINE_TYPE ?= i686-m64
INC_PATH ?= inc
SRC_PATH ?= src

CXX = g++
CXXFLAGS = -O2 -std=c++11 -Wall -I$(SRIPATH)/include -I$(INC_PATH)
CXXFLAGS_MAP = -Wall -O2 -std=c++11
CXXFLAGS_MAP_DBG = -Wall -g -std=c++11
vpath lib%.a $(SRIPATH)/lib/$(MACHINE_TYPE)
vpath %.c $(SRC_PATH)
vpath %.cpp $(SRC_PATH)

TARGET = mydisambig
SRC = mydisambig.cpp
OBJ = $(SRC:.cpp=.o)

MAP_TARGET = map map_dbg
FROM ?= Big5-ZhuYin.map
TO ?= ZhuYin-Big5.map
.PHONY: all clean map

all: disamb.o $(TARGET)

$(TARGET): $(OBJ) disamb.o -loolm -ldstruct -lmisc
	$(CXX) $(LDFLAGS) -o $@ $^

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $<

disamb.o: src/disamb.h src/disamb.cpp
	$(CXX) $(CXXFLAGS) -c src/disamb.h src/disamb.cpp

map: src/map.cpp
	@#TODO
	@#python3 mapping.py $(FROM) $(TO)
	$(CXX) $(CXXFLAGS_MAP) -o $@ $^

map_dbg: src/map.cpp
	$(CXX) $(CXXFLAGS_MAP_DBG) -o $@ $^

clean:
	$(RM) $(OBJ) $(TARGET) $(MAP_TARGET)
