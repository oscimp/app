CORE_MODULES_DIR=../../modules

mkdir -p /lib/firmware
cp -r ../bitstreams/adcChanADmaDirect_wrapper.bit.bin /lib/firmware
DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga
if [ -d $DTB_DIR ]; then
	rmdir $DTB_DIR
fi
mkdir $DTB_DIR
cat adcChanADmaDirect.dtbo > $DTB_DIR/dtbo

insmod ${CORE_MODULES_DIR}/data_dma_direct_core.ko
