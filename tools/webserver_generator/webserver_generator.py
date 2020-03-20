#!/usr/bin/env python

from xml.dom import minidom
import sys
import os

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
	os.remove('%s_webserver.py'%name)
except:
	pass

with open('%s_webserver.py'%name, 'a') as f:
	f.write('#!/usr/bin/env python\n\n')
	f.write('import liboscimp_fpga\n')
	f.write('import ctypes\n')
	f.write('import os\n')
	f.write('from lxml import objectify\n')
	f.write('import lxml.etree\n')
	f.write('import remi.gui as gui\n')
	f.write('from remi import start, App\n\n')

	f.write('vals = objectify.Element("item")\n')
	f.write('vals.config = "%s_defconf.xml"\n'%name)
	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write('vals.%s = 0\n'%elem[1])

		if elem[0] == 'axi_to_dac':
			f.write('vals.ch1_%s = 0\n'%elem[1])
			f.write('vals.ch2_%s = 0\n'%elem[1])

		if elem[0] == 'pidv3_axi':
			f.write('vals.kp_%s = 0\n'%elem[1])
			f.write('vals.ki_%s = 0\n'%elem[1])
			f.write('vals.rst_int_%s = "true"\n'%elem[1])
			f.write('vals.sp_%s = 0\n'%elem[1])
			f.write('vals.sign_%s = 0\n'%elem[1])

		if elem[0] == 'shiterReal_dyn':
			f.write('vals.%s = 9\n'%elem[1])

		if elem[0] == 'nco_counter':
			f.write('vals.pinc_%s = 0\n'%elem[1])
			f.write('vals.poff_%s = 0\n'%elem[1])
			f.write('vals.cb_pinc_%s = "true"\n'%elem[1])
			f.write('vals.cb_poff_%s = "true"\n'%elem[1])

		if elem[0] == 'switchReal':
			f.write('vals.%s = "true"\n'%elem[1])

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

	for elem in board_driver_array:
		print('%s\t%s'%(elem[1], elem[0]))

		if elem[0] == 'add_constReal':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("/dev/%s", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			if 'f0' not in elem[1]:
				f.write('\t\tself.sd_%s = gui.Slider(vals.%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1],elem[1]))
			else:
				f.write('\t\tself.sd_%s = gui.Slider(vals.%s, 0, 62500000, 1, width="60%%", margin="10px")\n'%(elem[1],elem[1]))
			f.write('\t\tself.sd_%s.set_oninput_listener(self.sd_%s_changed)\n'%(elem[1], elem[1]))
			if 'f0' not in elem[1]:
				f.write('\t\tself.sb_%s = gui.SpinBox(vals.%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1],elem[1]))
			else:
				f.write('\t\tself.sb_%s = gui.SpinBox(vals.%s, 0, 62500000, 0.02, width="20%%", margin="10px")\n'%(elem[1],elem[1]))
			f.write('\t\tself.sb_%s.set_on_change_listener(self.sb_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s_changed(self.sd_%s, self.sd_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])

		if elem[0] == 'axi_to_dac':
			f.write('\t\tself.hbox_ch1_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_ch1_%s = gui.Label("/dev/%s/1", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch1_%s = gui.Slider(vals.ch1_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch1_%s.set_oninput_listener(self.sd_ch1_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch1_%s = gui.SpinBox(vals.ch1_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch1_%s.set_on_change_listener(self.sb_ch1_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch1_%s_changed(self.sd_ch1_%s, self.sd_ch1_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_ch1_%s.append(self.lb_ch1_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch1_%s.append(self.sd_ch1_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch1_%s.append(self.sb_ch1_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_ch1_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_ch2_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_ch2_%s = gui.Label("/dev/%s/2", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s = gui.Slider(vals.ch2_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s.set_oninput_listener(self.sd_ch2_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch2_%s = gui.SpinBox(vals.ch2_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ch2_%s.set_on_change_listener(self.sb_ch2_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s_changed(self.sd_ch2_%s, self.sd_ch2_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_ch2_%s.append(self.lb_ch2_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch2_%s.append(self.sd_ch2_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ch2_%s.append(self.sb_ch2_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_ch2_%s)\n\n'%elem[1])

		if elem[0] == 'pidv3_axi':
			f.write('\t\tself.hbox_kp_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_kp_%s = gui.Label("/dev/%s/kp", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_kp_%s = gui.Slider(vals.kp_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_kp_%s.set_oninput_listener(self.sd_kp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_kp_%s = gui.SpinBox(vals.kp_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_kp_%s.set_on_change_listener(self.sb_kp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_kp_%s_changed(self.sd_kp_%s, self.sd_kp_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_kp_%s.append(self.lb_kp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_kp_%s.append(self.sd_kp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_kp_%s.append(self.sb_kp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_kp_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_ki_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_ki_%s = gui.Label("/dev/%s/ki", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s = gui.Slider(vals.ki_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s.set_oninput_listener(self.sd_ki_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ki_%s = gui.SpinBox(vals.ki_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_ki_%s.set_on_change_listener(self.sb_ki_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s_changed(self.sd_ki_%s, self.sd_ki_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_rst_int_%s = gui.CheckBoxLabel("rst_int", vals.rst_int_%s, width="5%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_rst_int_%s.set_on_change_listener(self.cb_rst_int_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.lb_ki_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.sd_ki_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.sb_ki_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_ki_%s.append(self.cb_rst_int_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_ki_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_sp_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_sp_%s = gui.Label("/dev/%s/setpoint", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s = gui.Slider(vals.sp_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s.set_oninput_listener(self.sd_sp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sp_%s = gui.SpinBox(vals.sp_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sp_%s.set_on_change_listener(self.sb_sp_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s_changed(self.sd_sp_%s, self.sd_sp_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_sp_%s.append(self.lb_sp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sp_%s.append(self.sd_sp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sp_%s.append(self.sb_sp_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_sp_%s)\n\n'%elem[1])

			f.write('\t\tself.hbox_sign_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_sign_%s = gui.Label("/dev/%s/sign", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s = gui.Slider(vals.sign_%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s.set_oninput_listener(self.sd_sign_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sign_%s = gui.SpinBox(vals.sign_%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_sign_%s.set_on_change_listener(self.sb_sign_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s_changed(self.sd_sign_%s, self.sd_sign_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_sign_%s.append(self.lb_sign_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sign_%s.append(self.sd_sign_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_sign_%s.append(self.sb_sign_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_sign_%s)\n\n'%elem[1])

		if elem[0] == 'shiterReal_dyn':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("/dev/%s", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s = gui.Slider(vals.%s, -8192, 8191, 1, width="60%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s.set_oninput_listener(self.sd_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_%s = gui.SpinBox(vals.%s, -8192, 8191, 1, width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_%s.set_on_change_listener(self.sb_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_%s_changed(self.sd_%s, self.sd_%s.get_value())\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])


		if elem[0] == 'nco_counter':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.lb_%s = gui.Label("/dev/%s", width="20%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_pinc_%s = gui.Slider(vals.pinc_%s, 0, 62500000, 1, width="25%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_pinc_%s.set_oninput_listener(self.sd_pinc_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s = gui.SpinBox(vals.pinc_%s, 0, 62500000, 0.02, width="10%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s.set_on_change_listener(self.sb_pinc_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s = gui.Slider(vals.poff_%s, -8192, 8191, 1, width="25%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s.set_oninput_listener(self.sd_poff_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s = gui.SpinBox(vals.poff_%s, -8192, 8191, 1, width="10%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s.set_on_change_listener(self.sb_poff_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s = gui.CheckBoxLabel("pinc", vals.cb_pinc_%s, width="5%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s.set_on_change_listener(self.cb_pinc_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s = gui.CheckBoxLabel("poff", vals.cb_poff_%s, width="5%%", margin="10px")\n'%(elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s.set_on_change_listener(self.cb_poff_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.lb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_pinc_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_pinc_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sd_poff_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.sb_poff_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.cb_pinc_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.cb_poff_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])

		if elem[0] == 'switchReal':
			f.write('\t\tself.hbox_%s = gui.HBox(margin="10px")\n'%elem[1])
			f.write('\t\tself.cb_%s = gui.CheckBoxLabel("%s", vals.%s, width="5%%", margin="10px")\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_%s.set_on_change_listener(self.cb_%s_changed)\n'%(elem[1], elem[1]))
			f.write('\t\tself.hbox_%s.append(self.cb_%s)\n'%(elem[1], elem[1]))
			f.write('\t\tself.w.append(self.hbox_%s)\n\n'%elem[1])

	f.write('\t\treturn self.w\n\n')

	f.write('\tdef dtext_conf_file_changed(self, widget, value):\n')
	f.write('\t\tprint(value)\n')
	f.write('\t\tvals.config=value\n\n')

	f.write('\tdef bt_load_changed(self, widget):\n')
	f.write('\t\twith open(str(vals.config), "r") as f:\n')
	f.write('\t\t\t lf = objectify.fromstring(f.read())\n\n')

	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write('\t\tself.sd_%s_changed(self.sd_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_%s_changed(self.sb_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'axi_to_dac':
			f.write('\t\tself.sd_ch1_%s_changed(self.sd_ch1_%s, lf.ch1_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_ch1_%s_changed(self.sd_ch1_%s, lf.ch1_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_ch2_%s_changed(self.sb_ch2_%s, lf.ch2_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_ch2_%s_changed(self.sb_ch2_%s, lf.ch2_%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'pidv3_axi':
			f.write('\t\tself.sd_kp_%s_changed(self.sd_kp_%s, lf.kp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_kp_%s_changed(self.sb_kp_%s, lf.kp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_ki_%s_changed(self.sd_ki_%s, lf.ki_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_ki_%s_changed(self.sb_ki_%s, lf.ki_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_rst_int_%s_changed(self.cb_rst_int_%s, lf.rst_int_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_sp_%s_changed(self.sd_sp_%s, lf.sp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_sp_%s_changed(self.sb_sp_%s, lf.sp_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_sign_%s_changed(self.sd_sign_%s, lf.sign_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_sign_%s_changed(self.sb_sign_%s, lf.sign_%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'shiterReal_dyn':
			f.write('\t\tself.sd_%s_changed(self.sd_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_%s_changed(self.sb_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'nco_counter':
			f.write('\t\tself.sd_pinc_%s_changed(self.sd_pinc_%s, lf.pinc_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s_changed(self.sb_pinc_%s, lf.pinc_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s_changed(self.sd_poff_%s, lf.poff_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s_changed(self.sb_poff_%s, lf.poff_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s_changed(self.cb_pinc_%s, lf.cb_pinc_%s)\n'%(elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s_changed(self.cb_poff_%s, lf.cb_poff_%s)\n'%(elem[1], elem[1], elem[1]))
		if elem[0] == 'switchReal':
			f.write('\t\tself.cb_%s_changed(self.cb_%s, lf.%s)\n'%(elem[1], elem[1], elem[1]))

	f.write('\t\tprint("Configuration loaded")\n\n')
	f.write('\tdef bt_save_changed(self, widget):\n')
	f.write('\t\ttry:\n')
	f.write('\t\t\tos.remove(str(vals.config))\n')
	f.write('\t\texcept:\n')
	f.write('\t\t\tpass\n')
	f.write('\t\twith open(str(vals.config), "wb") as f:\n')
	f.write('\t\t\tf.write(lxml.etree.tostring(vals, pretty_print=True))\n')
	f.write('\t\tprint("Saved")\n\n')


	for elem in board_driver_array:
		if elem[0] == 'add_constReal':
			f.write('\tdef sd_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			if 'f0' not in elem[1]:
				f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(value))\n'%elem[1])
			else:
				f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(round(int(value)/(125e6/2**32))))\n'%elem[1])
			f.write('\t\tself.sb_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			if 'f0' not in elem[1]:
				f.write('\t\tprint("/dev/%s", int(value))\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(value))\n'%elem[1])
			else:
				f.write('\t\tprint("/dev/%s", value)\n'%elem[1])
				f.write('\t\tliboscimp_fpga.add_const_set_offset("/dev/%s", int(round(float(value)/(125e6/2**32))))\n'%elem[1])
			f.write('\t\tself.sd_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'axi_to_dac':
			f.write('\tdef sd_ch1_%s_changed(self, widget, value):\n'% elem[1])
			f.write('\t\tvals.ch1_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch1", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANA, int(value))\n'%elem[1])
			f.write('\t\tself.sb_ch1_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_ch1_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ch1_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch1", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANA, int(value))\n'%elem[1])
			f.write('\t\tself.sd_ch1_%s.set_value(int(float(value)))\n\n'%elem[1])

			f.write('\tdef sd_ch2_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ch2_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch2", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANB, int(value))\n'%elem[1])
			f.write('\t\tself.sb_ch2_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_ch2_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ch2_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_conf_enable("/dev/%s", liboscimp_fpga.BOTH_ALWAYS_HIGH)\n'%elem[1])
			f.write('\t\tprint("/dev/%s ch2", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.axi_to_dac_set_chan("/dev/%s", liboscimp_fpga.CHANB, int(value))\n'%elem[1])
			f.write('\t\tself.sd_ch2_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'pidv3_axi':
			f.write('\tdef sd_kp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.kp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/kp", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KP, int(value))\n'%elem[1])
			f.write('\t\tself.sb_kp_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_kp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.kp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/kp", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KP, int(value))\n'%elem[1])
			f.write('\t\tself.sd_kp_%s.set_value(int(float(value)))\n\n'%elem[1])

			f.write('\tdef sd_ki_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ki_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/ki", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KI, int(value))\n'%elem[1])
			f.write('\t\tself.sb_ki_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_ki_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.ki_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/ki", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.KI, int(value))\n'%elem[1])
			f.write('\t\tself.sd_ki_%s.set_value(int(float(value)))\n\n'%elem[1])
			f.write('\tdef cb_rst_int_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.rst_int_%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_int_rst("/dev/%s", 1)\n'%elem[1])
			f.write('\t\tprint("/dev/%s/rst_int", int(value=="true"))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_int_rst("/dev/%s", int(value=="true"))\n'%elem[1])
			f.write('\t\tself.cb_rst_int_%s.set_value(int(value=="true"))\n\n'%elem[1])

			f.write('\tdef sd_sp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/setpoint", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.SETPOINT, int(value))\n'%elem[1])
			f.write('\t\tself.sb_sp_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_sp_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sp_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/setpoint", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set("/dev/%s", liboscimp_fpga.SETPOINT, int(value))\n'%elem[1])
			f.write('\t\tself.sd_sp_%s.set_value(int(float(value)))\n\n'%elem[1])

			f.write('\tdef sd_sign_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sign_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/sign", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_sign("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sb_sign_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_sign_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.sign_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s/sign", int(value))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.pidv3_axi_set_sign("/dev/%s", int(value))\n'%elem[1])
			f.write('\t\tself.sd_sign_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'shiterReal_dyn':
			f.write('\tdef sd_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", ctypes.c_int32(int(value)))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.shifter_set("/dev/%s".encode("utf-8"), ctypes.c_int32(int(value)))\n'%elem[1])
			f.write('\t\tself.sb_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", ctypes.c_int32(int(value)))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.shifter_set("/dev/%s".encode("utf-8"), ctypes.c_int32(int(value)))\n'%elem[1])
			f.write('\t\tself.sd_%s.set_value(int(float(value)))\n\n'%elem[1])

		if elem[0] == 'nco_counter':
			f.write('\tdef sd_pinc_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.pinc_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", 125000000, int(value), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_pinc_%s.set_value(int(value))\n\n'%elem[1])
			f.write('\tdef sb_pinc_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.pinc_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", 125000000, value, 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_pinc_%s.set_value(value)\n\n'%elem[1])
			f.write('\tdef sd_poff_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.poff_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", 125000000, self.sb_pinc_%s.get_value(), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sb_poff_%s.set_value(value)\n\n'%elem[1])
			f.write('\tdef sb_poff_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.poff_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", 125000000, self.sb_pinc_%s.get_value(), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(value), int(self.cb_pinc_%s.get_value()), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.sd_poff_%s.set_value(value)\n\n'%elem[1])
			f.write('\tdef cb_pinc_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.cb_pinc_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", 125000000, self.sb_pinc_%s.get_value(), 40, int(self.sb_poff_%s.get_value()), int(value=="true"), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(self.sb_poff_%s.get_value()), int(value == "true"), int(self.cb_poff_%s.get_value()))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_pinc_%s.set_value(int(value=="true"))\n\n'%elem[1])
			f.write('\tdef cb_poff_%s_changed(self, widget, value):\n'%elem[1])
			f.write('\t\tvals.cb_poff_%s=value\n'%elem[1])
			f.write('\t\tprint("/dev/%s", 125000000, self.sb_pinc_%s.get_value(), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(value=="true"))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tliboscimp_fpga.nco_counter_send_conf("/dev/%s".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_%s.get_value())), 40, int(self.sb_poff_%s.get_value()), int(self.cb_pinc_%s.get_value()), int(value=="true"))\n'%(elem[1], elem[1], elem[1], elem[1]))
			f.write('\t\tself.cb_poff_%s.set_value(int(value=="true"))\n\n'%elem[1])

		if elem[0] == 'switchReal':
			f.write('\tdef cb_%s_changed(self, widget, value):\n'%(elem[1], elem[1]))
			f.write('\t\tvals.%s=value\n'%elem[1])
			f.write('\t\tliboscimp_fpga.switch_send_conf("/dev/%s".encode("utf-8"), 1)\n'%elem[1])
			f.write('\t\tprint("/dev/%s", int(value=="true"))\n'%elem[1])
			f.write('\t\tliboscimp_fpga.switch_send_conf("/dev/%s".encode("utf-8"), int(value=="true"))\n'%elem[1])
			f.write('\t\tself.cb_%s.set_value(int(value=="true"))\n\n'%elem[1])

	f.write('start(MyApp, address="0.0.0.0", port=80, title="%s_webserver")\n'%name)

	os.chmod('%s_webserver.py'%name, 0755)

print('\ndone')