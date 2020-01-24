CORE_MODULES_DIR=./

DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga
if [ -d $DTB_DIR ]; then
	rmdir $DTB_DIR
fi
mkdir $DTB_DIR
cat optical_probe.dtbo > $DTB_DIR/dtbo

insmod ${CORE_MODULES_DIR}/fpgagen_core.ko
insmod ${CORE_MODULES_DIR}/data_dma_direct_core.ko
