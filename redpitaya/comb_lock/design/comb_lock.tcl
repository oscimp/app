# comb_lock.tcl
#
# currently working only with Redpitaya 14!
# if you wish to implement operation on Redpitaya 16, 
# the hardware (board) must be modified, such that the DAC output will have DC coupling. 
# Redpitaya 16 by default supports only AC-coupled outputs.
#
# device XC7Z010 / (XC7Z020 - Redpitaya16)
#
#
#
# change to upper
set up_board [string toupper $::env(BOARD_NAME)]
if {$up_board == "REDPITAYA"} {
    set ADC_SIZE 14
} else {
    if {$up_board == "REDPITAYA16"} {
        set ADC_SIZE 16
    }
}

#-------------------------------------------------------------------------
#                        Constants 
#-------------------------------------------------------------------------
if {$up_board == "REDPITAYA16"} {
	set ADC_SIZE 16
	set ADC_SZ_PLUS_1 17
	set ADC_SZ_PLUS_1_TIMES_INT16 33
	set ADC_SZ_PLUS_1_TIMES_INT16_PLUS_1 34
} else {
	set ADC_SIZE 14
	set ADC_SZ_PLUS_1 15
	set ADC_SZ_PLUS_1_TIMES_INT16 31
	set ADC_SZ_PLUS_1_TIMES_INT16_PLUS_1 32
}

# in Redpitaya 14 and Redpitaya 16 both have 14 bit DAC
set DAC_SIZE 14

set INT16_SIZE 16
set INT32_SIZE 32

# Number of samples for fast RAM dump
# Xilinx ZYNQ XC7Z010 SoC has limitation of 2.1Mb BRAM elements (60x36kbit)
# 60x36x1024/8 = 276,480Bytes = 34560  2byte (I,Q) pairs. Some BRAM has to be left for design,
# so we choose 16384 elements.
set FAST_RAM_NUMEL 16384

# constant LPF_COEFF defines the IIR LP filter cutoff frequency as
set LPF_COEFF 16 

# constants for CORDIC and phase unwrap
#  number of ATAN iteration for given output precision DATA_SIZE = NB_ITER-1+4
set NB_ITER 13 
# Scaled PI value for ATAN PI_VAL = 3.141592*2**(NB_ITER-1)
set PI_VAL 12868 
# DATA_OUT_SIZE = NB_ITER-1+4
set CORDIC_PHASE_OUT_SIZE 16

# data width after phase unwrapping algorithm
set AFTER_UNWRAP_SIZE 32
# PI regulators integral shift 
set FAST_INTEGRATOR_SHIFT 8
set SLOW_INTEGRATOR_SHIFT 18

#-------------------------------------------------------------------------
#                        Block instantiation
#-------------------------------------------------------------------------
# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {false} \
	ADC_SIZE $ADC_SIZE }

connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0
connect_proc_rst redpitaya_converters_0 adc_rst_i

# Create instance: dupplReal_1_to_2_0, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_0 {
	DATA_SIZE $ADC_SIZE }
	
# Create instance: dupplReal_1_to_2_1, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_1 {
	DATA_SIZE $ADC_SIZE }

# Create instance : const_real_0, and set properties
add_ip_and_conf const_real const_real_0 {
	DATA_SIZE $ADC_SIZE\
	INT_REAL_PART_OUT_VALUE {0}}

connect_intf redpitaya_converters_0 clk_o const_real_0 ref_clk_i
connect_intf redpitaya_converters_0 rst_o const_real_0 ref_rst_i

# Create instance : const_real_1, and set properties
add_ip_and_conf const_real const_real_1 {
	DATA_SIZE $ADC_SIZE\
	INT_REAL_PART_OUT_VALUE {0}}

connect_intf redpitaya_converters_0 clk_o const_real_1 ref_clk_i
connect_intf redpitaya_converters_0 rst_o const_real_1 ref_rst_i

