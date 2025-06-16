# Design double_iq_pid_vco

```
cd design
make xpr
make xml
make
cd ..
../../tools/module_generator/module_generator double_iq_pid_vco.xml
../../tools/webserver_generator/webserver_generator.py double_iq_pid_vco.xml
```

## Description

Double lock loop with modulation and demodulation. Used for a PLL in an optical fiber link.

## RF scheme of the design  

![double_iq_pid_vco](double_iq_pid_vco.png)

## Web server setup

Notice (red highlight) the output frequency, amplitude and the availability of the external reference 
clock (green square).

<img src="2025-06-13-113948_2704x1050_scrot.png">

## Experimental setup

<img src="redpit12.jpg">
