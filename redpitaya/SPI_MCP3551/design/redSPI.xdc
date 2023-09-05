# common to PMOD1, PMOD2, PMOD3
## MOSI
set_property -dict {PACKAGE_PIN L16 IOSTANDARD LVCMOS33} [get_ports {spi_mosi_o_0}]
#set_property -dict {PACKAGE_PIN L16 IOSTANDARD LVCMOS33} [get_ports {SPI_0_0_io0_io}]
## MISO
set_property -dict {PACKAGE_PIN L14 IOSTANDARD LVCMOS33} [get_ports {spi_miso_i_0}]
#set_property -dict {PACKAGE_PIN L14 IOSTANDARD LVCMOS33} [get_ports {SPI_0_0_io1_io}]
## SCK
set_property -dict {PACKAGE_PIN K16 IOSTANDARD LVCMOS33} [get_ports {spi_clk_o_0}]
#set_property -dict {PACKAGE_PIN K16 IOSTANDARD LVCMOS33} [get_ports {SPI_0_0_sck_io}]
# PMOD1 CS
set_property -dict {PACKAGE_PIN K18 IOSTANDARD LVCMOS33 PULLTYPE PULLUP} [get_ports {spi_ss_o_0}]
#set_property -dict {PACKAGE_PIN K18 IOSTANDARD LVCMOS33} [get_ports {SPI_0_0_ss_io}]
# PMOD2 CS
set_property -dict {PACKAGE_PIN J16 IOSTANDARD LVCMOS33 PULLTYPE PULLUP} [get_ports {spi_ss1_o_0}]
#set_property -dict {PACKAGE_PIN J16 IOSTANDARD LVCMOS33} [get_ports {SPI_0_0_ss1_o}]
# PMOD3 CS
set_property -dict {PACKAGE_PIN K17 IOSTANDARD LVCMOS33 PULLTYPE PULLUP} [get_ports {spi_ss2_o_0}]
#set_property -dict {PACKAGE_PIN K17 IOSTANDARD LVCMOS33} [get_ports {SPI_0_0_ss2_o}]
