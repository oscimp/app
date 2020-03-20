CORE_MODULES_DIR=../../modules

mkdir -p /lib/firmware
cp ../bitstreams/demod_pid1_pidpwm3_vco_only2_wrapper.bit.bin /lib/firmware
DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga
if [ -d $DTB_DIR ]; then
	rmdir $DTB_DIR
fi
mkdir $DTB_DIR
cat demod_pid1_pidpwm3_vco_only2.dtbo > $DTB_DIR/dtbo

insmod ${CORE_MODULES_DIR}/add_const_core.ko
insmod ${CORE_MODULES_DIR}/axi_to_dac_core.ko
insmod ${CORE_MODULES_DIR}/pidv3_axi_core.ko
insmod ${CORE_MODULES_DIR}/data_to_ram_core.ko
insmod ${CORE_MODULES_DIR}/fpgagen_core.ko
insmod ${CORE_MODULES_DIR}/fpgagen_core.ko
insmod ${CORE_MODULES_DIR}/nco_counter_core.ko
insmod ${CORE_MODULES_DIR}/fir_core.ko
