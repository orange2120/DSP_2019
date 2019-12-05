SRIPATH ?= /root/srilm-1.5.10
MACHINE_TYPE ?= i686-m64
INC_PATH ?= inc
SRC_PATH ?= src

CXX = g++
CXXFLAGS = -std=c++11 -Wall -I$(SRIPATH)/include -I$(INC_PATH)
OPTFLAGS = -O3
DBGFLAGS = -g
SRLIBFLAGS = -loolm -ldstruct -lmisc
CXXFLAGS_MAP = -Wall -std=c++11

vpath lib%.a $(SRIPATH)/lib/$(MACHINE_TYPE)
vpath %.c $(SRC_PATH)
vpath %.cpp $(SRC_PATH)

TARGET = mydisambig
DBG_TARGET = mydisambig_dbg
SRC = mydisambig.cpp
OBJ = $(SRC:.cpp=.o)

MAP_TARGET = map map_dbg
FROM ?= Big5-ZhuYin.map
TO ?= ZhuYin-Big5.map
.PHONY: all clean map

all: $(TARGET) 
dbg: $(DBG_TARGET)

# $(TARGET): $(OBJ) disamb.o -loolm -ldstruct -lmisc
	# $(CXX) $(LDFLAGS) -o $@ $^

# %.o: %.cpp
	# $(CXX) $(CXXFLAGS) $(OPTFLAGS) -c $<

mydisambig: disamb.o $(SRC_PATH)/mydisambig.cpp $(SRLIBFLAGS)
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) $(LDFLAGS) $^ -o $@

mydisambig_dbg: disamb_dbg.o $(SRC_PATH)/mydisambig.cpp $(SRLIBFLAGS)
	$(CXX) $(CXXFLAGS) $(DBGFLAGS) $(LDFLAGS) $^ -o $@

disamb.o: $(INC_PATH)/disamb.h $(SRC_PATH)/disamb.cpp
	$(CXX) $(CXXFLAGS) $(OPTFLAGS) -c $^

disamb_dbg.o: $(INC_PATH)/disamb.h $(SRC_PATH)/disamb.cpp
	$(CXX) $(CXXFLAGS) $(DBGFLAGS) -c $^
	mv disamb.o disamb_dbg.o

map: src/map.cpp
	@#TODO
	@#python3 mapping.py $(FROM) $(TO)
	$(CXX) $(CXXFLAGS_MAP) $(OPTFLAGS) -o $@ $^
	./map $(FROM) $(TO)

map_dbg: src/map.cpp
	$(CXX) $(CXXFLAGS_MAP) $(DBGFLAGS) -o $@ $^

clean:
	$(RM) $(TARGET) $(DBG_TARGET) $(MAP_TARGET) $(SRC_PATH)/*.o *.o $(INC_PATH)/*.gch
