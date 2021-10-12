# change to upper
set up_board [string toupper $board_name]
if {$up_board == "REDPITAYA"} {
	set ADC_SIZE 14
	set DAC_SIZE 14

} else {
    if {$up_board == "REDPITAYA16"} {
        set ADC_SIZE 16
	set DAC_SIZE 16
    }
}
set DATA_OUT_FIR_SIZE 32
set DATA_SIZE 16
#number of ATAN iteration for given output precision NB_ITER = DATA_SIZE-1+4
set NB_ITER 13 
#scaled PI value for ATAN PI_VAL = 3.141592*2**(NB_ITER-1)
set PI_VAL 12868

set PID_CONST_SIZE 16
set PID_OUT_SIZE 32

# Create instance: redpitaya_converters_0, and set properties
add_ip_and_conf redpitaya_converters redpitaya_converters_0 {
	CLOCK_DUTY_CYCLE_STABILIZER_EN {TRUE} \
	ADC_SIZE $ADC_SIZE }

connect_to_fpga_pins redpitaya_converters_0 phys_interface phys_interface_0
connect_proc_rst redpitaya_converters_0 adc_rst_i

# Create instance: mixer_sin_0, and set properties
add_ip_and_conf mixer_sin mixer_sin_0 {
	DATA_IN_SIZE $ADC_SIZE \
	DATA_OUT_SIZE $DATA_SIZE \
	NCO_SIZE {16} }

connect_intf redpitaya_converters_0 dataA_out mixer_sin_0 data_in

# Create instance: demod1_nco, and set properties
add_ip_and_conf nco_counter demod1_nco {
	COUNTER_SIZE {40} \
	DATA_SIZE {16} \
	LUT_SIZE {12} }

connect_intf redpitaya_converters_0 clk_o demod1_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o demod1_nco ref_rst_i
connect_intf demod1_nco sine_out mixer_sin_0 nco_in

connect_proc demod1_nco s00_axi 0x70000

# Create instance: dupplComplex_0, and set properties
add_ip_and_conf dupplComplex dupplComplex_0 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}

connect_intf mixer_sin_0 data_out dupplComplex_0 data_in

# Create instance: DemodFIR125MSa_125MSa, and set properties
add_ip_and_conf firComplex DemodFIR_125MSa_125MSa {
	DATA_IN_SIZE $DATA_SIZE \
	DATA_OUT_SIZE $DATA_OUT_FIR_SIZE \
	DECIMATE_FACTOR {1} \
	NB_COEFF {25} }
connect_intf dupplComplex_0 data1_out DemodFIR_125MSa_125MSa data_in
connect_proc DemodFIR_125MSa_125MSa s00_axi 0xB0000
#connect_proc DemodFIR125MSa_125MSa s00_axi s00_axi_aclk s00_axi_reset 0xB0000


# Create instance: shifterComplex_0, and set properties
add_ip_and_conf shifterComplex shifterComplex_0 {
	DATA_IN_SIZE $DATA_OUT_FIR_SIZE \
	DATA_OUT_SIZE $DATA_SIZE }


# Create instance: DemodFIR125MSa_25MSa, and set properties
add_ip_and_conf firComplex DemodFIR_125MSa_25MSa {
	DATA_IN_SIZE $DATA_SIZE \
	DATA_OUT_SIZE $DATA_OUT_FIR_SIZE \
	DECIMATE_FACTOR {5} \
	NB_COEFF {25} }

connect_intf dupplComplex_0 data2_out DemodFIR_125MSa_25MSa data_in
connect_intf DemodFIR_125MSa_125MSa data_out shifterComplex_0 data_in
connect_proc DemodFIR_125MSa_25MSa s00_axi 0xA0000

# Create instance: shifterComplex_1, and set properties
add_ip_and_conf shifterComplex shifterComplex_1 {
	DATA_IN_SIZE $DATA_OUT_FIR_SIZE \
	DATA_OUT_SIZE $DATA_SIZE }

connect_intf DemodFIR_125MSa_25MSa data_out shifterComplex_1 data_in

# Create instance: dupplComplex_1, and set properties
add_ip_and_conf dupplComplex dupplComplex_1 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}
connect_intf shifterComplex_1 data_out dupplComplex_1 data_in


# Create instance: DemodFIR25MSa_5MSa, and set properties
add_ip_and_conf firComplex DemodFIR_25MSa_5MSa {
	DATA_IN_SIZE $DATA_SIZE \
	DATA_OUT_SIZE $DATA_OUT_FIR_SIZE \
	DECIMATE_FACTOR {5} \
	NB_COEFF {25} }
connect_intf dupplComplex_1 data2_out DemodFIR_25MSa_5MSa data_in
connect_proc DemodFIR_25MSa_5MSa s00_axi  0x90000

# Create instance: shifterComplex_2, and set properties
add_ip_and_conf shifterComplex shifterComplex_2 {
	DATA_IN_SIZE $DATA_OUT_FIR_SIZE \
	DATA_OUT_SIZE $DATA_SIZE }

connect_intf DemodFIR_25MSa_5MSa data_out shifterComplex_2 data_in