# Create instance : iir_lpf_real_0, and set properties
add_ip_and_conf iir_lpf_real iir_lpf_real_0 {
	DATA_WIDTH $ADC_SIZE \ 
	FILTER_COEFF_TWOS_POWER $LPF_COEFF }

# Create instance : iir_lpf_real_1, and set properties
add_ip_and_conf iir_lpf_real iir_lpf_real_1 {
	DATA_WIDTH $ADC_SIZE \ 
	FILTER_COEFF_TWOS_POWER $LPF_COEFF }

# Create instance : adder_substracter_real_0, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_real_0 {
	opp {subtract}\
	DATA_SIZE $ADC_SIZE}

# Create instance : addder_substracter_real_1, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_real_1 {
	opp {subtract}\
	DATA_SIZE $ADC_SIZE}

# Create instance : switchReal_0, and set properties
add_ip_and_conf switchReal switchReal_0 {
	DATA_SIZE $ADC_SIZE\
	DEFAULT_INPUT {0}}

connect_proc switchReal_0 s00_axi 0x10000

# Create instance : switchReal_1, and set properties
add_ip_and_conf switchReal switchReal_1 {
	DATA_SIZE $ADC_SIZE\
	DEFAULT_INPUT {0}}

connect_proc switchReal_1 s00_axi 0x20000

# Create instance: dupplReal_1_to_2_2, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_2 {
	DATA_SIZE $ADC_SZ_PLUS_1 }

# Create instance: dupplReal_1_to_2_3, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_3 {
	DATA_SIZE $ADC_SZ_PLUS_1 }

# Create instance: convertRealToComplex_0, and set properties
add_ip_and_conf convertRealToComplex convertRealToComplex_0 {
	DATA_SIZE $ADC_SZ_PLUS_1 }

# Create instance: expanderComplex_0, and set properties
if {$up_board != "REDPITAYA16"} {
	add_ip_and_conf expanderComplex expanderComplex_0 {
		DATA_IN_SIZE $ADC_SZ_PLUS_1\
		DATA_OUT_SIZE $INT16_SIZE}
}
#Create instance: dataComplex_to_ram_0, and set properties
add_ip_and_conf dataComplex_to_ram dataComplex_to_ram_0 {
	DATA_SIZE $INT16_SIZE\
	NB_INPUT {1}\
	NB_SAMPLE $FAST_RAM_NUMEL}

connect_proc dataComplex_to_ram_0 s00_axi 0xA0000

# Create instance: dupplReal_1_to_2_4, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_4 {
	DATA_SIZE $ADC_SZ_PLUS_1 }

# Create instance: dupplReal_1_to_2_5, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_5 {
	DATA_SIZE $ADC_SZ_PLUS_1 }

# Create instance: multiplierReal_0, and set properties
add_ip_and_conf multiplierReal multiplierReal_0 {
	DATA1_IN_SIZE $ADC_SZ_PLUS_1 \
	DATA2_IN_SIZE $INT16_SIZE \
	DATA_OUT_SIZE $ADC_SZ_PLUS_1_TIMES_INT16}

# Create instance: multiplierReal_1, and set properties
add_ip_and_conf multiplierReal multiplierReal_1 {
	DATA1_IN_SIZE $ADC_SZ_PLUS_1 \
	DATA2_IN_SIZE $INT16_SIZE \
	DATA_OUT_SIZE $ADC_SZ_PLUS_1_TIMES_INT16}

# Create instance: multiplierReal_2, and set properties
add_ip_and_conf multiplierReal multiplierReal_2 {
	DATA1_IN_SIZE $ADC_SZ_PLUS_1 \
	DATA2_IN_SIZE $INT16_SIZE \
	DATA_OUT_SIZE $ADC_SZ_PLUS_1_TIMES_INT16}

# Create instance: multiplierReal_3, and set properties
add_ip_and_conf multiplierReal multiplierReal_3 {
	DATA1_IN_SIZE $ADC_SZ_PLUS_1 \
	DATA2_IN_SIZE $INT16_SIZE \
	DATA_OUT_SIZE $ADC_SZ_PLUS_1_TIMES_INT16}

