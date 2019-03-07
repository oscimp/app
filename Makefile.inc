#define all stuffs needed to compile
OUTPUT_DIR=$(BR_DIR)/output
HOST_DIR=$(OUTPUT_DIR)/host
STAGING_DIR=$(OUTPUT_DIR)/staging

COMPILER_NAME=arm-linux-
DTC=$(HOST_DIR)/bin/dtc
CC=$(HOST_DIR)/bin/$(COMPILER_NAME)gcc

APP_INSTALL_DIR:=$(OSCIMP_DIGITAL_NFS)/$(BOARD_NAME)/$(BASE_NAME)

CFLAGS+=-g -W -Wall

ifndef DONT_USE_LIB
LDFLAGS+=-L$(OSCIMP_DIGITAL_LIB) -loscimp_fpga
CFLAGS+=-I$(OSCIMP_DIGITAL_LIB)
endif

LDFLAGS+=-L$(STAGING_DIR)/usr/lib

CFLAGS+=-I$(OSCIMP_DIGITAL_DRIVER)

EXEC_NAME=$(BASE_NAME)_us
SRC=$(wildcard *.c)
OBJS=$(SRC:.c=.o)
DTS_NAME=$(wildcard *.dts)
DTBO_NAME=$(DTS_NAME:.dts=.dtbo)

all: $(EXEC_NAME) $(DTBO_NAME)

default: $(EXEC_NAME)
dtbo: $(DTBO_NAME)

$(EXEC_NAME): $(OBJS)
	$(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CFLAGS) -o $@ -c $<

%.dtbo: %.dts
	${DTC} -@ -I dts -O dtb -o $@ $<

clean:
	rm -rf $(OBJS)
	rm -f $(EXEC_NAME)
	rm -f $(DTBO_NAME)
	rm -f *.c~ *.h~ Makefile~

install: all
	mkdir -p $(APP_INSTALL_DIR)/bin
	mkdir -p $(APP_INSTALL_DIR)/bitstreams
	cp -f $(DTBO_NAME) $(EXEC_NAME) $(EXEC_NAME).sh $(APP_INSTALL_DIR)/bin

uninstall:
	rm -rf $(APP_INSTALL_DIR)

.PHONY: clean install uninstall
