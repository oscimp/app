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
CFLAGS+=-I$(OSCIMP_DIGITAL_LIB)
LDFLAGS+=-L$(OSCIMP_DIGITAL_LIB)
ifndef USE_STATIC_LIB
LDFLAGS+=-loscimp_fpga
else
LDFLAGS+=-loscimp_fpga_static
endif
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

install_ssh: all
	mkdir -p /tmp/$(BASE_NAME)/bin
	mkdir -p /tmp/$(BASE_NAME)/modules
	cp $(CORE_MODULES_LIST) /tmp/$(BASE_NAME)/modules/
	cp -f $(DTBO_NAME) $(EXEC_NAME) $(EXEC_NAME).sh /tmp/$(BASE_NAME)/bin
	sed -i 's/^CORE_MODULES_DIR=.*/CORE_MODULES_DIR=\.\.\/modules/g' /tmp/$(BASE_NAME)/bin/$(EXEC_NAME).sh
	scp -r /tmp/$(BASE_NAME) root@$(IP):/tmp/

uninstall:
	rm -rf $(APP_INSTALL_DIR)

.PHONY: clean install uninstall