# Create instance: matrix_mxi, and set properties
# TODO what is meaning of DATA{A,B}_DEFAULT_OUT: integer value?
# in the case if there is no data for matrix on the AXI bus, 
# we will set the matrix entries to create an identity matrix.
add_ip_and_conf axi_to_dac matrix_mxi {
	DATA_SIZE $INT16_SIZE \
	SYNCHRONIZE_CHAN {true}\
	DATAA_DEFAULT_OUT {1}\
	DATAA_EN_ALWAYS_HIGH {true}\
	DATAB_DEFAULT_OUT {0}\
	DATAB_EN_ALWAYS_HIGH {true}}

connect_intf redpitaya_converters_0 clk_o matrix_mxi ref_clk_i
connect_intf redpitaya_converters_0 rst_o matrix_mxi ref_rst_i
connect_proc matrix_mxi s00_axi 0x30000

# Create instance: matrix_myq, and set properties
# TODO what is meaning of DATA{A,B}_DEFAULT_OUT: integer value?
# in the case if there is no data for matrix on the AXI bus, 
# we will set the matrix entries to create an identity matrix.
add_ip_and_conf axi_to_dac matrix_myq {
	DATA_SIZE $INT16_SIZE \
	SYNCHRONIZE_CHAN {true}\
	DATAA_DEFAULT_OUT {0}\
	DATAA_EN_ALWAYS_HIGH {true}\
	DATAB_DEFAULT_OUT {1}\
	DATAB_EN_ALWAYS_HIGH {true}}

connect_intf redpitaya_converters_0 clk_o matrix_myq ref_clk_i
connect_intf redpitaya_converters_0 rst_o matrix_myq ref_rst_i
connect_proc matrix_myq s00_axi 0x40000

# Create instance : adder_substracter_real_3, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_real_3 {
	opp {add}\
	DATA_SIZE $ADC_SZ_PLUS_1_TIMES_INT16}

# Create instance : adder_substracter_real_4, and set properties
add_ip_and_conf adder_substracter_real adder_substracter_real_4 {
	opp {add}\
	DATA_SIZE $ADC_SZ_PLUS_1_TIMES_INT16}

# Create instance: convertRealToComplex_1, and set properties
add_ip_and_conf convertRealToComplex convertRealToComplex_1 {
	DATA_SIZE $ADC_SZ_PLUS_1_TIMES_INT16_PLUS_1 }

# IR 8-Feb-2022 
# Create instance: dupplComplex_0, and set properties
add_ip_and_conf dupplComplex dupplComplex_0 {
	NB_OUTPUT {2}\
	DATA_SIZE $ADC_SZ_PLUS_1_TIMES_INT16_PLUS_1 }

# Create instance: shifterComplex_0, and set properties
add_ip_and_conf shifterComplex shifterComplex_0 {
	DATA_IN_SIZE $ADC_SZ_PLUS_1_TIMES_INT16_PLUS_1 \
	DATA_OUT_SIZE $INT16_SIZE }	

#Create instance: dataComplex_to_ram_1, and set properties
add_ip_and_conf dataComplex_to_ram dataComplex_to_ram_1 {
	DATA_SIZE $INT16_SIZE\
	NB_INPUT {1}\
	NB_SAMPLE $FAST_RAM_NUMEL}

connect_proc dataComplex_to_ram_1 s00_axi 0xB0000

# Create instance: cordicAtan_0, and set properties
# DATA_OUT_SIZE = NB_ITER-1+4
# PI_VAL  = round(3.141592*2**(NB_ITER-1))
add_ip_and_conf cordicAtan cordicAtan_0 {
	DATA_IN_SIZE $ADC_SZ_PLUS_1_TIMES_INT16_PLUS_1\
	NB_ITER $NB_ITER\
	DATA_OUT_SIZE $CORDIC_PHASE_OUT_SIZE\
	PI_VALUE $PI_VAL\
	}

# Create instance: dupplReal_1_to_2_6, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_6 {
	DATA_SIZE $CORDIC_PHASE_OUT_SIZE }

