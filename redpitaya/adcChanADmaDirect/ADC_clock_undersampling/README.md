Hardware modifications of the 14-bit Red Pitaya (also known as STEMlab 125-14) described
in report.pdf, and the associated KiCAD files (courtesy of Gilles Martin, FEMTO-ST, France)
for undersampling by getting rid of the unbalanced-balanced amplifier also acting as
low pass filter. Replacing the active amplifier with a broadband balun (tested over the
whole track-and-hold range up to 875 MHz input frequency) requires soldering three tiny
wires (differential pair + Vref) on each channel at your own risks after removing the
inductors connecting the differential amplifier output to the ADC inputs. The Vref signal
trace must be cut before soldering a wire to the via pad whose varnish will have been
removed with a sharp blade.
