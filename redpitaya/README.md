Various applications for the Red Pitaya board used at the Time & Frequency department
of the [FEMTO-ST](http://www.femto-st.fr) institute in the framework of the Oscillator Instabilty Measurement Platform,
most significantly for optical link locks.

Documentation on these applications can be found at https://github.com/sdenis6/Base_Designs_tuto

Two applications not related to optical frequency link locks:
* adcChanADmaDirect dumps the full speed output of an ADC to memory through DMA for further processing
* pulsed_radar is a 2.45 pulsed RADAR design for fast proving Surface Acoustic Wave reflective delay lines

**Issues with webserver:**

Hardcoded webservers are prone to compatibility obsolescence as the surrounding frameworks (REMI) are evolving. It would be safer to regenerate the webserver in case of version updates:
```bash
cd design
make project  # assumes Vivado is initialized and in the PATH: generate project file
make xml      # generate XML file
cd ..
${OSCIMP_DIGITAL_APP}/tools/webserver_generator/webserver_generator.py *.xml
```
will regenerate the webserver.py in the app directory.
