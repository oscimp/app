webserver generator
===================

Dependencies
------------
- REMI python package https://github.com/dddomodossola/remi.git
- lxmp python package
- liboscimp_fgpa python wrap (see fpga_lib)

Test it
-------
* clone REMI repo and add it to buildroot

`cp Makefile %your_REMI_repo`

`make install_python_package` or `make install_python_package_ssh IP=XXX.XXX.XXX.XXX`

* build the webserver application by providing the XML configuration file myproject.xml: this configuration file is the 
same than the one used to configure [module generator](https://github.com/oscimp/app/tree/master/tools/module_generator).

`./webserver_generator myproject.xml`