# Create instance: dupplComplex_2, and set properties
add_ip_and_conf dupplComplex dupplComplex_2 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}

connect_intf shifterComplex_2 data_out dupplComplex_2 data_in

#*******************************
# Since Zynq XC7Z010 has only 80 DSP48 units, the last filter will not fit in.
# Thus the branch with DemodFIR_5MSa_1MSa is commented-out and removed.
# It is replaced by a following direct cionnection:
#connect_intf dupplComplex_2 data2_out DemodFIR_5MSa_1MSa data_in

# Create instance: DemodFIR5MSa_1MSa, and set properties
#add_ip_and_conf firComplex DemodFIR5MSa_1MSa {
#	DATA_IN_SIZE $DATA_SIZE \
#	DATA_OUT_SIZE $DATA_OUT_FIR_SIZE \
#	DECIMATE_FACTOR {1} \
#	NB_COEFF {25} }

#connect_proc DemodFIR5MSa_1MSa s00_axi 0x80000
#connect_intf DemodFIR_5MSa_1MSa data_out shifterComplex_3 data_in

# Create instance: shifterComplex_3, and set properties
#add_ip_and_conf shifterComplex shifterComplex_3 {
#	DATA_IN_SIZE $DATA_OUT_FIR_SIZE \
#	DATA_OUT_SIZE $DATA_SIZE }

#connect_intf shifterComplex_3 data_out dupplComplex_3 data_in
#*******************************

# Create instance: dupplComplex_3, and set properties
add_ip_and_conf dupplComplex dupplComplex_3 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}
connect_intf dupplComplex_2 data2_out dupplComplex_3 data_in


# Create instance: dupplComplex_4, and set properties
add_ip_and_conf dupplComplex dupplComplex_4 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}
connect_intf dupplComplex_2 data1_out dupplComplex_4 data_in


# Create instance: dupplComplex_5, and set properties
add_ip_and_conf dupplComplex dupplComplex_5 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}

connect_intf dupplComplex_1 data1_out dupplComplex_5 data_in

# Create instance: dupplComplex_6, and set properties
add_ip_and_conf dupplComplex dupplComplex_6 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}

connect_intf shifterComplex_0 data_out dupplComplex_6 data_in

# Create instance: mux_filter, and set properties
add_ip_and_conf MUXcomplexNto1 mux_filter {
	DATA_SIZE $DATA_SIZE\
	INPUTS {4}}
connect_intf dupplComplex_3 data1_out mux_filter data_3
connect_intf DupplComplex_6 data1_out mux_filter data_0
connect_intf DupplComplex_5 data1_out mux_filter data_1
connect_intf dupplComplex_4 data1_out mux_filter data_2

connect_proc mux_filter s00_axi 0xE0000

# Create instance: mux_ram, and set properties
add_ip_and_conf MUXcomplexNto1 mux_ram {
	DATA_SIZE $DATA_SIZE\
	INPUTS {4}}
connect_intf DupplComplex_6 data2_out mux_ram data_0
connect_intf DupplComplex_5 data2_out mux_ram data_1
connect_intf dupplComplex_4 data2_out mux_ram data_2
connect_intf dupplComplex_3 data2_out mux_ram data_3

connect_proc mux_ram s00_axi 0xD0000

# Create instance: meanComplex_0, and set properties
add_ip_and_conf meanComplex meanComplex_0 {
	DATA_IN_SIZE $DATA_SIZE \
	DATA_OUT_SIZE $DATA_SIZE \
	NB_ACCUM {128} \
	SHIFT {7}}

connect_intf mux_ram data_out meanComplex_0 data_in

# Create instance: dataComplexFast, and set properties
add_ip_and_conf dataComplex_to_ram dataComplexFast {
	DATA_SIZE $DATA_SIZE \
	NB_INPUT {1} \
	NB_SAMPLE {1024} }

connect_intf meanComplex_0 data_out dataComplexFast data1_in

connect_proc dataComplexFast s00_axi 0x10000

# Create instance: dupplComplex_7, and set properties
add_ip_and_conf dupplComplex dupplComplex_7 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {3}}

connect_intf mux_filter data_out dupplComplex_7 data_in

# Create instance: convertComplexToReal_0, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_0 {
	DATA_SIZE $DATA_SIZE\
	}
connect_intf dupplComplex_7 data1_out convertComplexToReal_0 data_in

# Create instance: dupplReal_0, and set properties
add_ip_and_conf dupplReal dupplReal_0 {
	DATA_SIZE $DATA_SIZE\
	NB_OUTPUT {2}}

connect_intf convertComplexToReal_0 dataI_out dupplReal_0 data_in

# Create instance: magnitude_0, and set properties
add_ip_and_conf magnitude magnitude_0 {
	DATA_SIZE $DATA_SIZE\
	}

connect_intf dupplComplex_7 data2_out magnitude_0 data_in

# Create instance cordicAtan_0, and set properties
# DATA_OUT_SIZE = NB_ITER-1+4
# PI_VAL  = round(3.141592*2**(NB_ITER-1))
add_ip_and_conf cordicAtan cordicAtan_0 {
	DATA_IN_SIZE $DATA_SIZE\
	NB_ITER $NB_ITER\
	DATA_OUT_SIZE $DATA_SIZE\
	PI_VALUE $PI_VAL\
	}

