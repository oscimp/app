BASE_NAME=optical_probe
USE_STATIC_LIB=1
LDFLAGS+=-liio -lad9361

CORE_MODULES_LIST=$(OSCIMP_DIGITAL_DRIVER)/fpgagen_core/*.ko \
		$(OSCIMP_DIGITAL_DRIVER)/data_dma_direct_core/*.ko
include $(OSCIMP_DIGITAL_APP)/Makefile.inc
