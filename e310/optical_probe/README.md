# Optical probe for acoustic wave displacement field mapping using a E310 USRP 

Acoustic transducers have been developed as a solution for compact analog signal 
processing of radiofrequency signals. The electromagnetic signal is converted to
an acoustic wave through the inverse piezoelectric effect, with a velocity ratio
of 1E5 between electromagnetic and acoustic waves leading to a shrinkage of device
size by the same ratio. However, acoustic wave propagation is subject to various artifacts
including bouncing on reflectors, scattering or attenuation. An optical probe is designed
to map the acoustic field of the radiofrequency acoustic wave

## Motivation

Classical instrumentations techniques include collecing measurements from (slow) laboratory
equipment (spectrum analyzer, lock in amplifier) or oscilloscope. Here we use an affordable
radiofrequency signal acquisition system for recording the radiofrequency signal and streaming
through a 0-MQ channels samples to GNU/Octave for further processing. The FPGA bitstream has
been modified to trigger measurement on an external signal synchronizing data streaming with
laser scanning.

<img src="https://github.com/oscimp/app/blob/master/e310/optical_probe/figures/DSC_0338_3.JPG" width=300>
<img src="https://github.com/oscimp/app/blob/master/e310/optical_probe/figures/DSC_0344_3.JPG" width=300>

## Developments

The provided bitstream will synchronize data acquisition, based on the Analog Devices data acquisition
blocks, on an external trigger signal.
