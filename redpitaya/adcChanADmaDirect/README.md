# Adc ChanA to CPU with DMA direct

## Purpose

This application is used to fetch, from ADC channelA, a large amount of sample.
By using the DMA to store data in CPU RAM instead of BRAM it's possible to
bypass the redpitaya Zynq resources limitation.

By default this project fetch 1Msamples 16bits at full speed (125MS/s)

## Usage

After executing *adcChanADmaDirect_us* a binary file called *dump.bin* is
present in current directory. To read content using Gnu Octave:
```
fd = fopen("dump.bin"); dd = fread(fd, inf, "int16"); fclose(fd); plot(dd)
```
