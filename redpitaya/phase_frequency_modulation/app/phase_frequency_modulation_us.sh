CORE_MODULES_DIR=../../modules

mkdir -p /lib/firmware
cp ../bitstreams/phase_frequency_modulation_wrapper.bit.bin /lib/firmware
DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga
if [ -d $DTB_DIR ]; then
	rmdir $DTB_DIR
fi
mkdir $DTB_DIR
cat phase_frequency_modulation.dtbo > $DTB_DIR/dtbo

insmod ${CORE_MODULES_DIR}/axi_to_dac_core.ko
insmod ${CORE_MODULES_DIR}/add_const_core.ko
insmod ${CORE_MODULES_DIR}/nco_counter_core.ko
