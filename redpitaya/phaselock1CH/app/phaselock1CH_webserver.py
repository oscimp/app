#!/usr/bin/env python
import liboscimp_fpga
import ctypes
import os
from lxml import objectify
import lxml.etree
import remi.gui as gui
from remi import start, App
import sys

vals = objectify.Element("item")
vals.config = "phaselock1CH_defconf.xml"
vals.dds1_f0 = 0
vals.pinc_dds1_nco = 0
vals.poff_dds1_nco = 0
vals.cb_pinc_dds1_nco = "true"
vals.cb_poff_dds1_nco = "true"
vals.ch1_dds_ampl = 0
vals.ch1_dds_range = 0
vals.pinc_demod1_nco = 0
vals.poff_demod1_nco = 0
vals.cb_pinc_demod1_nco = "true"
vals.cb_poff_demod1_nco = "true"
vals.mux_filter  = 0
vals.mux_ram = 0
vals.mux_pid = 0
vals.mux_out_ch2 = 0
vals.kp_pid1 = 0
vals.ki_pid1 = 0
vals.rst_int_pid1 = "true"
vals.sp_pid1 = 0
vals.sign_pid1 = 0

IP_ADDR = "0.0.0.0"
verLess37 =( sys.version_info[0]*10 + sys.version_info[1] <= 37)
#verLess37 = False

