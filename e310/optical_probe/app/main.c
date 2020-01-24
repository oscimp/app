#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>

#include <iio.h>
#include <ad9361.h>

#include <fpgagen_conf.h>

/* 3s @ 128khz */
/* complex dual */
#define SAMP_SIZE (384000 * 2 * 2)
//#define SAMPLERATE 128000
#define SAMPLERATE 1024000

int configure_fpga(long lo, int g1, int g2);

int main(int argc, char **argv)
{
	int g1 = 30;
	int g2 = 0;

	if (argc < 2) {
		printf("%s: missing lo\n", argv[0]);
		return EXIT_FAILURE;
	}

	long lo = atol(argv[1]);

	if (argc > 2)
		g1 = atoi(argv[2]);
	if (argc > 3)
		g2 = atoi(argv[3]);

	printf("%d lo: %ld g1: %d g2: %d\n", sizeof(int16_t)*SAMP_SIZE, lo, g1, g2);
	uint16_t *buff;

	buff = (uint16_t*) malloc(sizeof(uint16_t) * SAMP_SIZE);
	if (!buff) {
		printf("malloc failed\n");
		return EXIT_FAILURE;
	}

	int fi, fo;

	fi = open("/dev/data00", O_RDWR);
	fo = open("/tmp/data.bin", O_WRONLY | O_CREAT);
	if (fi < 0) {
		printf("%s: open /dev/data00 failed\n", argv[0]);
		return EXIT_FAILURE;
	}
	if (fo < 0) {
		printf("%s: open /tmp/data.bin failed\n", argv[0]);
		return EXIT_FAILURE;
	}
	configure_fpga(lo, g1, g2);

	/* configure pulse */
	int base_freq = 100000000; /* /s */
	int base_time = (int)((float)base_freq * 2.5); /* 5s */
	base_time = 384000;
	fpgagen_send_conf("/dev/pulse", 0 << 2, base_time);

	/* start pulse */
	fpgagen_send_conf("/dev/pulse", 2 << 2, 1);

	read(fi, buff, SAMP_SIZE * sizeof(uint16_t));
	write(fo, buff, SAMP_SIZE * sizeof(uint16_t));

	close(fi);
	close(fo);
	free(buff);
}


int setparamsStr(struct iio_device *phy, char *key, char *val)
{
	struct iio_channel *chn = NULL;
	const char *attr = NULL;
	int ret;

	ret = iio_device_identify_filename(phy, key, &chn, &attr);
	if (ret) {
		printf("Parameter not recognized: %s", key);
		return EXIT_FAILURE;
	}
	if (chn)
		ret = iio_channel_attr_write(chn, attr, val);
	else if (iio_device_find_attr(phy, attr))
		ret = iio_device_attr_write(phy, attr, val);
	else
		ret = iio_device_debug_attr_write(phy, attr, val);
	if (ret < 0) {
		printf("Unable to write attribute %s : %d\n", key, ret);
		return EXIT_FAILURE;
	}

	return EXIT_SUCCESS;
}

int setparams(struct iio_device *phy, char *key, int value)
{
	char val[128];
	sprintf(val, "%d", value);
	return setparamsStr(phy, key, val);
}

int configure_fpga(long lo, int g1, int g2)
{
	int ret;
	long lo_freq = lo;

#if 1
	/* ad936x configuration */
	struct iio_device *dev;
	struct iio_channel *rx0_i, *rx0_q;

	struct iio_device *phy;
	struct iio_context *ctx;
	ctx = iio_create_local_context();

	dev = iio_context_find_device(ctx, "cf-ad9361-lpc");
	phy = iio_context_find_device(ctx, "ad9361-phy");

	setparams(phy, "out_altvoltage0_RX_LO_frequency", lo_freq);

	setparams(phy, "in_voltage_rf_bandwidth", 50000000);//bandwidth);
	setparams(phy, "in_voltage_quadrature_tracking_en", 1);//quadrature);
	setparams(phy, "in_voltage_rf_dc_offset_tracking_en", 1);//rfdc);
	setparams(phy, "in_voltage_bb_dc_offset_tracking_en", 1);//bbdc);

	setparamsStr(phy, "in_voltage0_gain_control_mode", "manual");//gain1_str);
	setparamsStr(phy, "in_voltage1_gain_control_mode", "manual");//gain1_str);
	setparams(phy, "in_voltage1_hardwaregain", g1);
	setparams(phy, "in_voltage0_hardwaregain", g2);

	/* not necessary for E310 since A/B/C is selected according to lo_freq */
	//setparamsStr(phy, "in_voltage0_rf_port_select", "A_BALANCED");

	ret = ad9361_set_bb_rate(phy, SAMPLERATE);
	if (ret) {
		printf("Unable to set BB rate\n");
		return EXIT_FAILURE;
	}

	rx0_i = iio_device_find_channel(dev, "voltage0", 0);
	rx0_q = iio_device_find_channel(dev, "voltage1", 0);

	iio_channel_enable(rx0_i);
	iio_channel_enable(rx0_q);
#endif

	return EXIT_SUCCESS;
}
