# module_generator

## Motivation

*module_generator* is designed with the aim of creating the skeleton
of an userspace application
(directory structure and ready-to-use files), as described through an
XML file provided by the user. This file defines the characteristics
of the corresponding design (drivers, memory addresses allocated to
each IP connected on the AXI bus).

According to the XML content, this tool generates
- a directory, called app, used to store all userspace files;
- a devicetree overlay containing attributes such as the name of the
bitstream to load, the list of modules to
   probe and the base address allocated to each module;
- a shell script used to:
	- copy the bitstream to */lib/firmware*;
	- unload and reload the devicetree overlay;
	- load mandatory drivers.
- a Makefile used to:
	- compile the userspace application and devicetree overlay;
	- install all binary files and script to a directory
	accessible by the target board
	(**$OSCIMP_DIGITAL_NFS/$BOARD_NAME/$BASE_DIR**).

## Compile/Install

*module_generator* requires tinyxml2 >= 6.2 with header files.

For debian users:
```bash
# apt-get install libtinyxml2-6a libtinyxml2-dev
```
or equivalent (see ```apt-cache search```, or your distribution *package
manager* for correct package name and version).

To compile, use ```make``` and
```bash
make install
```
(as root) to install, by default in */usr/local/bin* or
```bash
make install INSTALL_DIR=/somewhere
```
to install *module_generator* in */somewhere* directory.

## Usage

### XML file
The following sample xml code is an example of file used by *module_generator*
```xml
<?xml version="1.0" encoding="utf-8"?>
<project name="demo" version="1.0">
	<options>
		<option target="makefile" name="DONT_USE_LIB">1</option>
		<option target="makefile" name="CFLAGS">-Iopt -g -Wall</option>
		<option target="makefile" name="CFLAGS">-O4</option>
		<option target="makefile" name="LDFLAGS">-lm -lfftw</option>
	</options>
	<ips>
		<ip name ="dataComplex_to_ram" >
			<instance name="data1600" id = "0"
				base_addr="0x43C00000" addr_size="0x00ff" />
			<instance name="data1601" id = "1"
				base_addr="0x43C10000" addr_size="0x00ff" />
		</ip>
		<ip name="firReal" >
			<instance name="fir1600" id = "0"
				base_addr="0x43C20000" addr_size="0x00ff" />
		</ip>
		<ip name="add_const" >
			<instance name="add00" id = "0"
				base_addr="0x43C30000" addr_size="0x00ff" />
		</ip>
	</ips>
</project>
```

where:
- *name* attribute for *project* node is the name of the project (used for
   binary application name, bitstream and devicetree base name;
- *name* attribute for *ip* node is the name of an IP used by this application.
   To produce the devicetree and shell script, *module_generator* uses this
   information to, though *$OSCIMP_DIGITAL_IP*/ip.xml, know which driver must be
   used and finally, though *$OSCIMP_DIGITAL_DRIVER*/driver.xml, informations about the driver;
- *instance* refers to an instance of parent *ip* node,
	- *name* is used to create, at runtime, a /dev/xxx pseudo file
	- *base_addr* is the start address of the memory segment shared
	between the CPU and the FPGA
	- *addr_size* is the length of the memory segment allocated for this driver
	  instance.
- option (optional): use to pass flags or informations:
	- target: defines target file (currently only makefile);
	- name: variable name, may be a compiler flag or an variable to add
	- value: corresponding value.

#### Previous XML structure
The following sample xml code is an example of file used by *module_generator*
```xml
<?xml version="1.0" encoding="utf-8"?>
<drivers name="demo" version="1.0">
	<options>
		<option target="makefile" name="DONT_USE_LIB">1</option>
		<option target="makefile" name="CFLAGS">-Iopt -g -Wall</option>
		<option target="makefile" name="CFLAGS">-O4</option>
		<option target="makefile" name="LDFLAGS">-lm -lfftw</option>
	</options>
	<driver name ="data16Complex_to_ram" >
		<board_driver name="data1600" id = "0"
			base_addr="0x43C00000" addr_size="0x00ff" />
		<board_driver name="data1601" id = "1"
			base_addr="0x43C10000" addr_size="0x00ff" />
	</driver>
	<driver name="fir16bits" >
		<board_driver name="fir1600" id = "0"
			base_addr="0x43C20000" addr_size="0x00ff" />
	</driver>
	<driver name="add_const" >
		<board_driver name="add00" id = "0"
			base_addr="0x43C30000" addr_size="0x00ff" />
	</driver>
</drivers>
```

where:
- *name* attribute for *drivers* node is the name of the project (used for
   binary application name, bitstream and devicetree base name;
- *name* attribute for *driver* node is the name of a driver used by this
   application. This driver is located in a subdirectory of
   *$OSCIMP_DIGITAL_DRIVER*. To obtain information about this driver for
   creating the devicetree, *module_generator* uses
   *$OSCIMP_DIGITAL_DRIVER/driver.xml*
- board driver refers to an instance of IP, using the parent driver node,
	- *name* is used to create, at runtime, a /dev/xxx pseudo file
	- *base_addr* is the start address of the memory segment shared
	between the CPU and the FPGA
	- *addr_size* is the length of the memory segment allocated for this driver
	  instance.
- option (optional): use to pass flags or informations:
	- target: defines target file (currently only makefile);
	- name: variable name, may be a compiler flag or an variable to add
	- value: corresponding value.
### command line

to generate application files you need :
```bash
module_generator [-dts] [-nodts [-legacy]] xmlfile.xml
```

with :
- *-dts* to force devicetree source (dts) file generation (default option);
- *-nodts* to generate a board_driver instead of dts;
- *legacy* to use the old */dev/xdevcfg* to program the FPGA instead of
*/sys/class/fpga_manager/fpga0/firmware* (only available with *-nodts*)
- as last argument your xml file

Note: it is not possible to use both *-nodts* and *-dts*

## Add a driver

module_generator uses $OSCIMP_DIGITAL_DRIVER/driver.xml
to obtain information about each driver (mainly, the compatible attribute
for dts case or the struct name for board_driver case). When a new
driver is added in the linux_driver directory, and module_generator is
to be used
with this driver, an entry in driver.xml must be added such as:

```xml
<driver filename="driver_filename"
    compatible="vendor,driver_name"
    name="driver_name" plat="plat_driver_name">
</driver>

```
where:
- *filename* is the file name without .ko;
- *compatible* is used for devicetree *compatible* attribute (see devicetree
   rules for *vendor,driver_name*);
- *name* is the name used in xml to refer to this entry;
- *plat* is, in nodts mode, the name of the platform data used to provide
   information through the board driver and core driver.

## Add an IP
*module_generator* uses *$OSCIMP_DIGITAL_IP/ip.xml* to obtain relationship
between an IP and a driver. When a new IP is added, an entry in *ip.xml* must be
added such as:
```xml
<ip name="nco_counter"
	driver="nco_counter" />
```
where:
- *name* is the IP name;
- *driver* is the entry in *$OSCIMP_DIGITAL_DRIVER/driver.xml*