class MyApp(App):
	def __init__(self, *args):
		super(MyApp, self).__init__(*args)

	def main(self):
		self.w = gui.VBox()

		self.hbox_save_load = gui.HBox(margin="10px")
		self.dtext_conf_file = gui.TextInput(width=200, height=30)
		self.dtext_conf_file.set_value(str(vals.config))
		self.dtext_conf_file.set_on_change_listener(self.dtext_conf_file_changed)
		self.bt_load = gui.Button("Load", width=200, height=30, margin="10px")
		self.bt_load.set_on_click_listener(self.bt_load_changed)
		self.bt_save = gui.Button("Save", width=200, height=30, margin="10px")
		self.bt_save.set_on_click_listener(self.bt_save_changed)
		self.hbox_save_load.append(self.dtext_conf_file)
		self.hbox_save_load.append(self.bt_load)
		self.hbox_save_load.append(self.bt_save)
		self.w.append(self.hbox_save_load)

		self.hbox_dds1_f0 = gui.HBox(margin="10px")
		self.lb_dds1_f0 = gui.Label("/dev/dds1_f0", width="20%", margin="10px")
		self.sd_dds1_f0 = gui.Slider(vals.dds1_f0, 0, 62500000, 1, width="60%", margin="10px")
		self.sd_dds1_f0.set_oninput_listener(self.sd_dds1_f0_changed)
		self.sb_dds1_f0 = gui.SpinBox(vals.dds1_f0, 0, 62500000, 0.02, width="20%", margin="10px")
		self.sb_dds1_f0.set_on_change_listener(self.sb_dds1_f0_changed)
		self.sd_dds1_f0_changed(self.sd_dds1_f0, self.sd_dds1_f0.get_value())
		self.hbox_dds1_f0.append(self.lb_dds1_f0)
		self.hbox_dds1_f0.append(self.sd_dds1_f0)
		self.hbox_dds1_f0.append(self.sb_dds1_f0)
		self.w.append(self.hbox_dds1_f0)

		self.hbox_dds1_nco = gui.HBox(margin="10px")
		self.lb_dds1_nco = gui.Label("/dev/dds1_nco", width="20%", margin="10px")
		self.sd_pinc_dds1_nco = gui.Slider(vals.pinc_dds1_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_dds1_nco.set_oninput_listener(self.sd_pinc_dds1_nco_changed)
		self.sb_pinc_dds1_nco = gui.SpinBox(vals.pinc_dds1_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_dds1_nco.set_on_change_listener(self.sb_pinc_dds1_nco_changed)
		self.sd_poff_dds1_nco = gui.Slider(vals.poff_dds1_nco, -2048, 2047, 1, width="25%", margin="10px") # IR 12bit range
		self.sd_poff_dds1_nco.set_oninput_listener(self.sd_poff_dds1_nco_changed)
		self.sb_poff_dds1_nco = gui.SpinBox(vals.poff_dds1_nco, -2048, 2047, 1, width="10%", margin="10px") # IR 12bit range
		self.sb_poff_dds1_nco.set_on_change_listener(self.sb_poff_dds1_nco_changed)
		self.cb_pinc_dds1_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_dds1_nco, width="5%", margin="10px")
		self.cb_pinc_dds1_nco.set_on_change_listener(self.cb_pinc_dds1_nco_changed)
		self.cb_poff_dds1_nco = gui.CheckBoxLabel("poff", vals.cb_poff_dds1_nco, width="5%", margin="10px")
		self.cb_poff_dds1_nco.set_on_change_listener(self.cb_poff_dds1_nco_changed)
		self.hbox_dds1_nco.append(self.lb_dds1_nco)
		self.hbox_dds1_nco.append(self.sd_pinc_dds1_nco)
		self.hbox_dds1_nco.append(self.sb_pinc_dds1_nco)
		self.hbox_dds1_nco.append(self.sd_poff_dds1_nco)
		self.hbox_dds1_nco.append(self.sb_poff_dds1_nco)
		self.hbox_dds1_nco.append(self.cb_pinc_dds1_nco)
		self.hbox_dds1_nco.append(self.cb_poff_dds1_nco)
		self.w.append(self.hbox_dds1_nco)

		self.hbox_ch1_dds_ampl = gui.HBox(margin="10px")
		self.lb_ch1_dds_ampl = gui.Label("/dev/dds_ampl/1", width="20%", margin="10px")
		self.sd_ch1_dds_ampl = gui.Slider(vals.ch1_dds_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_dds_ampl.set_oninput_listener(self.sd_ch1_dds_ampl_changed)
		self.sb_ch1_dds_ampl = gui.SpinBox(vals.ch1_dds_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_dds_ampl.set_on_change_listener(self.sb_ch1_dds_ampl_changed)
		self.sd_ch1_dds_ampl_changed(self.sd_ch1_dds_ampl, self.sd_ch1_dds_ampl.get_value())
		self.hbox_ch1_dds_ampl.append(self.lb_ch1_dds_ampl)
		self.hbox_ch1_dds_ampl.append(self.sd_ch1_dds_ampl)
		self.hbox_ch1_dds_ampl.append(self.sb_ch1_dds_ampl)
		self.w.append(self.hbox_ch1_dds_ampl)

		self.hbox_ch1_dds_range = gui.HBox(margin="10px")
		self.lb_ch1_dds_range = gui.Label("/dev/dds_range/1", width="20%", margin="10px")
		self.sd_ch1_dds_range = gui.Slider(vals.ch1_dds_range, -128, 127, 1, width="60%", margin="10px") # IR 8bit range
		self.sd_ch1_dds_range.set_oninput_listener(self.sd_ch1_dds_range_changed)
		self.sb_ch1_dds_range = gui.SpinBox(vals.ch1_dds_range, -128, 127, 1, width="20%", margin="10px") # IR 8bit range
		self.sb_ch1_dds_range.set_on_change_listener(self.sb_ch1_dds_range_changed)
		self.sd_ch1_dds_range_changed(self.sd_ch1_dds_range, self.sd_ch1_dds_range.get_value())
		self.hbox_ch1_dds_range.append(self.lb_ch1_dds_range)
		self.hbox_ch1_dds_range.append(self.sd_ch1_dds_range)
		self.hbox_ch1_dds_range.append(self.sb_ch1_dds_range)
		self.w.append(self.hbox_ch1_dds_range)

		self.hbox_demod1_nco = gui.HBox(margin="10px")
		self.lb_demod1_nco = gui.Label("/dev/demod1_nco", width="20%", margin="10px")
		self.sd_pinc_demod1_nco = gui.Slider(vals.pinc_demod1_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_demod1_nco.set_oninput_listener(self.sd_pinc_demod1_nco_changed)
		self.sb_pinc_demod1_nco = gui.SpinBox(vals.pinc_demod1_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_demod1_nco.set_on_change_listener(self.sb_pinc_demod1_nco_changed)
		self.sd_poff_demod1_nco = gui.Slider(vals.poff_demod1_nco, -2048, 2047, 1, width="25%", margin="10px") # IR 12bit range
		self.sd_poff_demod1_nco.set_oninput_listener(self.sd_poff_demod1_nco_changed)
		self.sb_poff_demod1_nco = gui.SpinBox(vals.poff_demod1_nco, -2048, 2047, 1, width="10%", margin="10px") # IR 12bit range
		self.sb_poff_demod1_nco.set_on_change_listener(self.sb_poff_demod1_nco_changed)
		self.cb_pinc_demod1_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_demod1_nco, width="5%", margin="10px")
		self.cb_pinc_demod1_nco.set_on_change_listener(self.cb_pinc_demod1_nco_changed)
		self.cb_poff_demod1_nco = gui.CheckBoxLabel("poff", vals.cb_poff_demod1_nco, width="5%", margin="10px")
		self.cb_poff_demod1_nco.set_on_change_listener(self.cb_poff_demod1_nco_changed)
		self.hbox_demod1_nco.append(self.lb_demod1_nco)
		self.hbox_demod1_nco.append(self.sd_pinc_demod1_nco)
		self.hbox_demod1_nco.append(self.sb_pinc_demod1_nco)
		self.hbox_demod1_nco.append(self.sd_poff_demod1_nco)
		self.hbox_demod1_nco.append(self.sb_poff_demod1_nco)
		self.hbox_demod1_nco.append(self.cb_pinc_demod1_nco)
		self.hbox_demod1_nco.append(self.cb_poff_demod1_nco)
		self.w.append(self.hbox_demod1_nco)

		self.hbox_mux_filter = gui.HBox(margin="10px")
		self.lb_mux_filter = gui.Label("/dev/mux_filter", width="20%", margin="10px")
		self.sd_mux_filter = gui.Slider(vals.mux_filter, 0, 3, 1, width="60%", margin="10px")
		self.sd_mux_filter.set_oninput_listener(self.sd_mux_filter_changed)
		self.sb_mux_filter = gui.SpinBox(vals.mux_filter,0, 3, 1, width="20%", margin="10px")
		self.sb_mux_filter.set_on_change_listener(self.sb_mux_filter_changed)
		self.sd_mux_filter_changed(self.sd_mux_filter, self.sd_mux_filter.get_value())
		self.hbox_mux_filter.append(self.lb_mux_filter)
		self.hbox_mux_filter.append(self.sd_mux_filter)
		self.hbox_mux_filter.append(self.sb_mux_filter)
		self.w.append(self.hbox_mux_filter)

		self.hbox_mux_ram = gui.HBox(margin="10px")
		self.lb_mux_ram = gui.Label("/dev/mux_ram", width="20%", margin="10px")
		self.sd_mux_ram = gui.Slider(vals.mux_ram, 0, 3, 1, width="60%", margin="10px")
		self.sd_mux_ram.set_oninput_listener(self.sd_mux_ram_changed)
		self.sb_mux_ram = gui.SpinBox(vals.mux_ram,0, 3, 1, width="20%", margin="10px")
		self.sb_mux_ram.set_on_change_listener(self.sb_mux_ram_changed)
		self.sd_mux_ram_changed(self.sd_mux_ram, self.sd_mux_ram.get_value())
		self.hbox_mux_ram.append(self.lb_mux_ram)
		self.hbox_mux_ram.append(self.sd_mux_ram)
		self.hbox_mux_ram.append(self.sb_mux_ram)
		self.w.append(self.hbox_mux_ram)

		self.hbox_mux_pid = gui.HBox(margin="10px")
		self.lb_mux_pid = gui.Label("/dev/mux_pid", width="20%", margin="10px")
		self.sd_mux_pid = gui.Slider(vals.mux_pid, 0, 1, 1, width="60%", margin="10px")
		self.sd_mux_pid.set_oninput_listener(self.sd_mux_pid_changed)
		self.sb_mux_pid = gui.SpinBox(vals.mux_pid,0, 1, 1, width="20%", margin="10px")
		self.sb_mux_pid.set_on_change_listener(self.sb_mux_pid_changed)
		self.sd_mux_pid_changed(self.sd_mux_pid, self.sd_mux_pid.get_value())
		self.hbox_mux_pid.append(self.lb_mux_pid)
		self.hbox_mux_pid.append(self.sd_mux_pid)
		self.hbox_mux_pid.append(self.sb_mux_pid)
		self.w.append(self.hbox_mux_pid)

		self.hbox_mux_out_ch2 = gui.HBox(margin="10px")
		self.lb_mux_out_ch2 = gui.Label("/dev/mux_out_ch2", width="20%", margin="10px")
		self.sd_mux_out_ch2 = gui.Slider(vals.mux_out_ch2, 0, 3, 1, width="60%", margin="10px")
		self.sd_mux_out_ch2.set_oninput_listener(self.sd_mux_out_ch2_changed)
		self.sb_mux_out_ch2 = gui.SpinBox(vals.mux_out_ch2,0, 3, 1, width="20%", margin="10px")
		self.sb_mux_out_ch2.set_on_change_listener(self.sb_mux_out_ch2_changed)
		self.sd_mux_out_ch2_changed(self.sd_mux_out_ch2, self.sd_mux_out_ch2.get_value())
		self.hbox_mux_out_ch2.append(self.lb_mux_out_ch2)
		self.hbox_mux_out_ch2.append(self.sd_mux_out_ch2)
		self.hbox_mux_out_ch2.append(self.sb_mux_out_ch2)
		self.w.append(self.hbox_mux_out_ch2)


		self.hbox_kp_pid1 = gui.HBox(margin="10px")
		self.lb_kp_pid1 = gui.Label("/dev/pid1/kp", width="20%", margin="10px")
		self.sd_kp_pid1 = gui.Slider(vals.kp_pid1, -32768, 32767, 1, width="60%", margin="10px") # IR 16bit range
		self.sd_kp_pid1.set_oninput_listener(self.sd_kp_pid1_changed)
		self.sb_kp_pid1 = gui.SpinBox(vals.kp_pid1, -32768, 32767, 1, width="20%", margin="10px") # IR 16bit range
		self.sb_kp_pid1.set_on_change_listener(self.sb_kp_pid1_changed)
		self.sd_kp_pid1_changed(self.sd_kp_pid1, self.sd_kp_pid1.get_value())
		self.hbox_kp_pid1.append(self.lb_kp_pid1)
		self.hbox_kp_pid1.append(self.sd_kp_pid1)
		self.hbox_kp_pid1.append(self.sb_kp_pid1)
		self.w.append(self.hbox_kp_pid1)

		self.hbox_ki_pid1 = gui.HBox(margin="10px")
		self.lb_ki_pid1 = gui.Label("/dev/pid1/ki", width="20%", margin="10px")
		self.sd_ki_pid1 = gui.Slider(vals.ki_pid1, -32768, 32767, 1, width="60%", margin="10px") # IR 16bit range
		self.sd_ki_pid1.set_oninput_listener(self.sd_ki_pid1_changed)
		self.sb_ki_pid1 = gui.SpinBox(vals.ki_pid1, -32768, 32767, 1, width="20%", margin="10px") # IR 16bit range
		self.sb_ki_pid1.set_on_change_listener(self.sb_ki_pid1_changed)
		self.sd_ki_pid1_changed(self.sd_ki_pid1, self.sd_ki_pid1.get_value())
		self.cb_rst_int_pid1 = gui.CheckBoxLabel("rst_int", vals.rst_int_pid1, width="5%", margin="10px")
		self.cb_rst_int_pid1.set_on_change_listener(self.cb_rst_int_pid1_changed)
		self.hbox_ki_pid1.append(self.lb_ki_pid1)
		self.hbox_ki_pid1.append(self.sd_ki_pid1)
		self.hbox_ki_pid1.append(self.sb_ki_pid1)
		self.hbox_ki_pid1.append(self.cb_rst_int_pid1)
		self.w.append(self.hbox_ki_pid1)

		self.hbox_sp_pid1 = gui.HBox(margin="10px")
		self.lb_sp_pid1 = gui.Label("/dev/pid1/setpoint", width="20%", margin="10px")
		self.sd_sp_pid1 = gui.Slider(vals.sp_pid1, -32768, 32767, 1, width="60%", margin="10px") # IR 16bit range
		self.sd_sp_pid1.set_oninput_listener(self.sd_sp_pid1_changed)
		self.sb_sp_pid1 = gui.SpinBox(vals.sp_pid1, -32768, 32767, 1, width="20%", margin="10px") # IR 16bit range
		self.sb_sp_pid1.set_on_change_listener(self.sb_sp_pid1_changed)
		self.sd_sp_pid1_changed(self.sd_sp_pid1, self.sd_sp_pid1.get_value())
		self.hbox_sp_pid1.append(self.lb_sp_pid1)
		self.hbox_sp_pid1.append(self.sd_sp_pid1)
		self.hbox_sp_pid1.append(self.sb_sp_pid1)
		self.w.append(self.hbox_sp_pid1)

		self.hbox_sign_pid1 = gui.HBox(margin="10px")
		self.lb_sign_pid1 = gui.Label("/dev/pid1/sign 0: err=data-setpoint, 1: err=setpoint-data", width="20%", margin="10px")
		self.sd_sign_pid1 = gui.Slider(vals.sign_pid1, 0, 1, 1, width="60%", margin="10px")
		self.sd_sign_pid1.set_oninput_listener(self.sd_sign_pid1_changed)
		self.sb_sign_pid1 = gui.SpinBox(vals.sign_pid1, 0, 1, 1, width="20%", margin="10px")
		self.sb_sign_pid1.set_on_change_listener(self.sb_sign_pid1_changed)
		self.sd_sign_pid1_changed(self.sd_sign_pid1, self.sd_sign_pid1.get_value())
		self.hbox_sign_pid1.append(self.lb_sign_pid1)
		self.hbox_sign_pid1.append(self.sd_sign_pid1)
		self.hbox_sign_pid1.append(self.sb_sign_pid1)
		self.w.append(self.hbox_sign_pid1)

		return self.w

	def dtext_conf_file_changed(self, widget, value):
		print(value)
		vals.config=value

	def bt_load_changed(self, widget):
		with open(str(vals.config), "r") as f:
			 lf = objectify.fromstring(f.read())

		self.sd_dds1_f0_changed(self.sd_dds1_f0, lf.dds1_f0)
		self.sb_dds1_f0_changed(self.sb_dds1_f0, lf.dds1_f0)
		self.sd_pinc_dds1_nco_changed(self.sd_pinc_dds1_nco, lf.pinc_dds1_nco)
		self.sb_pinc_dds1_nco_changed(self.sb_pinc_dds1_nco, lf.pinc_dds1_nco)
		self.sd_poff_dds1_nco_changed(self.sd_poff_dds1_nco, lf.poff_dds1_nco)
		self.sb_poff_dds1_nco_changed(self.sb_poff_dds1_nco, lf.poff_dds1_nco)
		self.cb_pinc_dds1_nco_changed(self.cb_pinc_dds1_nco, lf.cb_pinc_dds1_nco)
		self.cb_poff_dds1_nco_changed(self.cb_poff_dds1_nco, lf.cb_poff_dds1_nco)
		self.sd_ch1_dds_ampl_changed(self.sd_ch1_dds_ampl, lf.ch1_dds_ampl)
		self.sb_ch1_dds_ampl_changed(self.sd_ch1_dds_ampl, lf.ch1_dds_ampl)
		self.sd_ch1_dds_range_changed(self.sd_ch1_dds_range, lf.ch1_dds_range)
		self.sb_ch1_dds_range_changed(self.sd_ch1_dds_range, lf.ch1_dds_range)
		self.sd_pinc_demod1_nco_changed(self.sd_pinc_demod1_nco, lf.pinc_demod1_nco)
		self.sb_pinc_demod1_nco_changed(self.sb_pinc_demod1_nco, lf.pinc_demod1_nco)
		self.sd_poff_demod1_nco_changed(self.sd_poff_demod1_nco, lf.poff_demod1_nco)
		self.sb_poff_demod1_nco_changed(self.sb_poff_demod1_nco, lf.poff_demod1_nco)
		self.cb_pinc_demod1_nco_changed(self.cb_pinc_demod1_nco, lf.cb_pinc_demod1_nco)
		self.cb_poff_demod1_nco_changed(self.cb_poff_demod1_nco, lf.cb_poff_demod1_nco)
		self.sd_mux_filter_changed(self.sd_mux_filter, lf.mux_filter) 
		self.sb_mux_filter_changed(self.sb_mux_filter, lf.mux_filter) 
		self.sd_mux_ram_changed(self.sd_mux_ram, lf.mux_ram) 
		self.sb_mux_ram_changed(self.sb_mux_ram, lf.mux_ram) 
		self.sd_mux_pid_changed(self.sd_mux_pid, lf.mux_pid) 
		self.sb_mux_pid_changed(self.sb_mux_pid, lf.mux_pid) 
		self.sd_mux_out_ch2_changed(self.sd_mux_out_ch2, lf.mux_out_ch2) 
		self.sb_mux_out_ch2_changed(self.sb_mux_out_ch2, lf.mux_out_ch2) 
		self.sd_kp_pid1_changed(self.sd_kp_pid1, lf.kp_pid1)
		self.sb_kp_pid1_changed(self.sb_kp_pid1, lf.kp_pid1)
		self.sd_ki_pid1_changed(self.sd_ki_pid1, lf.ki_pid1)
		self.sb_ki_pid1_changed(self.sb_ki_pid1, lf.ki_pid1)
		self.cb_rst_int_pid1_changed(self.cb_rst_int_pid1, lf.rst_int_pid1)
		self.sd_sp_pid1_changed(self.sd_sp_pid1, lf.sp_pid1)
		self.sb_sp_pid1_changed(self.sb_sp_pid1, lf.sp_pid1)
		self.sd_sign_pid1_changed(self.sd_sign_pid1, lf.sign_pid1)
		self.sb_sign_pid1_changed(self.sb_sign_pid1, lf.sign_pid1)
		print("Configuration loaded")

	def bt_save_changed(self, widget):
		try:
			os.remove(str(vals.config))
		except:
			pass
		with open(str(vals.config), "wb") as f:
			f.write(lxml.etree.tostring(vals, pretty_print=True))
		print("Saved")

	
	def sd_dds1_f0_changed(self, widget, value):
		vals.dds1_f0=value
		print("/dev/dds1_f0", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dds1_f0", int(round(int(value)/(125e6/2**40))))
		self.sb_dds1_f0.set_value(int(value))

	def sb_dds1_f0_changed(self, widget, value):
		vals.dds1_f0=value
		print("/dev/dds1_f0", value)
		liboscimp_fpga.add_const_set_offset("/dev/dds1_f0", int(round(float(value)/(125e6/2**40))))
		self.sd_dds1_f0.set_value(int(float(value)))

	def sd_pinc_dds1_nco_changed(self, widget, value):
		vals.pinc_dds1_nco=value
		print("/dev/dds1_nco", 125000000, int(value), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		if (verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco", 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))

		self.sb_pinc_dds1_nco.set_value(int(value))

	def sb_pinc_dds1_nco_changed(self, widget, value):
		vals.pinc_dds1_nco=value
		print("/dev/dds1_nco", 125000000, value, 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco", 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		self.sd_pinc_dds1_nco.set_value(value)

	def sd_poff_dds1_nco_changed(self, widget, value):
		vals.poff_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		self.sb_poff_dds1_nco.set_value(value)

	def sb_poff_dds1_nco_changed(self, widget, value):
		vals.poff_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))

		self.sd_poff_dds1_nco.set_value(value)

	def cb_pinc_dds1_nco_changed(self, widget, value):
		vals.cb_pinc_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(self.sb_poff_dds1_nco.get_value()), int(value=="true"), int(self.cb_poff_dds1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(self.sb_poff_dds1_nco.get_value()), int(value == "true"), int(self.cb_poff_dds1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(self.sb_poff_dds1_nco.get_value()), int(value == "true"), int(self.cb_poff_dds1_nco.get_value()))
		self.cb_pinc_dds1_nco.set_value(int(value=="true"))

	def cb_poff_dds1_nco_changed(self, widget, value):
		vals.cb_poff_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(value=="true"))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(value=="true"))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(value=="true"))

		self.cb_poff_dds1_nco.set_value(int(value=="true"))


	def sd_ch1_dds_ampl_changed(self, widget, value):
		vals.ch1_dds_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds1_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_dds_ampl.set_value(int(value))

	def sb_ch1_dds_ampl_changed(self, widget, value):
		vals.ch1_dds_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_dds_ampl.set_value(int(float(value)))

#	def sd_ch2_dds_ampl_changed(self, widget, value):
#		vals.ch2_dds_ampl=value
#		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
#		print("/dev/dds_ampl ch2", int(value))
#		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANB, int(value))
#		self.sb_ch2_dds_ampl.set_value(int(value))

#	def sb_ch2_dds_ampl_changed(self, widget, value):
#		vals.ch2_dds_ampl=value
#		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
#		print("/dev/dds_ampl ch2", int(value))
#		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANB, int(value))
#		self.sd_ch2_dds_ampl.set_value(int(float(value)))

	def sd_ch1_dds_range_changed(self, widget, value):
		vals.ch1_dds_range=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_range", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_range ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_range", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_dds_range.set_value(int(value))

	def sb_ch1_dds_range_changed(self, widget, value):
		vals.ch1_dds_range=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_range", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_range ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_range", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_dds_range.set_value(int(float(value)))


	def sd_pinc_demod1_nco_changed(self, widget, value):
		vals.pinc_demod1_nco=value
		print("/dev/demod1_nco", 125000000, int(value), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco", 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		self.sb_pinc_demod1_nco.set_value(int(value))

	def sb_pinc_demod1_nco_changed(self, widget, value):
		vals.pinc_demod1_nco=value
		print("/dev/demod1_nco", 125000000, value, 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco", 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))

		self.sd_pinc_demod1_nco.set_value(value)

	def sd_poff_demod1_nco_changed(self, widget, value):
		vals.poff_demod1_nco=value
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))

		self.sb_poff_demod1_nco.set_value(value)

	def sb_poff_demod1_nco_changed(self, widget, value):
		vals.poff_demod1_nco=value
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		self.sd_poff_demod1_nco.set_value(value)

	def cb_pinc_demod1_nco_changed(self, widget, value):
		vals.cb_pinc_demod1_nco=value
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(self.sb_poff_demod1_nco.get_value()), int(value=="true"), int(self.cb_poff_demod1_nco.get_value()))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(self.sb_poff_demod1_nco.get_value()), int(value == "true"), int(self.cb_poff_demod1_nco.get_value()))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(self.sb_poff_demod1_nco.get_value()), int(value == "true"), int(self.cb_poff_demod1_nco.get_value()))
		self.cb_pinc_demod1_nco.set_value(int(value=="true"))

	def cb_poff_demod1_nco_changed(self, widget, value):
		vals.cb_poff_demod1_nco=value
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(value=="true"))
		if(verLess37):
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(value=="true"))
		else:
			liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco", 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(value=="true"))
		self.cb_poff_demod1_nco.set_value(int(value=="true"))

	def sd_mux_filter_changed(self, widget, value):
		vals.mux_filter = value
		print("/dev/mux_filter", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_filter",int(value))
		self.sb_mux_filter.set_value(int(value))
#		self.sb_mux_filter.set_value(int(float(value)))

	def sb_mux_filter_changed(self, widget, value):
		vals.mux_filter = value
		print("/dev/mux_filter", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_filter",int(value))
		self.sd_mux_filter.set_value(int(value))
#		self.sd_mux_filter.set_value(int(float(value)))

	def sd_mux_ram_changed(self, widget, value):
		vals.mux_ram = value
		print("/dev/mux_ram", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_ram",int(value))
		self.sb_mux_ram.set_value(int(value))
#		self.sb_mux_ram.set_value(int(float(value)))

	def sb_mux_ram_changed(self, widget, value):
		vals.mux_ram = value
		print("/dev/mux_ram", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_ram",int(value))
		self.sd_mux_ram.set_value(int(value))
#		self.sd_mux_ram.set_value(int(float(value)))

	def sd_mux_pid_changed(self, widget, value):
		vals.mux_pid = value
		print("/dev/mux_pid", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_pid",int(value))
		self.sb_mux_pid.set_value(int(value))
#		self.sb_mux_pid.set_value(int(float(value)))

	def sb_mux_pid_changed(self, widget, value):
		vals.mux_pid = value
		print("/dev/mux_pid", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_pid",int(value))
		self.sd_mux_pid.set_value(int(value))
#		self.sd_mux_pid.set_value(int(float(value)))

	def sd_mux_out_ch2_changed(self, widget, value):
		vals.mux_out_ch2 = value
		print("/dev/mux_out_ch2", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_out_ch2",int(value))
		self.sb_mux_out_ch2.set_value(int(value))
#		self.sb_mux_out_ch2.set_value(int(float(value)))

	def sb_mux_out_ch2_changed(self, widget, value):
		vals.mux_out_ch2 = value
		print("/dev/mux_out_ch2", int(value))
		liboscimp_fpga.switch_send_conf("/dev/mux_out_ch2",int(value))
		self.sd_mux_out_ch2.set_value(int(value))
#		self.sd_mux_out_ch2.set_value(int(float(value)))

	def sd_kp_pid1_changed(self, widget, value):
		vals.kp_pid1=value
		print("/dev/pid1/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KP, int(value))
		self.sb_kp_pid1.set_value(int(value))

	def sb_kp_pid1_changed(self, widget, value):
		vals.kp_pid1=value
		print("/dev/pid1/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KP, int(value))
		self.sd_kp_pid1.set_value(int(float(value)))

	def sd_ki_pid1_changed(self, widget, value):
		vals.ki_pid1=value
		print("/dev/pid1/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KI, int(value))
		self.sb_ki_pid1.set_value(int(value))

	def sb_ki_pid1_changed(self, widget, value):
		vals.ki_pid1=value
		print("/dev/pid1/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KI, int(value))
		self.sd_ki_pid1.set_value(int(float(value)))

	def cb_rst_int_pid1_changed(self, widget, value):
		vals.rst_int_pid1=value
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pid1", 1)
		print("/dev/pid1/rst_int", int(value=="true"))
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pid1", int(value=="true"))
		self.cb_rst_int_pid1.set_value(int(value=="true"))

	def sd_sp_pid1_changed(self, widget, value):
		vals.sp_pid1=value
		print("/dev/pid1/setpoint", int(value))
#		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.SETPOINT, int(value))
		self.sb_sp_pid1.set_value(int(value))

	def sb_sp_pid1_changed(self, widget, value):
		vals.sp_pid1=value
		print("/dev/pid1/setpoint", int(value))
#		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.SETPOINT, int(value))
		self.sd_sp_pid1.set_value(int(float(value)))

	def sd_sign_pid1_changed(self, widget, value):
		vals.sign_pid1=value
		print("/dev/pid1/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pid1", int(value))
		self.sb_sign_pid1.set_value(int(value))

	def sb_sign_pid1_changed(self, widget, value):
		vals.sign_pid1=value
		print("/dev/pid1/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pid1", int(value))
		self.sd_sign_pid1.set_value(int(float(value)))

start(MyApp, address=IP_ADDR, port=80, title="phaselock1CH_webserver")
