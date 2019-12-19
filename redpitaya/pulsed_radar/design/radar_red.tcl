variable fpga_ip $::env(OSCIMP_DIGITAL_IP)

set part_name xc7z010clg400-1
set project_name radar_red
set build_path tmp
set bd_path $build_path/$project_name.srcs/sources_1/bd/$project_name
set repo_path $fpga_ip

file delete -force $build_path

create_project $project_name $build_path -part $part_name
create_bd_design $project_name

# Set Path for the custom IP cores
set_property IP_REPO_PATHS $repo_path [current_project]
update_ip_catalog

# Create port
set switch_o [ create_bd_port -dir O switch_o ]
set switchn_o [ create_bd_port -dir O switchn_o ]

# ADC/DAC
source $repo_path/redpitaya_converters/redpitaya_converters.tcl
set converters [ create_bd_cell -type ip -vlnv ggm:cogen:redpitaya_converters:1.0 converters]
set_property -dict [ list CONFIG.ADC_SIZE 14 \
						CONFIG.ADC_EN true \
						CONFIG.DAC_EN true] $converters

# realToComplex
set realToComplex [ create_bd_cell -type ip \
	-vlnv ggm:cogen:convertRealToComplex:1.0 realToComplex ]
set_property -dict [ list CONFIG.DATA_SIZE {14}] $realToComplex

