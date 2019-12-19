# Pulsed RADAR for SAW sensor interrogation

## Purpose

Surface Acoustic Wave (SAW) transducers act as ideal cooperative targets for passive wireless sensing.
Many means of probing the RADAR cross section of SAW sensors have been demonstrated as long as
the emitted signal spectrum matches the sensor transfer function. While pulsed mode RADAR is hardly energy
efficient, it provides the unique opportuniy of maximizing measurement bandwidth by collecting a full
sensor response at the pulse repetition rate. Assuming the longest sensor delay is 4 microseconds, the
measurement refresh rate can reach 250 kHz, a useful characteristics for vibration monitoring when probing
strain sensors for example.

## Hardware setup

A VCO has been selected as signal source to easily demonstate the local oscillator stability sensitivity
of the measurement. The VCO feeds a fast radiofrequency switch triggered by the Redpitaya to generate the
emitted pulse. A fraction of the VCO power drives a I/Q detector fed on the other hand by the amplified received
signal. The I/Q detector output is amplified by a baseband VGA (Variable Gain Amplified) whose output feeds
the Redpitaya ADC. Since a typical SAW sensor echo lasts a few tens of nanoseconds, the 125 MS/s (8-ns sampling
period) is more than enough to collect the sensor response. Observing the fast evolution of the echo phase
is achieved by generating on the fast DAC outputs an analog copy of the I and Q coefficients best viewed
on a radiofrequency grade oscilloscope.

REMEBER to load the channels of the oscilloscope connected to the DAC output to 50 ohm, while the trigger
signal must be loaded on a high impedance (1 Mohm) input.

## Usage

In case a custom kernel is used, our hardware setup requires compiling the AD5624R kernel module support.

## Results

## References

This setup has been used to collect the results presented in [@RSI2014]

---
references:
- id: RSI2014
  title: Fast contactless vibrating structure characterization using real time FPGA-based digital signal processing: demonstrations with a passive wireless acoustic delay line probe and vision
  author:
  - family: G. Goavec-Merou, N. Chrétien, J.-M Friedt, P. Sandoz, G. Martin, M. Lenczner, S.Ballandras
  container-title: Rev. Sci. Instrum.
  volume: 85
  URL: 'https://aip.scitation.org/doi/10.1063/1.4861190'
  DOI: 10.1063/1.4861190
  issue: 1
  page: 015109-
  type: article-journal
  issued:
    year: 2014
    month: 1
---
