# Adc ChanA to CPU with DMA direct

## Purpose

This application is used to fetch, from ADC channelA, a large amount of sample.
By using the DMA to store data in CPU RAM instead of BRAM it's possible to
bypass the redpitaya Zynq resources limitation.

By default this project fetches 1Msamples 16bits at full speed (125MS/s)

To sample both ADC (instead of only ADC channelA), update the design with
```
NB_INPUT 2
```
The number of samples and connections will be updated automagically.

## Usage

After executing *adcChanADmaDirect_us* a binary file called *dump.bin* is
present in current directory. To read content using Gnu Octave in single channel mode:
```
fd = fopen("dump.bin"); dd = fread(fd, inf, "int16"); fclose(fd); 
```
and in dual channel mode
```
fd = fopen("dump.bin"); dd = fread(fd, inf, "int16"); fclose(fd); d1=dd(1:2:end); d2=dd(2:2:end);
```