# genRadar
set genRadar [ create_bd_cell -type ip -vlnv ggm:cogen:gen_radar_prog:1.0 genRadar ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $genRadar

# dupplCheck
set dupplCheck [ create_bd_cell -type ip -vlnv ggm:cogen:dupplComplex_1_to_2:1.0 dupplCheck ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $dupplCheck

# checkValidBurst
set checkValidBurst [ create_bd_cell -type ip \
	-vlnv ggm:cogen:check_valid_burst:1.0 checkValidBurst ]
set_property -dict [ list CONFIG.ADDR_SIZE {10} \
	CONFIG.DFLT_LIMIT {311502} \
	CONFIG.DFLT_STOP_OFFSET {1023}] $checkValidBurst

# switchCheck
set switchCheck [ create_bd_cell -type ip -vlnv ggm:cogen:switchComplex:1.0 switchCheck ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $switchCheck

# dupplMean
set dupplMean [ create_bd_cell -type ip -vlnv ggm:cogen:dupplComplex_1_to_2:1.0 dupplMean ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $dupplMean

# meanVector
set meanVector [ create_bd_cell -type ip -vlnv ggm:cogen:mean_vector_axi:1.0 meanVector ]

# switchMean
set switchMean [ create_bd_cell -type ip -vlnv ggm:cogen:switchComplex:1.0 switchMean ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $switchMean

# dupplBranch
set dupplBranch [ create_bd_cell -type ip -vlnv ggm:cogen:dupplComplex_1_to_2:1.0 dupplBranch ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $dupplBranch

# branch direct
# dupplDirect
set dupplDirect [ create_bd_cell -type ip -vlnv ggm:cogen:dupplComplex_1_to_2:1.0 dupplDirect ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $dupplDirect

# dataDirect_to_ram
set dataDirect_to_ram [ create_bd_cell -type ip \
	-vlnv ggm:cogen:dataComplex_to_ram:1.0 dataDirect_to_ram ]
set_property -dict [ list CONFIG.DATA_SIZE {14} \
						CONFIG.USE_EOF {true} \
						CONFIG.NB_INPUT {1} \
						CONFIG.DATA_FORMAT {signed} \
						CONFIG.NB_SAMPLE {4096} ] $dataDirect_to_ram

# extract branch
# extractData
set extractData [ create_bd_cell -type ip \
	-vlnv ggm:cogen:extract_data_from_burst:1.0 extractData ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $extractData

# dupplExtract
set dupplExtract [ create_bd_cell -type ip -vlnv ggm:cogen:dupplComplex_1_to_2:1.0 dupplExtract ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $dupplExtract

# dataExtract_to_ram
set dataExtract_to_ram [ create_bd_cell -type ip \
	-vlnv ggm:cogen:dataComplex_to_ram:1.0 dataExtract_to_ram ]
set_property -dict [ list CONFIG.DATA_SIZE {14} \
						CONFIG.NB_INPUT {1} \
						CONFIG.DATA_FORMAT {signed} \
						CONFIG.NB_SAMPLE {4096} ] $dataExtract_to_ram

## FLOW TO DAC ##
# switchDAC
set switchDAC [ create_bd_cell -type ip -vlnv ggm:cogen:switchComplex:1.0 switchDAC ]
set_property -dict [ list CONFIG.DATA_SIZE {14} ] $switchDAC

# complexToReal
set complexToReal [ create_bd_cell -type ip -vlnv ggm:cogen:convertComplexToReal:1.0 complexToReal ]
set_property -dict [ list CONFIG.DATA_SIZE {14}] $complexToReal


# Create instance: ps7, and set properties
startgroup
set ps7 [ create_bd_cell -type ip -vlnv xilinx.com:ip:processing_system7:5.5 ps7 ]
set_property -dict [list CONFIG.PCW_IMPORT_BOARD_PRESET "$fpga_ip/preset/redpitaya_preset.xml" ] $ps7
endgroup

#=================#
# block <-> block #
#=================#

# ADC -> convert
connect_bd_intf_net -intf_net ltc2145_0_data_a \
	[get_bd_intf_pins realToComplex/dataI_in] \
	[get_bd_intf_pins converters/dataA_out]
connect_bd_intf_net -intf_net ltc2145_0_data_b \
	[get_bd_intf_pins realToComplex/dataQ_in] \
	[get_bd_intf_pins converters/dataB_out]
# convert -> genRadar
connect_bd_intf_net -intf_net convRealToComplex_genRadar \
  	[get_bd_intf_pins realToComplex/data_out] \
	[get_bd_intf_pins genRadar/data_in]
###
# genRadar -> check
# 1/genRadar -> duppl before check
connect_bd_intf_net -intf_net genRadar_duppl \
	[get_bd_intf_pins dupplCheck/data_in] \
	[get_bd_intf_pins genRadar/data_out]
# 2/duppl -> check
connect_bd_intf_net -intf_net duppl_check \
	[get_bd_intf_pins checkValidBurst/data_in] \
	[get_bd_intf_pins dupplCheck/data1_out]
# 3/check -> switch (val 0 (ie default)
connect_bd_intf_net -intf_net check_switch \
	[get_bd_intf_pins checkValidBurst/data_out] \
	[get_bd_intf_pins switchCheck/data1_in]
# 4/duppl -> switch after check (val 1 -> bypass)
connect_bd_intf_net -intf_net dupplCheck_check_switch \
	[get_bd_intf_pins dupplCheck/data2_out] \
	[get_bd_intf_pins switchCheck/data2_in]
###
# check -> mean
# 1/check -> duppl before mean
connect_bd_intf_net -intf_net check_duppl \
	[get_bd_intf_pins dupplMean/data_in] \
	[get_bd_intf_pins switchCheck/data_out]
# 2/duppl -> mean
connect_bd_intf_net -intf_net duppl_mean \
	[get_bd_intf_pins meanVector/data_in] \
	[get_bd_intf_pins dupplMean/data1_out]
# 3/mean -> switch after mean (val 0 -> use)
connect_bd_intf_net -intf_net mean_switch \
	[get_bd_intf_pins switchMean/data1_in] \
	[get_bd_intf_pins meanVector/data_out]
# 4/duppl before mean -> switch after mean (val 1 -> bypass)
connect_bd_intf_net -intf_net dupplMean_mean_switch \
	[get_bd_intf_pins switchMean/data2_in] \
	[get_bd_intf_pins dupplMean/data2_out]

# mean  -> duppl branch
connect_bd_intf_net -intf_net switchMean_dupplBranch \
	[get_bd_intf_pins dupplBranch/data_in] \
	[get_bd_intf_pins switchMean/data_out]

##
# direct branch
# dupplBranch -> duppl direct flow branch
connect_bd_intf_net -intf_net dupplBranch_dupplDirect \
	[get_bd_intf_pins dupplDirect/data_in] \
	[get_bd_intf_pins dupplBranch/data2_out]
# dupplDirect -> switch DAC (default 0 use direct) 
connect_bd_intf_net -intf_net dupplDirect_switchDAC \
	[get_bd_intf_pins switchDAC/data1_in] \
	[get_bd_intf_pins dupplDirect/data1_out]
# dupplDirect -> data_to_ram
connect_bd_intf_net -intf_net dupplDirect_data_to_ram \
	[get_bd_intf_pins dataDirect_to_ram/data1_in] \
	[get_bd_intf_pins dupplDirect/data2_out]

##
# extract point branch
# dupplBranch -> extract point branch
connect_bd_intf_net -intf_net dupplBranch_extractData \
	[get_bd_intf_pins extractData/data_in] \
	[get_bd_intf_pins dupplBranch/data1_out]
# extract -> dupplExtract
connect_bd_intf_net -intf_net extractData_dupplExtract \
	[get_bd_intf_pins dupplExtract/data_in] \
	[get_bd_intf_pins extractData/data_out]

# dupplExtract -> dataExtract_to_ram
connect_bd_intf_net -intf_net dupplExtract_dataExtract \
	[get_bd_intf_pins dataExtract_to_ram/data1_in] \
	[get_bd_intf_pins dupplExtract/data1_out]
# dupplExtract -> switch DAC (val 1 -> use point mode)
connect_bd_intf_net -intf_net dupplExtract_switchDAC \
	[get_bd_intf_pins switchDAC/data2_in] \
	[get_bd_intf_pins dupplExtract/data2_out]

###
# DAC output
# 1/switchDAC -> convert before DAC
connect_bd_intf_net -intf_net switchDAC_convert \
	[get_bd_intf_pins complexToReal/data_in] \
	[get_bd_intf_pins switchDAC/data_out]
# n/convert before DAC -> DAC
connect_bd_intf_net -intf_net complexToReal_DACA \
	[get_bd_intf_pins converters/dataA_in] \
	[get_bd_intf_pins complexToReal/dataI_out]
connect_bd_intf_net -intf_net complexToReal_DACB \
	[get_bd_intf_pins converters/dataB_in] \
	[get_bd_intf_pins complexToReal/dataQ_out]

# ADC/DAC (connect signals)
connect_bd_intf_net [get_bd_intf_pins $converters/phys_interface] \
	[get_bd_intf_ports phys_interface_0]

# Create port connections
connect_bd_net -net genRadar_switch_o [get_bd_ports switch_o] [get_bd_pins genRadar/switch_o]
connect_bd_net -net genRadar_switchn_o [get_bd_ports switchn_o] [get_bd_pins genRadar/switchn_o]

# AXI connection
apply_bd_automation -rule xilinx.com:bd_rule:processing_system7 \
	-config {make_external "FIXED_IO, DDR" Master "Disable" Slave "Disable"} $ps7

apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins genRadar/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins checkValidBurst/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins switchCheck/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins meanVector/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins switchMean/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins dataDirect_to_ram/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins extractData/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins dataExtract_to_ram/s00_axi]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config {Master "/ps7/M_AXI_GP0" Clk "Auto" } \
	[get_bd_intf_pins switchDAC/s00_axi]

# CANDR
connect_bd_net [get_bd_pins converters/adc_rst_i] \
	[get_bd_pins rst_ps7_125M/peripheral_reset]

save_bd_design

make_wrapper -files [get_files $bd_path/$project_name.bd] -top
set project_name_wrapper $project_name
append project_name_wrapper _wrapper
add_files -norecurse $bd_path/hdl/$project_name_wrapper.v

# Load any additional Verilog files in the project folder
set files [glob -nocomplain projects/$project_name/*.v projects/$project_name/*.sv]
if {[llength $files] > 0} {
	add_files -norecurse $files
}
## Load RedPitaya constraint files
add_files -norecurse -fileset constrs_1 radar_red.xdc
add_files -norecurse -fileset constrs_1 $repo_path/redpitaya_converters/redpitaya_converters.xdc
add_files -norecurse -fileset constrs_1 $repo_path/redpitaya_converters/redpitaya_converters_adc.xdc

set_property VERILOG_DEFINE {TOOL_VIVADO} [current_fileset]

set obj [get_runs impl_1]

set_property "needs_refresh" "1" $obj
# set the current impl run
current_run -implementation [get_runs impl_1]
puts "INFO: Project created: $project_name"
# set the current impl run
current_run -implementation [get_runs impl_1]
generate_target all [get_files $bd_path/$project_name.bd]
launch_runs synth_1 -jobs 4
wait_on_run synth_1
## do implementation
launch_runs impl_1 -jobs 4
wait_on_run impl_1
## make bit file
launch_runs impl_1 -to_step write_bitstream
wait_on_run impl_1
exit