connect_intf dupplComplex_7 data3_out cordicAtan_0 data_in

# Create instance: dupplReal_1, and set properties
add_ip_and_conf dupplReal dupplReal_1 {
	DATA_SIZE $DATA_SIZE\
	}

connect_intf cordicAtan_0 data_out dupplReal_1 data_in

# Create instance: mux_out_ch2, and set properties
add_ip_and_conf MUXrealNto1 mux_out_ch2 {
        DATA_SIZE $DATA_SIZE\
        INPUTS {4}}

connect_intf dupplReal_0 data1_out mux_out_ch2 data_in_0
connect_intf convertComplexToReal_0 dataQ_out mux_out_ch2 data_in_1
connect_intf magnitude_0 data_out mux_out_ch2 data_in_2
connect_intf dupplReal_1 data1_out mux_out_ch2 data_in_3

connect_proc mux_out_ch2 s00_axi 0x40000

# Create instance: shifterReal_0, and set properties
add_ip_and_conf shifterReal shifterReal_0 {
	DATA_IN_SIZE $DATA_SIZE \
	DATA_OUT_SIZE $DAC_SIZE }

connect_intf shifterReal_0 data_out redpitaya_converters_0 dataB_in
connect_intf mux_out_ch2 data_out shifterReal_0 data_in

# Create instance: mux_pid, and set properties
add_ip_and_conf MUXrealNto1 mux_pid {
	DATA_SIZE $DATA_SIZE\
	INPUTS {2}}

connect_intf dupplReal_0 data2_out mux_pid data_in_0
connect_intf dupplReal_1 data2_out mux_pid data_in_1

connect_proc mux_pid s00_axi 0x00000

# Create instance: pid1, and set properties
add_ip_and_conf pidv3_axi pid1 {
	DATA_IN_SIZE $DATA_SIZE\
	DATA_OUT_SIZE $PID_OUT_SIZE\
	PSR {0}\
	ISR {0} \
	DSR {0} \
	P_SIZE $PID_CONST_SIZE\
	I_SIZE $PID_CONST_SIZE \
	D_SIZE $PID_CONST_SIZE }

connect_proc pid1 s00_axi 0xC0000

connect_intf mux_pid data_out pid1 data_in
# Create instance: dds_range, and set properties
add_ip_and_conf axi_to_dac dds_range {
	DATA_SIZE {8} \
	SYNCHRONIZE_CHAN {false} }

connect_intf redpitaya_converters_0 clk_o dds_range ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_range ref_rst_i

connect_proc dds_range s00_axi 0x60000

# create instance: multiplierReal_0, and set properties
add_ip_and_conf multiplierReal multiplierReal_0 {
	DATA1_IN_SIZE {32}\
	DATA2_IN_SIZE {8}\
	DATA_OUT_SIZE {40}}

connect_intf pid1 data_out multiplierReal_0 data1_in
connect_intf dds_range dataA_out multiplierReal_0 data2_in

# Create instance: dds1_f0, and set properties
add_ip_and_conf add_constReal dds1_f0 {
	DATA_IN_SIZE {40}\
	DATA_OUT_SIZE {40}\
	format {unsigned} }

connect_proc dds1_f0 s00_axi 0x50000

connect_intf multiplierReal_0 data_out dds1_f0 data_in

# Create instance: dds1_nco, and set properties
add_ip_and_conf nco_counter dds1_nco {
	COUNTER_SIZE {40}\
	DATA_SIZE {16}\
	LUT_SIZE {12} }

connect_intf redpitaya_converters_0 clk_o dds1_nco ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds1_nco ref_rst_i

connect_proc dds1_nco s00_axi 0x30000

connect_intf dds1_f0 data_out dds1_nco pinc_in

# Create instance: convertComplexToReal_1, and set properties
add_ip_and_conf convertComplexToReal convertComplexToReal_1 {
	DATA_SIZE $DATA_SIZE\
	}

connect_intf dds1_nco sine_out convertComplexToReal_1 data_in

# Create instance: dds_ampl, and set properties
add_ip_and_conf axi_to_dac dds_ampl {
	DATA_SIZE {14} \
	SYNCHRONIZE_CHAN {false} }

connect_intf redpitaya_converters_0 clk_o dds_ampl ref_clk_i
connect_intf redpitaya_converters_0 rst_o dds_ampl ref_rst_i

connect_proc dds_ampl s00_axi 0x20000

# create instance: multiplierReal_1, and set properties
add_ip_and_conf multiplierReal multiplierReal_1 {
	DATA1_IN_SIZE {16}\
	DATA2_IN_SIZE {14}\
	DATA_OUT_SIZE {14}}

connect_intf dds_ampl dataA_out multiplierReal_1 data2_in
connect_intf multiplierReal_1 data_out redpitaya_converters_0 dataA_in
connect_intf convertComplexToReal_1 dataI_out multiplierReal_1 data1_in
