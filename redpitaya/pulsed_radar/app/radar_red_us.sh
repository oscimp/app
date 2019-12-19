CORE_MODULES_DIR=../../modules

mkdir -p /lib/firmware
cp ../bitstreams/radar_red_wrapper.bit.bin /lib/firmware
DTB_DIR=/sys/kernel/config/device-tree/overlays/fpga
rmdir $DTB_DIR
mkdir $DTB_DIR
cat radar_red.dtbo > $DTB_DIR/dtbo

echo "65535" > /sys/bus/iio/devices/iio\:device1/out_voltage0_raw
echo "65535" > /sys/bus/iio/devices/iio\:device1/out_voltage1_raw

insmod ${CORE_MODULES_DIR}/fpgagen_core.ko
insmod ${CORE_MODULES_DIR}/data_to_ram_core.ko
insmod ${CORE_MODULES_DIR}/edfb_core.ko    # Extract Data From Burst (edfb)
insmod ${CORE_MODULES_DIR}/switch_core.ko

#default
./radar_red_us period 512       # 512 samples * 8 ns/sample = 4.096 us Pulse Repetition Rate
./radar_red_us limit 55000      # reject noise threshold
./radar_red_us start_offset 350 # burst sample at which only noise is measured (no sample)
./radar_red_us bypass_mean  1   # no averaging
./radar_red_us bypass_check 1   # do NOT reject noisy measurements (e.g. WiFi/BT emissions)
