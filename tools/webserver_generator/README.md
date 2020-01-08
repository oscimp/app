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

* build the webserver app, need myproject.xml (same as module generator)

`./webserver_generator myproject.xml`
