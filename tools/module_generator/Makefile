INSTALL_DIR:=/usr/local/bin
CC=g++
CPPFLAGS=-DDEBUG -g -Wall -fPIC
LDFLAGS=-ltinyxml2
DEST=module_generator
SRC=$(wildcard *.cpp)
OBJS=$(SRC:.cpp=.o)

all: $(DEST)

$(DEST): $(OBJS)
	 $(CC) -o $@ $^ $(LDFLAGS)

%.o: %.c
	$(CC) $(CPPFLAGS) -o $@ -c $<

install: $(DEST)
	mkdir -p $(INSTALL_DIR)
	cp $(DEST) $(INSTALL_DIR)

clean:
	rm -rf $(OBJS) $(DEST)


