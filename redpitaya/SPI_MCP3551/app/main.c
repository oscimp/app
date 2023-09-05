#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

int main()
{
	int i, value, ret;
	char fileScale[256], fileRaw[256];
	FILE *fd, *raw[4];
	double scale[4];

	/* for all device read scale and open raw file
	 * in fact since all device are MCP3551, this value is always the same
	 */
	/* device0                         -> XADC
	 * device1/device2/device3/device4 -> MCP
	 */
	for (i = 0; i < 4; i++) {
		sprintf(fileScale, "/sys/bus/iio/devices/iio:device%d/in_voltage-voltage_scale", i+1);
		sprintf(fileRaw, "/sys/bus/iio/devices/iio:device%d/in_voltage0-voltage1_raw", i+1);

		fd = fopen(fileScale, "r");
		if (!fd) {
			printf("erreur d'ouverture de %s\n", fileScale);
			return 1;
		}
		fscanf(fd, "%lf", &scale[i]);
		printf("%10.24lf ", scale[i]);
		fclose(fd);

		raw[i] = fopen(fileRaw, "r");
		if (!raw[i]) {
			printf("erreur d'ouverture de %s\n", fileRaw);
			return 1;
		}

	}
	printf("\n");

	while (1) {
		for (i = 0; i < 4; i++) {
			fscanf(raw[i], "%d", &value);
			printf("%d %3.12lf ", value, (double)value*scale[i]);
			fseek(raw[i], 0, SEEK_SET);
		}
		ret = usleep(100*1000);
		if (ret != 0) {
			printf("erreur de usleep %s\n", strerror(ret));
			return 1;
		}

	}

	return 0;
}
