# 4.1s @ 128kHz
#set NB_SAMPLE 525804
# 3s @ 128kHz
set NB_SAMPLE 384000

for {set i 0} {$i < 2} {incr i} {
	## better => xlconcat
	ad_ip_instance util_cpack2 ggm_util_pack_$i
	ad_ip_parameter ggm_util_pack_$i CONFIG.NUM_OF_CHANNELS 2
	ad_connect axi_ad9361/rst ggm_util_pack_$i/reset
	ad_connect axi_ad9361/l_clk ggm_util_pack_$i/clk

	ad_connect axi_ad9361/adc_valid_i0 ggm_util_pack_$i/fifo_wr_en
	ad_connect axi_ad9361/adc_data_i$i ggm_util_pack_$i/fifo_wr_data_0
	ad_connect axi_ad9361/adc_data_q$i ggm_util_pack_$i/fifo_wr_data_1
	ad_connect axi_ad9361/adc_enable_i$i ggm_util_pack_$i/enable_0
	ad_connect axi_ad9361/adc_enable_q$i ggm_util_pack_$i/enable_1

	# axiStreamToComplex
	ad_ip_instance axiStreamToComplex axis2Complex_$i
	ad_ip_parameter axis2Complex_$i CONFIG.DATA_SIZE 16
	
	ad_connect axi_ad9361/rst axis2Complex_$i/s00_axis_reset
	ad_connect axi_ad9361/l_clk axis2Complex_$i/s00_axis_aclk
	
	ad_connect ggm_util_pack_$i/packed_fifo_wr_data axis2Complex_$i/s00_axis_tdata
	ad_connect ggm_util_pack_$i/packed_fifo_wr_en axis2Complex_$i/s00_axis_tvalid

	# complex to axis
	ad_ip_instance complexToAxiStream cplx_to_axis_$i
	ad_ip_parameter cplx_to_axis_$i CONFIG.DATA_SIZE 16
	
	ad_connect axis2Complex_$i/data_out cplx_to_axis_$i/data_in
	
	ad_connect axi_ad9361/l_clk cplx_to_axis_$i/m00_axis_aclk
	
	# fifo
	ad_ip_instance fifo_generator fifo_clk_$i
	ad_ip_parameter fifo_clk_$i CONFIG.INTERFACE_TYPE {AXI_STREAM}
	ad_ip_parameter fifo_clk_$i CONFIG.Clock_Type_AXI {Independent_Clock}
	ad_ip_parameter fifo_clk_$i CONFIG.Empty_Threshold_Assert_Value_axis 13
	ad_ip_parameter fifo_clk_$i CONFIG.Empty_Threshold_Assert_Value_rach 13
	ad_ip_parameter fifo_clk_$i CONFIG.Empty_Threshold_Assert_Value_rdch 1021
	ad_ip_parameter fifo_clk_$i CONFIG.Empty_Threshold_Assert_Value_wach 13
	ad_ip_parameter fifo_clk_$i CONFIG.Empty_Threshold_Assert_Value_wdch 1021
	ad_ip_parameter fifo_clk_$i CONFIG.Empty_Threshold_Assert_Value_wrch 13
	ad_ip_parameter fifo_clk_$i CONFIG.FIFO_Implementation_axis {Independent_Clocks_Block_RAM}
	ad_ip_parameter fifo_clk_$i CONFIG.FIFO_Implementation_rach {Independent_Clocks_Distributed_RAM}
	ad_ip_parameter fifo_clk_$i CONFIG.FIFO_Implementation_rdch {Independent_Clocks_Block_RAM}
	ad_ip_parameter fifo_clk_$i CONFIG.FIFO_Implementation_wach {Independent_Clocks_Distributed_RAM}
	ad_ip_parameter fifo_clk_$i CONFIG.FIFO_Implementation_wdch {Independent_Clocks_Block_RAM}
	ad_ip_parameter fifo_clk_$i CONFIG.FIFO_Implementation_wrch {Independent_Clocks_Distributed_RAM}
	ad_ip_parameter fifo_clk_$i CONFIG.Full_Flags_Reset_Value 1
	ad_ip_parameter fifo_clk_$i CONFIG.Full_Threshold_Assert_Value_axis 15
	ad_ip_parameter fifo_clk_$i CONFIG.Full_Threshold_Assert_Value_rach 15
	ad_ip_parameter fifo_clk_$i CONFIG.Full_Threshold_Assert_Value_wach 15
	ad_ip_parameter fifo_clk_$i CONFIG.Full_Threshold_Assert_Value_wrch 15
	ad_ip_parameter fifo_clk_$i CONFIG.HAS_ACLKEN {false}
	ad_ip_parameter fifo_clk_$i CONFIG.Input_Depth_axis 16
	ad_ip_parameter fifo_clk_$i CONFIG.Reset_Type {Asynchronous_Reset}
	ad_ip_parameter fifo_clk_$i CONFIG.TDATA_NUM_BYTES 4
	ad_ip_parameter fifo_clk_$i CONFIG.TKEEP_WIDTH 4
	ad_ip_parameter fifo_clk_$i CONFIG.TSTRB_WIDTH 4
	ad_ip_parameter fifo_clk_$i CONFIG.TUSER_WIDTH 0
	
	ad_connect cplx_to_axis_$i/m00_axis fifo_clk_$i/S_AXIS
	
	ad_connect axi_ad9361/l_clk fifo_clk_$i/s_aclk
	ad_connect sys_ps7/FCLK_CLK0 fifo_clk_$i/m_aclk
	ad_connect sys_rstgen/peripheral_aresetn fifo_clk_$i/s_aresetn
	
	#fifo axis to complex
	ad_ip_instance axiStreamToComplex fifo2Cplx_$i
	ad_ip_parameter fifo2Cplx_$i CONFIG.DATA_SIZE 16
	
	ad_connect fifo_clk_$i/M_AXIS fifo2Cplx_$i/s00_axis
	ad_connect sys_rstgen/peripheral_reset fifo2Cplx_$i/s00_axis_reset
	ad_connect sys_ps7/FCLK_CLK0 fifo2Cplx_$i/s00_axis_aclk
	
	ad_ip_instance meanComplex mean_$i
	ad_ip_parameter mean_$i CONFIG.SIGNED_FORMAT true
	ad_ip_parameter mean_$i CONFIG.NB_ACCUM 8
	ad_ip_parameter mean_$i CONFIG.SHIFT 3
	ad_ip_parameter mean_$i CONFIG.DATA_IN_SIZE 16
	ad_ip_parameter mean_$i CONFIG.DATA_OUT_SIZE 16

	ad_connect fifo2Cplx_$i/data_out mean_$i/data_in
	
}