# Create instance: unwrap_phase_diff_0, and set parameters
add_ip_and_conf unwrap_phase_diff unwrap_phase_diff_0 {
	DATA_WIDTH $CORDIC_PHASE_OUT_SIZE\
	DATA_OUT_WIDTH $AFTER_UNWRAP_SIZE\
	PI_VALUE $PI_VAL\
	ESTIMATION_METHOD {2} }

# Create instance: shifterReal_dyn_0, and set properties
add_ip_and_conf shifterReal_dyn shifterReal_dyn_0 {
	DATA_IN_SIZE $AFTER_UNWRAP_SIZE \
	DATA_OUT_SIZE $CORDIC_PHASE_OUT_SIZE }

connect_proc shifterReal_dyn_0 s00_axi 0x50000

# Create instance : switchReal_2, and set properties
add_ip_and_conf switchReal switchReal_2 {
	DATA_SIZE $CORDIC_PHASE_OUT_SIZE\
	DEFAULT_INPUT {0} }

connect_proc switchReal_2 s00_axi 0x60000

# Create instance: dupplReal_1_to_2_7, and set properties
add_ip_and_conf dupplReal_1_to_2 dupplReal_1_to_2_7 {
	DATA_SIZE $CORDIC_PHASE_OUT_SIZE }

# Create instance: frequency_offset, and set properties
add_ip_and_conf add_constReal frequency_offset {
	DATA_IN_SIZE $CORDIC_PHASE_OUT_SIZE \
	DATA_OUT_SIZE $CORDIC_PHASE_OUT_SIZE }
connect_proc frequency_offset s00_axi 0x90000

# Create instance: pidv3_axi_0, and set properties
add_ip_and_conf pidv3_axi pidv3_axi_0 {
	PSR {0} \
	ISR $FAST_INTEGRATOR_SHIFT \
	DSR {0} \
	P_SIZE {16} \
	I_SIZE {16} \
	D_SIZE {16} \
	DATA_IN_SIZE $CORDIC_PHASE_OUT_SIZE\
	DATA_OUT_SIZE {16}}

connect_proc pidv3_axi_0 s00_axi 0x70000

# Create instance: pidv3_axi_1, and set properties
add_ip_and_conf pidv3_axi pidv3_axi_1 {
	PSR {0} \
	ISR $SLOW_INTEGRATOR_SHIFT \
	DSR {0} \
	P_SIZE {16} \
	I_SIZE {16} \
	D_SIZE {16} \
	DATA_IN_SIZE $CORDIC_PHASE_OUT_SIZE\
	DATA_OUT_SIZE {16}}

connect_proc pidv3_axi_1 s00_axi 0x80000
# Create instance: shifterReal_0, and set properties
add_ip_and_conf shifterReal shifterReal_0 {
	DATA_IN_SIZE {16} \
	DATA_OUT_SIZE $DAC_SIZE }
# Create instance: shifterReal_1, and set properties
add_ip_and_conf shifterReal shifterReal_1 {
	DATA_IN_SIZE {16} \
	DATA_OUT_SIZE $DAC_SIZE }

#-------------------------------------------------------------------------
#                        Block connections
#-------------------------------------------------------------------------
connect_intf dupplReal_1_to_2_0 data_in redpitaya_converters_0 dataA_out
connect_intf dupplReal_1_to_2_1 data_in redpitaya_converters_0 dataB_out

connect_intf dupplReal_1_to_2_0 data1_out iir_lpf_real_0 data_in
connect_intf dupplReal_1_to_2_1 data1_out iir_lpf_real_1 data_in

connect_intf dupplReal_1_to_2_0 data2_out adder_substracter_real_0 data1_in
connect_intf dupplReal_1_to_2_1 data2_out adder_substracter_real_1 data1_in

connect_intf const_real_0 data_out switchReal_0 data1_in
connect_intf const_real_1 data_out switchReal_1 data1_in

