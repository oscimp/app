CORE_MODULES_DIR=../../modules

mkdir -p /lib/firmware
cp ../bitstreams/redSPI_wrapper.bit.bin /lib/firmware
DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga
if [ -d $DTB_DIR ]; then
	rmdir $DTB_DIR
fi
mkdir $DTB_DIR
cat redSPI.dtbo > $DTB_DIR/dtbo
