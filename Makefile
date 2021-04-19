CC = gcc
CFLAGS = -g
# CFLAGS = -g -v -Wall -std=gnu99 -static 
# CFLAGS += $(shell pkg-config --cflags json-c)
# LDFLAGS += $(shell pkg-config --libs json-c)
JSON_C_DIR=/usr/local
CFLAGS += -I$(JSON_C_DIR)/include/json-c
LDFLAGS+= -L$(JSON_C_DIR)/lib 
LIBJSONC = -ljson-c

all: translator

translator:
# 	$(CC) $(CFLAGS) translator.c -o translator
	$(CC) $(CFLAGS) $(LDFLAGS) translator.c -o translator $(LIBJSONC)

clean:
	rm -f *.o *.so *.a
	rm -f translator