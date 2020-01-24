####################################################################################
## Copyright 2018(c) Analog Devices, Inc.
## Auto-generated, do not modify!
####################################################################################

PROJECT_NAME := usrpe31x

M_DEPS += $(ADI_HDL_DIR)/library/xilinx/common/ad_iobuf.v
M_DEPS += $(ADI_HDL_DIR)/library/axi_ad9361/axi_ad9361_delay.tcl

LIB_DEPS += axi_ad9361
LIB_DEPS += axi_dmac
LIB_DEPS += util_pack/util_cpack2
LIB_DEPS += util_pack/util_upack2
LIB_DEPS += util_tdd_sync

include $(ADI_HDL_DIR)/projects/scripts/project-xilinx.mk

BIT_FILE=*.runs/impl_1/*.bit
install_boot:$(BIT_FILE)
	scp $(BIT_FILE) root@192.168.0.10:/boot/

BIT_FILE=usrpe31x.runs/impl_1/system_top.bit
BIF_FILE=$(TARGET).bif
BIN_FILE=$(TARGET).bit.bin

force_bin:
	@rm -f $(BIF_FILE) $(BIN_FILE)
	@echo "all:" >> $(BIF_FILE)
	@echo "{" >> $(BIF_FILE)
	@echo " $(BIT_FILE)" >> $(BIF_FILE)
	@echo "}" >> $(BIF_FILE)

	bootgen -w -image $(NAME).bif -arch zynq -process_bitstream bin
	mv $(BIT_FILE).bin .
	@rm -f $(BIF_FILE)

force_install:
	if [ ! -d $(INSTALL_DIR) ]; then mkdir -p $(INSTALL_DIR); fi
	cp $(BIN_FILE) $(INSTALL_DIR)