connect_intf iir_lpf_real_0 data_out switchReal_0 data2_in 
connect_intf iir_lpf_real_1 data_out switchReal_1 data2_in

connect_intf switchReal_0 data_out adder_substracter_real_0 data2_in
connect_intf switchReal_1 data_out adder_substracter_real_1 data2_in

connect_intf adder_substracter_real_0 data_out dupplReal_1_to_2_2 data_in
connect_intf adder_substracter_real_1 data_out dupplReal_1_to_2_3 data_in

connect_intf dupplReal_1_to_2_2 data2_out convertRealToComplex_0 dataI_in
connect_intf dupplReal_1_to_2_3 data2_out convertRealToComplex_0 dataQ_in
# expanderComplex_0  is conditionally bypassed if 16 bit ADC is used

#
if {$up_board == "REDPITAYA16"} {
	connect_intf convertRealToComplex_0 data_out dataComplex_to_ram_0 data1_in
} else {
	connect_intf convertRealToComplex_0 data_out expanderComplex_0 data_in
	connect_intf expanderComplex_0 data_out dataComplex_to_ram_0 data1_in
}
#--------
connect_intf dupplReal_1_to_2_2 data1_out dupplReal_1_to_2_4 data_in
connect_intf dupplReal_1_to_2_3 data1_out dupplReal_1_to_2_5 data_in

connect_intf dupplReal_1_to_2_4 data1_out multiplierReal_0 data1_in
connect_intf dupplReal_1_to_2_4 data2_out multiplierReal_1 data1_in

connect_intf dupplReal_1_to_2_5 data1_out multiplierReal_2 data1_in
connect_intf dupplReal_1_to_2_5 data2_out multiplierReal_3 data1_in

connect_intf matrix_mxi dataA_out multiplierReal_0 data2_in
connect_intf matrix_mxi dataB_out multiplierReal_1 data2_in

connect_intf matrix_myq dataA_out multiplierReal_2 data2_in
connect_intf matrix_myq dataB_out multiplierReal_3 data2_in

connect_intf multiplierReal_0 data_out adder_substracter_real_3 data1_in
connect_intf multiplierReal_1 data_out adder_substracter_real_4 data1_in
connect_intf multiplierReal_2 data_out adder_substracter_real_3 data2_in
connect_intf multiplierReal_3 data_out adder_substracter_real_4 data2_in

connect_intf adder_substracter_real_3 data_out convertRealToComplex_1 dataI_in
connect_intf adder_substracter_real_4 data_out convertRealToComplex_1 dataQ_in

connect_intf convertRealToComplex_1 data_out dupplComplex_0 data_in
connect_intf dupplComplex_0 data1_out cordicAtan_0 data_in
connect_intf dupplComplex_0 data2_out shifterComplex_0 data_in

connect_intf shifterComplex_0 data_out dataComplex_to_ram_1 data1_in

#connect_intf convertRealToComplex_1 data_out cordicAtan_0 data_in
connect_intf cordicAtan_0 data_out dupplReal_1_to_2_6 data_in

connect_intf dupplReal_1_to_2_6 data1_out unwrap_phase_diff_0 data_in
connect_intf dupplReal_1_to_2_6 data2_out switchReal_2 data1_in
connect_intf unwrap_phase_diff_0 data_out shifterReal_dyn_0 data_in
connect_intf shifterReal_dyn_0 data_out switchReal_2 data2_in

connect_intf switchReal_2 data_out frequency_offset data_in
connect_intf frequency_offset data_out dupplReal_1_to_2_7 data_in
connect_intf dupplReal_1_to_2_7 data1_out pidv3_axi_0 data_in
connect_intf dupplReal_1_to_2_7 data2_out pidv3_axi_1 data_in

connect_intf pidv3_axi_0 data_out shifterReal_0 data_in
connect_intf pidv3_axi_1 data_out shifterReal_1 data_in
connect_intf shifterReal_0 data_out redpitaya_converters_0 dataA_in
connect_intf shifterReal_1 data_out redpitaya_converters_0 dataB_in

# END of file
