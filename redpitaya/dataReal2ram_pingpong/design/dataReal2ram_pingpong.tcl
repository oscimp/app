set nb_data 16384
set data_sz 16

set nb_data_log2 [expr {[::tcl::mathfunc::ceil [expr {log($nb_data)/[expr log(2)]}]]}]

## Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
    CLOCK_DUTY_CYCLE_STABILIZER_EN false }
connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0

add_ip_and_conf ram_to_dataReal axiToRam {
	COEFF_ADDR_SIZE $nb_data_log2 \
	COEFF_SIZE $data_sz \
	DECIM_FACTOR_POW 14 }
connect_proc axiToRam s00_axi 0x00000
connect_intf redpitaya_converters_0 clk_o axiToRam ref_clk_i
connect_intf redpitaya_converters_0 rst_o axiToRam ref_rst_i

add_ip_and_conf dupplReal duppl {
	DATA_SIZE $data_sz \
	NB_OUTPUT 2 }
connect_intf axiToRam data_out duppl data_in

add_ip_and_conf dataReal_to_ram data2ram {
	DATA_SIZE $data_sz \
	NB_INPUT 1 \
	NB_SAMPLE $nb_data }
connect_proc data2ram s00_axi 0x10000
connect_intf duppl data1_out data2ram data1_in

add_ip_and_conf dataReal_to_ram_pingpong data2ram_pp {
	DATA_SIZE $data_sz \
	NB_INPUT 1 \
	NB_SAMPLE $nb_data }
connect_proc data2ram_pp s00_axi 0x20000
connect_intf duppl data2_out data2ram_pp data1_in

connect_proc_rst redpitaya_converters_0 adc_rst_i
