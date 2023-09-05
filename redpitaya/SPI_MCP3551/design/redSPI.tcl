
# add SPI adapter to have a small simple reduce connector
add_ip_and_conf SPIAdapter SPIadap
# connect CPU SPI 0 interface to this adapter
connect_intf ps7 SPI_0 SPIadap S00_SPI

# connect adapter to FPGA pins
connect_to_fpga_pins SPIadap spi_clk_o spi_clk_o_0
connect_to_fpga_pins SPIadap spi_mosi_o spi_mosi_o_0
connect_to_fpga_pins SPIadap spi_miso_i spi_miso_i_0
connect_to_fpga_pins SPIadap spi_ss_o spi_ss_o_0
connect_to_fpga_pins SPIadap spi_ss1_o spi_ss1_o_0
connect_to_fpga_pins SPIadap spi_ss2_o spi_ss2_o_0
