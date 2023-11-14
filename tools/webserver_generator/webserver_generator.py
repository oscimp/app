#!/usr/bin/env python3

from xml.dom import minidom
import sys
import os, stat

board_driver_array = []
xmldoc = minidom.parse(sys.argv[1])
name = sys.argv[1].split('/')[-1].split('.')[0]

driver_list = xmldoc.getElementsByTagName('ip')

for driver in driver_list:
	board_driver_list = driver.getElementsByTagName('instance')
	for board_driver in board_driver_list:
		board_driver_array.append([str(driver.attributes['name'].value), str(board_driver.attributes['name'].value)])

board_driver_array = sorted(board_driver_array, key=lambda x:x[-1])

try:
	os.chdir('app')
except:
	os.mkdir('app')
	os.chdir('app')

try:
	os.remove(f'{name}_webserver.py')
except:
	pass

with open(f'{name}_webserver.py', 'a') as f:
	f.write('#!/usr/bin/env python\n\n')

	f.write('import liboscimp_fpga\n')
	f.write('import ctypes\n')
	f.write('import os\n')
	f.write('import time\n')
	f.write('from lxml import objectify\n')
	f.write('import lxml.etree\n')
	f.write('import remi.gui as gui\n')
	f.write('from remi import start, App\n\n')

	for elem in board_driver_array:
		if elem[0] == 'redpitaya_converters_12':
			f.write('#Packages for the redpitaya12 board\n')
			f.write('from threading import Timer\n\n')

			f.write('# Initiate the controller input and output switches\n')
			f.write('liboscimp_fpga.RP_12_initController()\n\n')

			f.write('# Power on ADC and DAC\n')
			f.write('os.system("echo 908 > /sys/class/gpio/export")\n')
			f.write('os.system("echo out > /sys/class/gpio/gpio908/direction")\n')
			f.write('os.system("echo 1 > /sys/class/gpio/gpio908/value")\n')
			f.write('os.system("echo 908 > /sys/class/gpio/unexport")\n')
			f.write('os.system("echo 909 > /sys/class/gpio/export")\n')
			f.write('os.system("echo out > /sys/class/gpio/gpio909/direction")\n')
			f.write('os.system("echo 1 > /sys/class/gpio/gpio909/value")\n')
			f.write('os.system("echo 909 > /sys/class/gpio/unexport")\n\n')

			f.write('# Configure the ADCs \n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0xff,0x00,1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0xff,0x00,0)\n')
			f.write('time.sleep(0.1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0x14,0x01,1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0x14,0x01,0)\n')
			f.write('time.sleep(0.1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0x16,0xa0,1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0x16,0xa0,0)\n')
			f.write('time.sleep(0.1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0x18,0x1b,1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0x18,0x1b,0)\n')
			f.write('time.sleep(0.1)\n')
			f.write(f'liboscimp_fpga.redpitaya_converters_12_spi_conf("/dev/{elem[1]}",1,0xff,0x01,1)\n\n')

	try:
		board_name = os.environ["BOARD_NAME"].lower()
	except KeyError:
		print("Error: missing BOARD_NAME")
		os.sys.exit()

	nco_accum_size = 40
	const_size = 32
	pid_coeff_size = 14
	lut_size = 12

	if board_name == "redpitaya":
		samp_freq = 125000000
	elif board_name == "redpitaya16":
		samp_freq = 122880000
	elif board_name == "plutosdr":
		samp_freq = 50000000
		rx_lo = 1000000000
		tx_lo = 1000000000
	elif board_name == "redpitaya12":
		samp_freq = 250000000
	elif board_name == "zedboard":
		samp_freq = 100000000

	if board_name == "plutosdr":

		f.write('import iio\n\n')

		f.write('ctx = iio.Context()\n')
		f.write('dev_rx = ctx.find_device("cf-ad9361-lpc")\n')
		f.write('dev_tx = ctx.find_device("cf-ad9361-dds-core-lpc")\n')
		f.write('phy = ctx.find_device("ad9361-phy")\n\n')

		f.write(f'[i for i in phy.channels if i.id == "altvoltage0"][0].attrs["frequency"].value = "{rx_lo}"\n')
		f.write(f'[i for i in phy.channels if i.id == "altvoltage1"][0].attrs["frequency"].value = "{tx_lo}"\n\n')

		#f.write(f'[i for i in phy.channels if i.id == "out"][0].attrs["voltage_filter_fir_en"].value = "1"\n\n')

		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["sampling_frequency"].value = "{samp_freq}"\n')
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["rf_bandwidth"].value = "{samp_freq}"\n')
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["quadrature_tracking_en"].value = "1"\n')
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["rf_dc_offset_tracking_en"].value = "1"\n')
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["bb_dc_offset_tracking_en"].value = "1"\n')
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["gain_control_mode"].value = "manual"\n') #put a control
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["hardwaregain"].value = "30"\n') #put a control
		f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["rf_port_select"].value = "A_BALANCED"\n\n')
		#f.write(f'[i for i in phy.channels if i.id == "voltage0"][0].attrs["filter_fir_en"].value = "1"\n\n')

	f.write('#Sampling frequency\n')
	f.write(f"samp_freq = {samp_freq}\n\n")

	f.write('#NCO accumulator size\n')
	f.write(f"nco_accum_size = {nco_accum_size}\n\n")

	f.write('#const size\n')
	f.write(f"const_size = {const_size}\n\n")

	f.write('#pid size\n')
	f.write(f"pid_coeff_size = {pid_coeff_size}\n\n")

	f.write('#lut size\n')
	f.write(f"lut_size = {lut_size}\n\n")

	f.write('vals = objectify.Element("item")\n')
	f.write(f'vals.config = "{name}_defconf.xml"\n')

	if board_name == "plutosdr":
		f.write('vals.tx_lo = 1000000000\n')
		f.write('vals.rx_lo = 1000000000\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write(f'vals.{elem[1]} = 0\n')

		if elem[0] == 'axi_to_dac':
			f.write(f'vals.ch1_{elem[1]} = 0\n')
			f.write(f'vals.ch2_{elem[1]} = 0\n')

		if elem[0] == 'pidv3_axi':
			f.write(f'vals.kp_{elem[1]} = 0\n')
			f.write(f'vals.ki_{elem[1]} = 0\n')
			f.write(f'vals.rst_int_{elem[1]} = True\n')
			f.write(f'vals.sp_{elem[1]} = 0\n')
			f.write(f'vals.sign_{elem[1]} = 0\n')

		if elem[0] == 'redpitaya_converters_12':
			f.write('vals.listView_acdc1 = "ADC1 DC"\n')
			f.write('vals.listView_acdc2 = "ADC2 DC"\n')
			f.write('vals.listView_range1 = "ADC1\\xa01/20"\n')
			f.write('vals.listView_range2 = "ADC2\\xa01/20"\n')
			f.write('vals.listView_ampl1 = "DAC1\\xa02V"\n')
			f.write('vals.listView_ampl2 = "DAC2\\xa02V"\n')
			f.write('vals.listView_extref = "Int\\xa0Clock"\n')

		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn']:
			f.write(f'vals.{elem[1]} = 9\n')

		if elem[0] == 'delayTempoReal_axi':
			f.write(f'vals.{elem[1]} = 0\n')

		if elem[0] == 'nco_counter':
			f.write(f'vals.pinc_{elem[1]} = 0\n')
			f.write(f'vals.poff_{elem[1]} = 0\n')
			f.write(f'vals.cb_pinc_{elem[1]} = True\n')
			f.write(f'vals.cb_poff_{elem[1]} = True\n')

		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write(f'vals.{elem[1]} = False\n')

	f.write('\nclass MyApp(App):\n')
	f.write('\tdef __init__(self, *args):\n')
	f.write('\t\tsuper(MyApp, self).__init__(*args)\n\n')
	f.write('\tdef main(self):\n')
	f.write('\t\tself.w = gui.VBox()\n\n')

	print('\n')

	f.write('\t\tself.hbox_save_load = gui.HBox(margin="10px")\n')
	f.write('\t\tself.dtext_conf_file = gui.TextInput(width=200, height=30)\n')
	f.write('\t\tself.dtext_conf_file.set_value(str(vals.config))\n')
	f.write('\t\tself.dtext_conf_file.set_on_change_listener(self.dtext_conf_file_changed)\n')
	f.write('\t\tself.bt_load = gui.Button("Load", width=200, height=30, margin="10px")\n')
	f.write('\t\tself.bt_load.set_on_click_listener(self.bt_load_changed)\n')
	f.write('\t\tself.bt_save = gui.Button("Save", width=200, height=30, margin="10px")\n')
	f.write('\t\tself.bt_save.set_on_click_listener(self.bt_save_changed)\n')
	f.write('\t\tself.hbox_save_load.append(self.dtext_conf_file)\n')
	f.write('\t\tself.hbox_save_load.append(self.bt_load)\n')
	f.write('\t\tself.hbox_save_load.append(self.bt_save)\n')
	f.write('\t\tself.w.append(self.hbox_save_load)\n\n')

	if board_name == "plutosdr":
		f.write('\t\tself.hbox_tx_lo = gui.HBox(margin="10px")\n')
		f.write('\t\tself.lb_tx_lo = gui.Label("iio:tx_lo", width="20%%", margin="10px")\n')
		f.write('\t\tself.sd_tx_lo = gui.Slider(vals.tx_lo, 0, 7000000000, 1000000, width="60%%", margin="10px")\n')
		f.write('\t\tself.sd_tx_lo.set_on_change_listener(self.sd_tx_lo_changed)\n')
		f.write('\t\tself.sb_tx_lo = gui.SpinBox(vals.tx_lo, 0, 7000000000, 1000000, width="20%%", margin="10px")\n')
		f.write('\t\tself.sb_tx_lo.set_on_change_listener(self.sb_tx_lo_changed)\n')
		f.write('\t\tself.sd_tx_lo_changed(self.sd_tx_lo, self.sd_tx_lo.get_value())\n')
		f.write('\t\tself.hbox_tx_lo.append(self.lb_tx_lo)\n')
		f.write('\t\tself.hbox_tx_lo.append(self.sd_tx_lo)\n')
		f.write('\t\tself.hbox_tx_lo.append(self.sb_tx_lo)\n')
		f.write('\t\tself.w.append(self.hbox_tx_lo)\n\n')

		f.write('\t\tself.hbox_rx_lo = gui.HBox(margin="10px")\n')
		f.write('\t\tself.lb_rx_lo = gui.Label("iio:rx_lo", width="20%%", margin="10px")\n')
		f.write('\t\tself.sd_rx_lo = gui.Slider(vals.rx_lo, 0, 7000000000, 1000000, width="60%%", margin="10px")\n')
		f.write('\t\tself.sd_rx_lo.set_on_change_listener(self.sd_rx_lo_changed)\n')
		f.write('\t\tself.sb_rx_lo = gui.SpinBox(vals.rx_lo, 0, 7000000000, 1000000, width="20%%", margin="10px")\n')
		f.write('\t\tself.sb_rx_lo.set_on_change_listener(self.sb_rx_lo_changed)\n')
		f.write('\t\tself.sd_rx_lo_changed(self.sd_rx_lo, self.sd_rx_lo.get_value())\n')
		f.write('\t\tself.hbox_rx_lo.append(self.lb_rx_lo)\n')
		f.write('\t\tself.hbox_rx_lo.append(self.sd_rx_lo)\n')
		f.write('\t\tself.hbox_rx_lo.append(self.sb_rx_lo)\n')
		f.write('\t\tself.w.append(self.hbox_rx_lo)\n\n')

	for elem in board_driver_array:
		print(f'{elem[1]}\t{elem[0]}')

		if elem[0] == 'add_constReal':
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_{elem[1]} = gui.Label("/dev/{elem[1]}", width="20%%", margin="10px")\n')
			if 'f0' not in elem[1]:
				f.write(f'\t\tself.sd_{elem[1]} = gui.Slider(vals.{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="60%%", margin="10px")\n')
			else:
				f.write(f'\t\tself.sd_{elem[1]} = gui.Slider(vals.{elem[1]}, 0, samp_freq/2, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_{elem[1]}.set_on_change_listener(self.sd_{elem[1]}_changed)\n')
			if 'f0' not in elem[1]:
				f.write(f'\t\tself.sb_{elem[1]} = gui.SpinBox(vals.{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="20%%", margin="10px")\n')
			else:
				f.write(f'\t\tself.sb_{elem[1]} = gui.SpinBox(vals.{elem[1]}, 0, samp_freq/2, samp_freq/2**nco_accum_size, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_{elem[1]}.set_on_change_listener(self.sb_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_{elem[1]}_changed(self.sd_{elem[1]}, self.sd_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.lb_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sd_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sb_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_{elem[1]})\n\n')

		if elem[0] == 'axi_to_dac':
			f.write(f'\t\tself.hbox_ch1_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_ch1_{elem[1]} = gui.Label("/dev/{elem[1]}/1", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_ch1_{elem[1]} = gui.Slider(vals.ch1_{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_ch1_{elem[1]}.set_on_change_listener(self.sd_ch1_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_ch1_{elem[1]} = gui.SpinBox(vals.ch1_{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_ch1_{elem[1]}.set_on_change_listener(self.sb_ch1_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_ch1_{elem[1]}_changed(self.sd_ch1_{elem[1]}, self.sd_ch1_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_ch1_{elem[1]}.append(self.lb_ch1_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ch1_{elem[1]}.append(self.sd_ch1_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ch1_{elem[1]}.append(self.sb_ch1_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_ch1_{elem[1]})\n\n')

			f.write(f'\t\tself.hbox_ch2_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_ch2_{elem[1]} = gui.Label("/dev/{elem[1]}/2", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_ch2_{elem[1]} = gui.Slider(vals.ch2_{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_ch2_{elem[1]}.set_on_change_listener(self.sd_ch2_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_ch2_{elem[1]} = gui.SpinBox(vals.ch2_{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_ch2_{elem[1]}.set_on_change_listener(self.sb_ch2_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_ch2_{elem[1]}_changed(self.sd_ch2_{elem[1]}, self.sd_ch2_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_ch2_{elem[1]}.append(self.lb_ch2_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ch2_{elem[1]}.append(self.sd_ch2_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ch2_{elem[1]}.append(self.sb_ch2_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_ch2_{elem[1]})\n\n')

		if elem[0] == 'pidv3_axi':
			f.write(f'\t\tself.hbox_kp_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_kp_{elem[1]} = gui.Label("/dev/{elem[1]}/kp", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_kp_{elem[1]} = gui.Slider(vals.kp_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_kp_{elem[1]}.set_on_change_listener(self.sd_kp_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_kp_{elem[1]} = gui.SpinBox(vals.kp_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_kp_{elem[1]}.set_on_change_listener(self.sb_kp_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_kp_{elem[1]}_changed(self.sd_kp_{elem[1]}, self.sd_kp_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_kp_{elem[1]}.append(self.lb_kp_{elem[1]})\n')
			f.write(f'\t\tself.hbox_kp_{elem[1]}.append(self.sd_kp_{elem[1]})\n')
			f.write(f'\t\tself.hbox_kp_{elem[1]}.append(self.sb_kp_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_kp_{elem[1]})\n\n')

			f.write(f'\t\tself.hbox_ki_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_ki_{elem[1]} = gui.Label("/dev/{elem[1]}/ki", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_ki_{elem[1]} = gui.Slider(vals.ki_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_ki_{elem[1]}.set_on_change_listener(self.sd_ki_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_ki_{elem[1]} = gui.SpinBox(vals.ki_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_ki_{elem[1]}.set_on_change_listener(self.sb_ki_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_ki_{elem[1]}_changed(self.sd_ki_{elem[1]}, self.sd_ki_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.cb_rst_int_{elem[1]} = gui.CheckBoxLabel("rst_int", vals.rst_int_{elem[1]}, width="5%%", margin="10px")\n')
			f.write(f'\t\tself.cb_rst_int_{elem[1]}.set_on_change_listener(self.cb_rst_int_{elem[1]}_changed)\n')
			f.write(f'\t\tself.hbox_ki_{elem[1]}.append(self.lb_ki_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ki_{elem[1]}.append(self.sd_ki_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ki_{elem[1]}.append(self.sb_ki_{elem[1]})\n')
			f.write(f'\t\tself.hbox_ki_{elem[1]}.append(self.cb_rst_int_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_ki_{elem[1]})\n\n')

			f.write(f'\t\tself.hbox_sp_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_sp_{elem[1]} = gui.Label("/dev/{elem[1]}/setpoint", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_sp_{elem[1]} = gui.Slider(vals.sp_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_sp_{elem[1]}.set_on_change_listener(self.sd_sp_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_sp_{elem[1]} = gui.SpinBox(vals.sp_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_sp_{elem[1]}.set_on_change_listener(self.sb_sp_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_sp_{elem[1]}_changed(self.sd_sp_{elem[1]}, self.sd_sp_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_sp_{elem[1]}.append(self.lb_sp_{elem[1]})\n')
			f.write(f'\t\tself.hbox_sp_{elem[1]}.append(self.sd_sp_{elem[1]})\n')
			f.write(f'\t\tself.hbox_sp_{elem[1]}.append(self.sb_sp_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_sp_{elem[1]})\n\n')

			f.write(f'\t\tself.hbox_sign_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_sign_{elem[1]} = gui.Label("/dev/{elem[1]}/sign", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_sign_{elem[1]} = gui.Slider(vals.sign_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_sign_{elem[1]}.set_on_change_listener(self.sd_sign_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_sign_{elem[1]} = gui.SpinBox(vals.sign_{elem[1]}, -2**(pid_coeff_size-1), 2**(pid_coeff_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_sign_{elem[1]}.set_on_change_listener(self.sb_sign_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_sign_{elem[1]}_changed(self.sd_sign_{elem[1]}, self.sd_sign_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.hbox_sign_{elem[1]}.append(self.lb_sign_{elem[1]})\n')
			f.write(f'\t\tself.hbox_sign_{elem[1]}.append(self.sd_sign_{elem[1]})\n')
			f.write(f'\t\tself.hbox_sign_{elem[1]}.append(self.sb_sign_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_sign_{elem[1]})\n\n')

		if elem[0] == 'redpitaya_converters_12':
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="2px")\n')
			f.write(f'\t\tself.lb_{elem[1]} = gui.Label("RP12", width="20%%",height=0, margin="10px")\n')
			f.write('\t\tself.listView_acdc1 = gui.ListView.new_from_list(("ADC1 AC","ADC1 DC"), width=70, height=50, margin="10px")\n')
			f.write('\t\tself.listView_range1 = gui.ListView.new_from_list(("ADC1\\xa01/1","ADC1\\xa01/20"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_ampl1 = gui.ListView.new_from_list(("DAC1\\xa02V","DAC1\\xa010V"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_acdc2 = gui.ListView.new_from_list(("ADC2 AC","ADC2 DC"), width=70, height=50, margin="10px")\n')
			f.write('\t\tself.listView_range2 = gui.ListView.new_from_list(("ADC2\\xa01/1","ADC2\\xa01/20"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_ampl2 = gui.ListView.new_from_list(("DAC2\\xa02V","DAC2\\xa010V"), width=80, height=50, margin="10px")\n')
			f.write('\t\tself.listView_extref = gui.ListView.new_from_list(("Int\\xa0Clock","Ext\\xa0Ref"), width=70, height=50, margin="10px", style={"background-color": "#FE96A0"})\n')
			f.write('\t\tself.listView_acdc1.onselection(self.listView_acdc1_changed)\n')
			f.write('\t\tself.listView_range1.onselection(self.listView_range1_changed)\n')
			f.write('\t\tself.listView_ampl1.onselection(self.listView_ampl1_changed)\n')
			f.write('\t\tself.listView_acdc2.onselection(self.listView_acdc2_changed)\n')
			f.write('\t\tself.listView_range2.onselection(self.listView_range2_changed)\n')
			f.write('\t\tself.listView_ampl2.onselection(self.listView_ampl2_changed)\n')
			f.write('\t\tself.listView_extref.onselection(self.listView_extref_changed)\n')
			f.write('\t\tself.listView_acdc1.select_by_value("ADC1 DC")\n')
			f.write('\t\tself.listView_acdc2.select_by_value("ADC2 DC")\n')
			f.write('\t\tself.listView_range1.select_by_value("ADC1\\xa01/20")\n')
			f.write('\t\tself.listView_range2.select_by_value("ADC2\\xa01/20")\n')
			f.write('\t\tself.listView_ampl1.select_by_value("DAC1\\xa02V")\n')
			f.write('\t\tself.listView_ampl2.select_by_value("DAC2\\xa02V")\n')
			f.write('\t\tself.listView_extref.select_by_value("Int\\xa0Clock")\n')
			f.write('\t\tself.dcolor_extref_state = gui.ColorPicker(width=40, height=40)\n')
			f.write('\t\tself.dcolor_extref_state.set_value("#ff0000")\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.lb_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_acdc1)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_acdc2)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_range1)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_range2)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_ampl1)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_ampl2)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.listView_extref)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.dcolor_extref_state)\n')
			f.write(f'\t\tself.w.append(self.hbox_{elem[1]})\n\n')
			f.write('\t\tself.stop_flag = False\n')
			f.write('\t\tself.display_extref_state()\n\n')

		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn'] :
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_{elem[1]} = gui.Label("/dev/{elem[1]}", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_{elem[1]} = gui.Slider(vals.{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_{elem[1]}.set_on_change_listener(self.sd_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_{elem[1]} = gui.SpinBox(vals.{elem[1]}, -2**(const_size-1), 2**(const_size-1)-1, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_{elem[1]}.set_on_change_listener(self.sb_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_{elem[1]}_changed(self.sd_{elem[1]}, self.sd_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.lb_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sd_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sb_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_{elem[1]})\n\n')

		if elem[0] == 'delayTempoReal_axi':
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_{elem[1]} = gui.Label("/dev/{elem[1]}", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_{elem[1]} = gui.Slider(vals.{elem[1]}, 0, 10000, 1, width="60%%", margin="10px")\n')
			f.write(f'\t\tself.sd_{elem[1]}.set_oninput_listener(self.sd_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_{elem[1]} = gui.SpinBox(vals.{elem[1]}, 0, 10000, 1, width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sb_{elem[1]}.set_on_change_listener(self.sb_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_{elem[1]}_changed(self.sd_{elem[1]}, self.sd_{elem[1]}.get_value())\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.lb_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sd_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sb_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_{elem[1]})\n\n')

		if elem[0] == 'nco_counter':
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.lb_{elem[1]} = gui.Label("/dev/{elem[1]}", width="20%%", margin="10px")\n')
			f.write(f'\t\tself.sd_pinc_{elem[1]} = gui.Slider(vals.pinc_{elem[1]}, 0, samp_freq/2, samp_freq/2**nco_accum_size, width="25%%", margin="10px")\n')
			f.write(f'\t\tself.sd_pinc_{elem[1]}.set_on_change_listener(self.sd_pinc_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_pinc_{elem[1]} = gui.SpinBox(vals.pinc_{elem[1]}, 0, samp_freq/2, samp_freq/2**nco_accum_size, width="10%%", margin="10px")\n')
			f.write(f'\t\tself.sb_pinc_{elem[1]}.set_on_change_listener(self.sb_pinc_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sd_poff_{elem[1]} = gui.Slider(vals.poff_{elem[1]}, -2**(lut_size-1), 2**(lut_size-1)-1, 1, width="25%%", margin="10px")\n')
			f.write(f'\t\tself.sd_poff_{elem[1]}.set_on_change_listener(self.sd_poff_{elem[1]}_changed)\n')
			f.write(f'\t\tself.sb_poff_{elem[1]} = gui.SpinBox(vals.poff_{elem[1]}, -2**(lut_size-1), 2**(lut_size-1)-1, 1, width="10%%", margin="10px")\n')
			f.write(f'\t\tself.sb_poff_{elem[1]}.set_on_change_listener(self.sb_poff_{elem[1]}_changed)\n')
			f.write(f'\t\tself.cb_pinc_{elem[1]} = gui.CheckBoxLabel("pinc", vals.cb_pinc_{elem[1]}, width="5%%", margin="10px")\n')
			f.write(f'\t\tself.cb_pinc_{elem[1]}.set_on_change_listener(self.cb_pinc_{elem[1]}_changed)\n')
			f.write(f'\t\tself.cb_poff_{elem[1]} = gui.CheckBoxLabel("poff", vals.cb_poff_{elem[1]}, width="5%%", margin="10px")\n')
			f.write(f'\t\tself.cb_poff_{elem[1]}.set_on_change_listener(self.cb_poff_{elem[1]}_changed)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.lb_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sd_pinc_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sb_pinc_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sd_poff_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.sb_poff_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.cb_pinc_{elem[1]})\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.cb_poff_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_{elem[1]})\n\n')

		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write(f'\t\tself.hbox_{elem[1]} = gui.HBox(margin="10px")\n')
			f.write(f'\t\tself.cb_{elem[1]} = gui.CheckBoxLabel("{elem[1]}", vals.{elem[1]}, width="5%%", margin="10px")\n')
			f.write(f'\t\tself.cb_{elem[1]}.set_on_change_listener(self.cb_{elem[1]}_changed)\n')
			f.write(f'\t\tself.hbox_{elem[1]}.append(self.cb_{elem[1]})\n')
			f.write(f'\t\tself.w.append(self.hbox_{elem[1]})\n\n')

	f.write('\t\treturn self.w\n\n')

	f.write('\tdef dtext_conf_file_changed(self, widget, value):\n')
	f.write('\t\tprint(value)\n')
	f.write('\t\tvals.config=value\n\n')

	f.write('\tdef bt_load_changed(self, widget):\n')
	f.write('\t\twith open(str(vals.config), "r") as f:\n')
	f.write('\t\t\t lf = objectify.fromstring(f.read())\n\n')

	if board_name == "plutosdr":
		f.write('\t\tself.sd_tx_lo_changed(self.sd_tx_lo, lf.tx_lo)\n')
		f.write('\t\tself.sb_tx_lo_changed(self.sb_tx_lo, lf.tx_lo)\n')

		f.write('\t\tself.sd_rx_lo_changed(self.sd_rx_lo, lf.rx_lo)\n')
		f.write('\t\tself.sb_rx_lo_changed(self.sb_rx_lo, lf.rx_lo)\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write(f'\t\tself.sd_{elem[1]}_changed(self.sd_{elem[1]}, lf.{elem[1]})\n')
			f.write(f'\t\tself.sb_{elem[1]}_changed(self.sb_{elem[1]}, lf.{elem[1]})\n')
		if elem[0] == 'axi_to_dac':
			f.write(f'\t\tself.sd_ch1_{elem[1]}_changed(self.sd_ch1_{elem[1]}, lf.ch1_{elem[1]})\n')
			f.write(f'\t\tself.sb_ch1_{elem[1]}_changed(self.sd_ch1_{elem[1]}, lf.ch1_{elem[1]})\n')
			f.write(f'\t\tself.sd_ch2_{elem[1]}_changed(self.sb_ch2_{elem[1]}, lf.ch2_{elem[1]})\n')
			f.write(f'\t\tself.sb_ch2_{elem[1]}_changed(self.sb_ch2_{elem[1]}, lf.ch2_{elem[1]})\n')
		if elem[0] == 'pidv3_axi':
			f.write(f'\t\tself.sd_kp_{elem[1]}_changed(self.sd_kp_{elem[1]}, lf.kp_{elem[1]})\n')
			f.write(f'\t\tself.sb_kp_{elem[1]}_changed(self.sb_kp_{elem[1]}, lf.kp_{elem[1]})\n')
			f.write(f'\t\tself.sd_ki_{elem[1]}_changed(self.sd_ki_{elem[1]}, lf.ki_{elem[1]})\n')
			f.write(f'\t\tself.sb_ki_{elem[1]}_changed(self.sb_ki_{elem[1]}, lf.ki_{elem[1]})\n')
			f.write(f'\t\tself.cb_rst_int_{elem[1]}_changed(self.cb_rst_int_{elem[1]}, lf.rst_int_{elem[1]})\n')
			f.write(f'\t\tself.sd_sp_{elem[1]}_changed(self.sd_sp_{elem[1]}, lf.sp_{elem[1]})\n')
			f.write(f'\t\tself.sb_sp_{elem[1]}_changed(self.sb_sp_{elem[1]}, lf.sp_{elem[1]})\n')
			f.write(f'\t\tself.sd_sign_{elem[1]}_changed(self.sd_sign_{elem[1]}, lf.sign_{elem[1]})\n')
			f.write(f'\t\tself.sb_sign_{elem[1]}_changed(self.sb_sign_{elem[1]}, lf.sign_{elem[1]})\n')
		if elem[0] == 'redpitaya_converters_12':
			f.write('\t\tself.listView_acdc1.select_by_value(lf.listView_acdc1)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH1 ,int(lf.listView_acdc1=="ADC1 AC"))\n')
			f.write('\t\tvals.listView_acdc1=lf.listView_acdc1\n')
			f.write('\t\tself.listView_range1.select_by_value(lf.listView_range1)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH1 ,int(lf.listView_range1=="ADC1\\xa01/1"))\n')
			f.write('\t\tvals.listView_range1=lf.listView_range1\n')
			f.write('\t\tself.listView_ampl1.select_by_value(lf.listView_ampl1)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH1 ,int(lf.listView_ampl1=="DAC1\\xa010V"))\n')
			f.write('\t\tvals.listView_ampl1=lf.listView_ampl1\n')
			f.write('\t\tself.listView_acdc2.select_by_value(lf.listView_acdc2)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH2 ,int(lf.listView_acdc2=="ADC2 AC"))\n')
			f.write('\t\tvals.listView_acdc2=lf.listView_acdc2\n')
			f.write('\t\tself.listView_range2.select_by_value(lf.listView_range2)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH2 ,int(lf.listView_range2=="ADC2\\xa01/1"))\n')
			f.write('\t\tvals.listView_range2=lf.listView_range2\n')
			f.write('\t\tself.listView_ampl2.select_by_value(lf.listView_ampl2)\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH2 ,int(lf.listView_ampl2=="DAC2\\xa010V"))\n')
			f.write('\t\tvals.listView_ampl2=lf.listView_ampl2\n')
			f.write('\t\tself.listView_extref.select_by_value(lf.listView_extref)\n')
			f.write(f'\t\tliboscimp_fpga.redpitaya_converters_12_ext_ref_enable("/dev/{elem[1]}" ,int(lf.listView_extref=="Ext\\xa0Ref"))\n')
			f.write('\t\tvals.listView_extref=lf.listView_extref\n')
		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn', 'delayTempoReal_axi'] :
			f.write(f'\t\tself.sd_{elem[1]}_changed(self.sd_{elem[1]}, lf.{elem[1]})\n')
			f.write(f'\t\tself.sb_{elem[1]}_changed(self.sb_{elem[1]}, lf.{elem[1]})\n')
		if elem[0] == 'nco_counter':
			f.write(f'\t\tself.sd_pinc_{elem[1]}_changed(self.sd_pinc_{elem[1]}, lf.pinc_{elem[1]})\n')
			f.write(f'\t\tself.sb_pinc_{elem[1]}_changed(self.sb_pinc_{elem[1]}, lf.pinc_{elem[1]})\n')
			f.write(f'\t\tself.sd_poff_{elem[1]}_changed(self.sd_poff_{elem[1]}, lf.poff_{elem[1]})\n')
			f.write(f'\t\tself.sb_poff_{elem[1]}_changed(self.sb_poff_{elem[1]}, lf.poff_{elem[1]})\n')
			f.write(f'\t\tself.cb_pinc_{elem[1]}_changed(self.cb_pinc_{elem[1]}, lf.cb_pinc_{elem[1]})\n')
			f.write(f'\t\tself.cb_poff_{elem[1]}_changed(self.cb_poff_{elem[1]}, lf.cb_poff_{elem[1]})\n')
		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write(f'\t\tself.cb_{elem[1]}_changed(self.cb_{elem[1]}, lf.{elem[1]})\n')

	f.write('\t\tprint("Configuration loaded")\n\n')
	f.write('\tdef bt_save_changed(self, widget):\n')
	f.write('\t\ttry:\n')
	f.write('\t\t\tos.remove(str(vals.config))\n')
	f.write('\t\texcept:\n')
	f.write('\t\t\tpass\n')
	f.write('\t\twith open(str(vals.config), "wb") as f:\n')
	f.write('\t\t\tf.write(lxml.etree.tostring(vals, pretty_print=True))\n')
	f.write('\t\tprint("Saved")\n\n')

	if board_name == "plutosdr":
		f.write('\tdef sd_tx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.tx_lo=value\n')
		f.write('\t\tprint("iio:tx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage1"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sb_tx_lo.set_value(int(value))\n\n')
		f.write('\tdef sb_tx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.tx_lo=value\n')
		f.write('\t\tprint("iio:tx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage1"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sd_tx_lo.set_value(int(float(value)))\n\n')

		f.write('\tdef sd_rx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.rx_lo=value\n')
		f.write('\t\tprint("iio:rx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage0"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sb_rx_lo.set_value(int(value))\n\n')
		f.write('\tdef sb_rx_lo_changed(self, widget, value):\n')
		f.write('\t\tvals.rx_lo=value\n')
		f.write('\t\tprint("iio:rx_lo", int(value))\n')
		f.write('\t\t[i for i in phy.channels if i.id == "altvoltage0"][0].attrs["frequency"].value = value\n')
		f.write('\t\tself.sd_rx_lo.set_value(int(float(value)))\n\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write(f'\tdef sd_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			if 'f0' not in elem[1]:
				f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
				f.write(f'\t\tliboscimp_fpga.add_const_set_offset("/dev/{elem[1]}", int(value))\n')
			else:
				f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
				f.write(f'\t\tliboscimp_fpga.add_const_set_offset("/dev/{elem[1]}", int(round(int(value)/(samp_freq/2**nco_accum_size))))\n')
			f.write(f'\t\tself.sb_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			if 'f0' not in elem[1]:
				f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
				f.write(f'\t\tliboscimp_fpga.add_const_set_offset("/dev/{elem[1]}", int(value))\n')
			else:
				f.write(f'\t\tprint("/dev/{elem[1]}", value)\n')
				f.write(f'\t\tliboscimp_fpga.add_const_set_offset("/dev/{elem[1]}", int(round(float(value)/(samp_freq/2**nco_accum_size))))\n')
			f.write(f'\t\tself.sd_{elem[1]}.set_value(int(float(value)))\n\n')

		if elem[0] == 'axi_to_dac':
			f.write(f'\tdef sd_ch1_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.ch1_{elem[1]}=value\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/{elem[1]}", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n')
			f.write(f'\t\tprint("/dev/{elem[1]} ch1", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/{elem[1]}", liboscimp_fpga.CHANA, int(value))\n')
			f.write(f'\t\tself.sb_ch1_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_ch1_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.ch1_{elem[1]}=value\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/{elem[1]}", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n')
			f.write(f'\t\tprint("/dev/{elem[1]} ch1", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/{elem[1]}", liboscimp_fpga.CHANA, int(value))\n')
			f.write(f'\t\tself.sd_ch1_{elem[1]}.set_value(int(float(value)))\n\n')

			f.write(f'\tdef sd_ch2_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.ch2_{elem[1]}=value\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/{elem[1]}", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n')
			f.write(f'\t\tprint("/dev/{elem[1]} ch2", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/{elem[1]}", liboscimp_fpga.CHANB, int(value))\n')
			f.write(f'\t\tself.sb_ch2_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_ch2_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.ch2_{elem[1]}=value\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/{elem[1]}", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n')
			f.write(f'\t\tprint("/dev/{elem[1]} ch2", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/{elem[1]}", liboscimp_fpga.CHANB, int(value))\n')
			f.write(f'\t\tself.sd_ch2_{elem[1]}.set_value(int(float(value)))\n\n')

		if elem[0] == 'pidv3_axi':
			f.write(f'\tdef sd_kp_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.kp_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/kp", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set("/dev/{elem[1]}", liboscimp_fpga.KP, int(value))\n')
			f.write(f'\t\tself.sb_kp_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_kp_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.kp_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/kp", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set("/dev/{elem[1]}", liboscimp_fpga.KP, int(value))\n')
			f.write(f'\t\tself.sd_kp_{elem[1]}.set_value(int(float(value)))\n\n')

			f.write(f'\tdef sd_ki_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.ki_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/ki", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set("/dev/{elem[1]}", liboscimp_fpga.KI, int(value))\n')
			f.write(f'\t\tself.sb_ki_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_ki_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.ki_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/ki", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set("/dev/{elem[1]}", liboscimp_fpga.KI, int(value))\n')
			f.write(f'\t\tself.sd_ki_{elem[1]}.set_value(int(float(value)))\n\n')
			f.write(f'\tdef cb_rst_int_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.rst_int_{elem[1]}=value\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set_int_rst("/dev/{elem[1]}", 1)\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/rst_int", int(value in (True, "True", "true")))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set_int_rst("/dev/{elem[1]}", int(value in (True, "True", "true")))\n')
			f.write(f'\t\tself.cb_rst_int_{elem[1]}.set_value(int(value in (True, "True", "true")))\n\n')

			f.write(f'\tdef sd_sp_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.sp_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/setpoint", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set_setpoint("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sb_sp_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_sp_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.sp_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/setpoint", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set_setpoint("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sd_sp_{elem[1]}.set_value(int(float(value)))\n\n')

			f.write(f'\tdef sd_sign_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.sign_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/sign", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set_sign("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sb_sign_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_sign_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.sign_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}/sign", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.pidv3_axi_set_sign("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sd_sign_{elem[1]}.set_value(int(float(value)))\n\n')

		if elem[0] == 'redpitaya_converters_12':

			f.write('\tdef display_extref_state(self):\n')
			f.write(f'\t\tref_state=liboscimp_fpga.redpitaya_converters_12_get_ref_status("/dev/{elem[1]}")\n')
			f.write('\t\tif ref_state[1]==1:\n')
			f.write('\t\t\tself.dcolor_extref_state.set_value("#0bff00")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tself.dcolor_extref_state.set_value("#ff0000")\n')
			f.write('\t\tif not self.stop_flag:\n')
			f.write('\t\t\tTimer(0.5, self.display_extref_state).start()\n\n')

			f.write('\tdef listView_acdc1_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_acdc1=self.listView_acdc1.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH1 ,int(vals.listView_acdc1=="ADC1 AC"))\n')
			f.write('\t\tif vals.listView_acdc1=="ADC1 AC":\n')
			f.write('\t\t\tprint("ADC1 AC")\n')
			f.write('\t\t\tself.listView_acdc1.select_by_value("ADC1 AC")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC1 DC")\n')
			f.write('\t\t\tself.listView_acdc1.select_by_value("ADC1 DC")\n\n')

			f.write('\tdef listView_range1_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_range1=self.listView_range1.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH1 ,int(vals.listView_range1=="ADC1\\xa01/1"))\n')
			f.write('\t\tif vals.listView_range1=="ADC1\\xa01/20":\n')
			f.write('\t\t\tprint("ADC1 1/20")\n')
			f.write('\t\t\tself.listView_range1.select_by_value("ADC1\\xa01/20")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC1 1/1")\n')
			f.write('\t\t\tself.listView_range1.select_by_value("ADC1\\xa01/1")\n\n')

			f.write('\tdef listView_ampl1_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_ampl1=self.listView_ampl1.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH1 ,int(vals.listView_ampl1=="DAC1\\xa010V"))\n')
			f.write('\t\tif vals.listView_ampl1=="DAC1\\xa02V":\n')
			f.write('\t\t\tprint("DAC1\\xa02V")\n')
			f.write('\t\t\tself.listView_ampl1.select_by_value("DAC1\\xa02V")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("DAC1\\xa010V")\n')
			f.write('\t\t\tself.listView_ampl1.select_by_value("DAC1\\xa010V")\n\n')

			f.write('\tdef listView_acdc2_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_acdc2=self.listView_acdc2.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAC_DC(liboscimp_fpga.CH2 ,int(vals.listView_acdc2=="ADC2 AC"))\n')
			f.write('\t\tif vals.listView_acdc2=="ADC2 AC":\n')
			f.write('\t\t\tprint("ADC2 AC")\n')
			f.write('\t\t\tself.listView_acdc2.select_by_value("ADC2 AC")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC2 DC")\n')
			f.write('\t\t\tself.listView_acdc2.select_by_value("ADC2 DC")\n\n')

			f.write('\tdef listView_range2_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_range2=self.listView_range2.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setAttenuator(liboscimp_fpga.CH2 ,int(vals.listView_range2=="ADC2\\xa01/1"))\n')
			f.write('\t\tif vals.listView_range2=="ADC2\\xa01/20":\n')
			f.write('\t\t\tprint("ADC2 1/20")\n')
			f.write('\t\t\tself.listView_range2.select_by_value("ADC2\\xa01/20")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("ADC2 1/1")\n')
			f.write('\t\t\tself.listView_range2.select_by_value("ADC2\\xa01/1")\n\n')

			f.write('\tdef listView_ampl2_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_ampl2=self.listView_ampl2.children[selected_item_key].get_text()\n')
			f.write('\t\tliboscimp_fpga.RP_12_setGainOut(liboscimp_fpga.CH2 ,int(vals.listView_ampl2=="DAC2\\xa010V"))\n')
			f.write('\t\tif vals.listView_ampl2=="DAC2\\xa02V":\n')
			f.write('\t\t\tprint("DAC2\\xa02V")\n')
			f.write('\t\t\tself.listView_ampl2.select_by_value("DAC2\\xa02V")\n')
			f.write('\t\telse :\n')
			f.write('\t\t\tprint("DAC2\\xa010V")\n')
			f.write('\t\t\tself.listView_ampl2.select_by_value("DAC2\\xa010V")\n\n')

			f.write('\tdef listView_extref_changed(self, widget, selected_item_key):\n')
			f.write('\t\tvals.listView_extref=self.listView_extref.children[selected_item_key].get_text()\n')
			f.write(f'\t\tliboscimp_fpga.redpitaya_converters_12_ext_ref_enable("/dev/{elem[1]}" ,int(vals.listView_extref=="Ext\\xa0Ref"))\n')
			f.write('\t\tif vals.listView_extref=="Ext\\xa0Ref":\n')
			f.write(f'\t\t\tprint("/dev/{elem[1]}","Ext\\xa0Ref")\n')
			f.write('\t\t\tself.listView_extref.select_by_value("Ext\\xa0Ref")\n')
			f.write('\t\telse :\n')
			f.write(f'\t\t\tprint("/dev/{elem[1]}","Int\\xa0Clock")\n')
			f.write('\t\t\tself.listView_extref.select_by_value("Int\\xa0Clock")\n\n')

		if elem[0] in ['shifterReal_dyn', 'shifterComplex_dyn'] :
			f.write(f'\tdef sd_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.shifter_set("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sb_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.shifter_set("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sd_{elem[1]}.set_value(int(float(value)))\n\n')

		if elem[0] == 'delayTempoReal_axi':
			f.write(f'\tdef sd_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.delayTempo_set("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sb_{elem[1]}.set_value(int(value))\n\n')
			f.write(f'\tdef sb_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tliboscimp_fpga.delayTempo_set("/dev/{elem[1]}", int(value))\n')
			f.write(f'\t\tself.sd_{elem[1]}.set_value(int(float(value)))\n\n')

		if elem[0] == 'nco_counter':
			f.write(f'\tdef sd_pinc_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.pinc_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", samp_freq, float(value), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tliboscimp_fpga.nco_counter_send_conf("/dev/{elem[1]}", samp_freq, ctypes.c_double(float(value)), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tself.sb_pinc_{elem[1]}.set_value(float(value))\n\n')
			f.write(f'\tdef sb_pinc_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.pinc_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", samp_freq, value, nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tliboscimp_fpga.nco_counter_send_conf("/dev/{elem[1]}", samp_freq, ctypes.c_double(float(value)), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tself.sd_pinc_{elem[1]}.set_value(value)\n\n')
			f.write(f'\tdef sd_poff_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.poff_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", samp_freq, self.sb_pinc_{elem[1]}.get_value(), nco_accum_size, int(value), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tliboscimp_fpga.nco_counter_send_conf("/dev/{elem[1]}", samp_freq, ctypes.c_double(float(self.sb_pinc_{elem[1]}.get_value())), nco_accum_size, int(value), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tself.sb_poff_{elem[1]}.set_value(value)\n\n')
			f.write(f'\tdef sb_poff_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.poff_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", samp_freq, self.sb_pinc_{elem[1]}.get_value(), nco_accum_size, int(value), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tliboscimp_fpga.nco_counter_send_conf("/dev/{elem[1]}", samp_freq, ctypes.c_double(float(self.sb_pinc_{elem[1]}.get_value())), nco_accum_size, int(value), int(self.cb_pinc_{elem[1]}.get_value()), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tself.sd_poff_{elem[1]}.set_value(value)\n\n')
			f.write(f'\tdef cb_pinc_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.cb_pinc_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", samp_freq, self.sb_pinc_{elem[1]}.get_value(), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(value in (True, "True", "true")), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tliboscimp_fpga.nco_counter_send_conf("/dev/{elem[1]}", samp_freq, ctypes.c_double(float(self.sb_pinc_{elem[1]}.get_value())), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(value in (True, "True", "true")), int(self.cb_poff_{elem[1]}.get_value()))\n')
			f.write(f'\t\tself.cb_pinc_{elem[1]}.set_value(int(value in (True, "True", "true")))\n\n')
			f.write(f'\tdef cb_poff_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.cb_poff_{elem[1]}=value\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", samp_freq, self.sb_pinc_{elem[1]}.get_value(), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(self.cb_pinc_{elem[1]}.get_value()), int(value in (True, "True", "true")))\n')
			f.write(f'\t\tliboscimp_fpga.nco_counter_send_conf("/dev/{elem[1]}", samp_freq, ctypes.c_double(float(self.sb_pinc_{elem[1]}.get_value())), nco_accum_size, int(self.sb_poff_{elem[1]}.get_value()), int(self.cb_pinc_{elem[1]}.get_value()), int(value in (True, "True", "true")))\n')
			f.write(f'\t\tself.cb_poff_{elem[1]}.set_value(int(value in (True, "True", "true")))\n\n')

		if elem[0] in ['switchReal', 'switchComplex'] :
			f.write(f'\tdef cb_{elem[1]}_changed(self, widget, value):\n')
			f.write(f'\t\tvals.{elem[1]}=value\n')
			f.write(f'\t\tliboscimp_fpga.switch_send_conf("/dev/{elem[1]}", 1)\n')
			f.write(f'\t\tprint("/dev/{elem[1]}", int(value in (True, "True", "true")))\n')
			f.write(f'\t\tliboscimp_fpga.switch_send_conf("/dev/{elem[1]}", int(value in (True, "True", "true")))\n')
			f.write(f'\t\tself.cb_{elem[1]}.set_value(int(value in (True, "True", "true")))\n\n')

	if board_name == "plutosdr":
		f.write(f'start(MyApp, address="0.0.0.0", port=8080, title="{name}_webserver")\n')
	else:
		f.write(f'start(MyApp, address="0.0.0.0", port=80, title="{name}_webserver")\n')

	os.chmod(f'{name}_webserver.py', stat.S_IRWXU | stat.S_IRGRP |
		 stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)

print('\ndone')
