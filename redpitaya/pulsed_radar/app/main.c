#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/types.h>
/* memory management */
#include <sys/mman.h>
#include <string.h>
#include <switch_conf.h>
#include <edfb_conf.h>
#include <fpgagen_conf.h>
#include <math.h>

#define ACQUIS_SIZE 4096  // taille de la RAM dans le FPGA (impos\'e)
#define NB_FILES    1

enum {
	MODE_TEMPO = 1,
	MODE_POS,
	MODE_INPUT,
	MODE_GEN_PERIOD,
	TXON,
	RXOFF,
	LIMIT,
	CHECK_START_OFFSET,
	BYPASS_CHECK,
	BYPASS_MEAN,
	SET_ITER
};

void print_usage(char *exec);
int readData(char *devname, char *output_name);

int getParams(int argc, char **argv)
{
	int value,nvalue;
	int mode;
	int shift_val;

	if (argc < 2)
		goto error_input;

	if (!strncmp(argv[1], "tempo", 5)) {
		mode = MODE_TEMPO;
		goto transfert_input;
	} else if (!strncmp(argv[1], "pos", 3))
		mode = MODE_POS;
	else if (!strncmp(argv[1], "input", 5))
		mode = MODE_INPUT;
	else if (!strncmp(argv[1], "period", 6))
		mode = MODE_GEN_PERIOD;
	else if (!strncmp(argv[1], "txon", 3))
		mode = TXON;
	else if (!strncmp(argv[1], "pon", 3)) {
		printf("pon is obsolete: use txon\n");
		mode = TXON;
	} else if (!strncmp(argv[1], "rxff", 4))
		mode = RXOFF;
	else if (!strncmp(argv[1], "poff", 4)) {
		printf("poff is obsolete: use rxoff\n");
		mode = RXOFF;
	}else if (!strncmp(argv[1], "limit", 5))
		mode = LIMIT;
	else if (!strncmp(argv[1], "start_offset", 12))
		mode = CHECK_START_OFFSET;
	else if (!strncmp(argv[1], "bypass_check", 12))
		mode = BYPASS_CHECK;
	else if (!strncmp(argv[1], "bypass_mean", 11))
		mode = BYPASS_MEAN;
	else if (!strncmp(argv[1], "iter", 4))
		mode = SET_ITER;
	else
		goto error_input;

	if (argc < 3)
		goto error_input;
	value = atoi(argv[2]);

	switch(mode) {
		case MODE_POS :
		edfb_send_conf("/dev/extractData", value);
		goto transfert_input;
		break;
	case MODE_INPUT :
		switch_send_conf("/dev/switchDAC", value);
		break;
	case MODE_GEN_PERIOD:
		fpgagen_send_conf("/dev/genRadar", (0x01<<2), value);
		/* check frame need to be updated too */
		fpgagen_send_conf("/dev/checkValidRafale", (0x03<<2), value-1);
		break;
	case TXON:
		fpgagen_send_conf("/dev/genRadar", (0x03<<2), value);
		fpgagen_recv_conf("/dev/genRadar", (0x03<<2), &nvalue);
		if (nvalue != value) printf("Error writing TX pulse duration.\n");
		break;
	case RXOFF:
		fpgagen_send_conf("/dev/genRadar", (0x02<<2), value);
		fpgagen_recv_conf("/dev/genRadar", (0x02<<2), &nvalue);
		if (nvalue != value) printf("Error writing RX pulse duration.\n");
		break;
	case LIMIT:
		fpgagen_send_conf("/dev/checkValidRafale", (0x02<<2), value);
		fpgagen_recv_conf("/dev/checkValidRafale", (0x02<<2), &nvalue);
		if (nvalue != value) printf("Error writing limit value.\n");
		break;
	case CHECK_START_OFFSET:
		fpgagen_send_conf("/dev/checkValidRafale", (0x01<<2), value);
		fpgagen_recv_conf("/dev/checkValidRafale", (0x01<<2), &nvalue);
		if (nvalue != value) printf("Error writing limit value.\n");
		break;
	case BYPASS_CHECK:
		switch_send_conf("/dev/switchCheck", value);
		break;
	case BYPASS_MEAN:
		switch_send_conf("/dev/switchMean", value);
		break;
	case SET_ITER:
		shift_val = log2(value);
		fpgagen_send_conf("/dev/meanVector", (0x01 << 2), shift_val);
		fpgagen_send_conf("/dev/meanVector", (0x02 << 2), value);
		break;
	}

	return 0;

transfert_input:
	return mode;
 error_input:
	print_usage(argv[0]);
	return -1;
}

int main(int argc, __attribute__ ((unused))
	 char **argv)
{
	int mode; 
	char filename[62];
	char out_base_name[62];

	mode = getParams(argc, argv);
	if (mode < 0)
		return EXIT_FAILURE;
	if (mode == 0)
		return EXIT_SUCCESS;

	printf("fin acquistion : transfert!\n");

	switch (mode) {
	case MODE_POS:
		sprintf(filename, "/dev/dataExtract_to_ram");
		sprintf(out_base_name, "mode_pos");
		break;
	case MODE_TEMPO:
		sprintf(filename, "/dev/dataDirect_to_ram");
		sprintf(out_base_name, "mode_tempo");
		break;
	}

	return readData(filename, out_base_name);
}

int readData(char *devname, char *output_name)
{
	int ret = EXIT_FAILURE;;
	int i, ii;
	char filename[62];
	int32_t *content;
	FILE *fileout;
	short vali, valq;

	int fd = open(devname, O_RDWR);
	if (fd < 0) {
		printf("erreur d'ouverture de %s\n", devname);
		return EXIT_FAILURE;
	}

	content = (int32_t *) malloc(ACQUIS_SIZE * sizeof(int32_t));
	if (content == NULL) {
		close(fd);
		printf("erreur d'allocation\n");
		return EXIT_FAILURE;
	}

	for (i = 0; i < NB_FILES; i++) { 
		sprintf(filename, "%s_%02d.dat", output_name, i);
		fileout = fopen(filename, "w+");
		if (fileout == NULL) {
			printf("erreur d'ouverture de %s\n", filename);
			goto out;
		}

		read(fd, content, ACQUIS_SIZE * sizeof(int32_t));
		for (ii = 0; ii < ACQUIS_SIZE; ii++) {
			vali = ((content[ii] >> 16) & 0xffff);
			valq = (content[ii] & 0xffff);
			fprintf(fileout, "%d %d\n", vali, valq);
		}
		fflush(fileout);
		fclose(fileout);
	}
	ret = EXIT_SUCCESS;
 out:
	close(fd);
	free(content);
	return ret;
}

void print_usage(char *exec)
{
	printf("%s mode [position]\n", exec);
	printf("mode : tempo, pos, input, period, pulse, limit\n\n");
	printf("tempo : transfert full frames\n");
	printf("pos posoffset : transfert a serie of point at posoffset position\n");
	printf("input (0/1) : select tempo or point for DAC input\n");
	printf("period nbpoint : set number of data per frame\n");
	printf("pon nbpoint (obsolete use txon)\n");
	printf("poff nbpoint (obsolete use rxoff\n");
	printf("txon nbpoint\n");
	printf("rxoff nbpoint\n");
	printf("limit maxValue : fix high limit for frame coruption detection\n");
	printf("start_offset offset : set the start offset for check frame block \n");
	printf("bypass_check (0/1) : use or not check frame block\n");
	printf("bypass_mean (0/1) : use or not mean vector block\n");
	printf("iter n : set number of iteration for mean\n");
}