create_bd_port -dir I trig_in
# pulse gen
ad_ip_instance syncTrigStream syncStream

ad_ip_parameter syncStream CONFIG.USE_EXT_TRIG true
ad_ip_parameter syncStream CONFIG.DFLT_PERIOD 500000000
ad_ip_parameter syncStream CONFIG.DFLT_DUTY 100
ad_ip_parameter syncStream CONFIG.GEN_SIZE 32
ad_ip_parameter syncStream CONFIG.DATA_SIZE 16
ad_ip_parameter syncStream CONFIG.NB_SAMPLE $NB_SAMPLE

ad_connect trig_in syncStream/ext_trig_i

ad_connect sys_cpu_reset syncStream/s00_axi_reset
ad_cpu_interconnect 0x43C10000 syncStream

ad_connect mean_0/data_out syncStream/data1_in
ad_connect mean_1/data_out syncStream/data2_in

#dataComplex dma
ad_ip_instance dataComplex_dma_direct data_to_ram
ad_ip_parameter data_to_ram CONFIG.SIGNED_FORMAT true
ad_ip_parameter data_to_ram CONFIG.USE_SOF true
ad_ip_parameter data_to_ram CONFIG.STOP_ON_EOF true
ad_ip_parameter data_to_ram CONFIG.DATA_SIZE 16
ad_ip_parameter data_to_ram CONFIG.NB_SAMPLE $NB_SAMPLE

ad_connect syncStream/data1_out data_to_ram/data1_in
ad_connect syncStream/data2_out data_to_ram/data2_in
ad_connect sys_rstgen/peripheral_reset data_to_ram/s00_axi_reset

ad_connect sys_cpu_reset  data_to_ram/m00_axis_reset
ad_connect sys_cpu_clk  data_to_ram/m00_axis_aclk

ad_cpu_interconnect 0x43C20000 data_to_ram

ad_ip_instance axi_dma axi_dma_x
ad_ip_parameter axi_dma_x CONFIG.c_include_sg false
ad_ip_parameter axi_dma_x CONFIG.c_sg_length_width 23
ad_ip_parameter axi_dma_x CONFIG.c_include_mm2s false
ad_ip_parameter axi_dma_x CONFIG.c_s2mm_burst_size 32

ad_connect data_to_ram/m00_axis axi_dma_x/s_axis_s2mm


ad_cpu_interconnect 0x43C30000 axi_dma_x
ad_connect sys_concat_intc/In14 axi_dma_x/s2mm_introut
ad_mem_hp3_interconnect sys_cpu_clk sys_ps7/S_AXI_HP3
ad_mem_hp3_interconnect sys_cpu_clk axi_dma_x/m_axi_s2mm
ad_connect sys_cpu_clk axi_dma_x/m_axi_s2mm_aclk
save_bd_design
