#!/usr/bin/env python

import liboscimp_fpga
import ctypes
import os
from lxml import objectify
import lxml.etree
import remi.gui as gui
from remi import start, App

vals = objectify.Element("item")
vals.config = "phase_frequency_modulation_defconf.xml"
vals.pinc_FM_nco = 0
vals.poff_FM_nco = 0
vals.cb_pinc_FM_nco = "true"
vals.cb_poff_FM_nco = "true"
vals.pinc_PM_nco = 0
vals.poff_PM_nco = 0
vals.cb_pinc_PM_nco = "true"
vals.cb_poff_PM_nco = "true"
vals.f0 = 0
vals.ch1_mod_ampl = 0
vals.ch2_mod_ampl = 0
vals.pinc_nco = 0
vals.poff_nco = 0
vals.cb_pinc_nco = "true"
vals.cb_poff_nco = "true"

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

		self.hbox_FM_nco = gui.HBox(margin="10px")
		self.lb_FM_nco = gui.Label("/dev/FM_nco", width="20%", margin="10px")
		self.sd_pinc_FM_nco = gui.Slider(vals.pinc_FM_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_FM_nco.set_oninput_listener(self.sd_pinc_FM_nco_changed)
		self.sb_pinc_FM_nco = gui.SpinBox(vals.pinc_FM_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_FM_nco.set_on_change_listener(self.sb_pinc_FM_nco_changed)
		self.sd_poff_FM_nco = gui.Slider(vals.poff_FM_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_FM_nco.set_oninput_listener(self.sd_poff_FM_nco_changed)
		self.sb_poff_FM_nco = gui.SpinBox(vals.poff_FM_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_FM_nco.set_on_change_listener(self.sb_poff_FM_nco_changed)
		self.cb_pinc_FM_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_FM_nco, width="5%", margin="10px")
		self.cb_pinc_FM_nco.set_on_change_listener(self.cb_pinc_FM_nco_changed)
		self.cb_poff_FM_nco = gui.CheckBoxLabel("poff", vals.cb_poff_FM_nco, width="5%", margin="10px")
		self.cb_poff_FM_nco.set_on_change_listener(self.cb_poff_FM_nco_changed)
		self.hbox_FM_nco.append(self.lb_FM_nco)
		self.hbox_FM_nco.append(self.sd_pinc_FM_nco)
		self.hbox_FM_nco.append(self.sb_pinc_FM_nco)
		self.hbox_FM_nco.append(self.sd_poff_FM_nco)
		self.hbox_FM_nco.append(self.sb_poff_FM_nco)
		self.hbox_FM_nco.append(self.cb_pinc_FM_nco)
		self.hbox_FM_nco.append(self.cb_poff_FM_nco)
		self.w.append(self.hbox_FM_nco)

		self.hbox_PM_nco = gui.HBox(margin="10px")
		self.lb_PM_nco = gui.Label("/dev/PM_nco", width="20%", margin="10px")
		self.sd_pinc_PM_nco = gui.Slider(vals.pinc_PM_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_PM_nco.set_oninput_listener(self.sd_pinc_PM_nco_changed)
		self.sb_pinc_PM_nco = gui.SpinBox(vals.pinc_PM_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_PM_nco.set_on_change_listener(self.sb_pinc_PM_nco_changed)
		self.sd_poff_PM_nco = gui.Slider(vals.poff_PM_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_PM_nco.set_oninput_listener(self.sd_poff_PM_nco_changed)
		self.sb_poff_PM_nco = gui.SpinBox(vals.poff_PM_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_PM_nco.set_on_change_listener(self.sb_poff_PM_nco_changed)
		self.cb_pinc_PM_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_PM_nco, width="5%", margin="10px")
		self.cb_pinc_PM_nco.set_on_change_listener(self.cb_pinc_PM_nco_changed)
		self.cb_poff_PM_nco = gui.CheckBoxLabel("poff", vals.cb_poff_PM_nco, width="5%", margin="10px")
		self.cb_poff_PM_nco.set_on_change_listener(self.cb_poff_PM_nco_changed)
		self.hbox_PM_nco.append(self.lb_PM_nco)
		self.hbox_PM_nco.append(self.sd_pinc_PM_nco)
		self.hbox_PM_nco.append(self.sb_pinc_PM_nco)
		self.hbox_PM_nco.append(self.sd_poff_PM_nco)
		self.hbox_PM_nco.append(self.sb_poff_PM_nco)
		self.hbox_PM_nco.append(self.cb_pinc_PM_nco)
		self.hbox_PM_nco.append(self.cb_poff_PM_nco)
		self.w.append(self.hbox_PM_nco)

		self.hbox_f0 = gui.HBox(margin="10px")
		self.lb_f0 = gui.Label("/dev/f0", width="20%", margin="10px")
		self.sd_f0 = gui.Slider(vals.f0, 0, 62500000, 1, width="60%", margin="10px")
		self.sd_f0.set_oninput_listener(self.sd_f0_changed)
		self.sb_f0 = gui.SpinBox(vals.f0, 0, 62500000, 0.02, width="20%", margin="10px")
		self.sb_f0.set_on_change_listener(self.sb_f0_changed)
		self.sd_f0_changed(self.sd_f0, self.sd_f0.get_value())
		self.hbox_f0.append(self.lb_f0)
		self.hbox_f0.append(self.sd_f0)
		self.hbox_f0.append(self.sb_f0)
		self.w.append(self.hbox_f0)

		self.hbox_ch1_mod_ampl = gui.HBox(margin="10px")
		self.lb_ch1_mod_ampl = gui.Label("/dev/mod_ampl/FM", width="20%", margin="10px")
		self.sd_ch1_mod_ampl = gui.Slider(vals.ch1_mod_ampl, 0, 62500000, 1, width="60%", margin="10px")
		self.sd_ch1_mod_ampl.set_oninput_listener(self.sd_ch1_mod_ampl_changed)
		self.sb_ch1_mod_ampl = gui.SpinBox(vals.ch1_mod_ampl, 0, 62500000, 1, width="20%", margin="10px")
		self.sb_ch1_mod_ampl.set_on_change_listener(self.sb_ch1_mod_ampl_changed)
		self.sd_ch1_mod_ampl_changed(self.sd_ch1_mod_ampl, self.sd_ch1_mod_ampl.get_value())
		self.hbox_ch1_mod_ampl.append(self.lb_ch1_mod_ampl)
		self.hbox_ch1_mod_ampl.append(self.sd_ch1_mod_ampl)
		self.hbox_ch1_mod_ampl.append(self.sb_ch1_mod_ampl)
		self.w.append(self.hbox_ch1_mod_ampl)

		self.hbox_ch2_mod_ampl = gui.HBox(margin="10px")
		self.lb_ch2_mod_ampl = gui.Label("/dev/mod_ampl/PM", width="20%", margin="10px")
		self.sd_ch2_mod_ampl = gui.Slider(vals.ch2_mod_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch2_mod_ampl.set_oninput_listener(self.sd_ch2_mod_ampl_changed)
		self.sb_ch2_mod_ampl = gui.SpinBox(vals.ch2_mod_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch2_mod_ampl.set_on_change_listener(self.sb_ch2_mod_ampl_changed)
		self.sd_ch2_mod_ampl_changed(self.sd_ch2_mod_ampl, self.sd_ch2_mod_ampl.get_value())
		self.hbox_ch2_mod_ampl.append(self.lb_ch2_mod_ampl)
		self.hbox_ch2_mod_ampl.append(self.sd_ch2_mod_ampl)
		self.hbox_ch2_mod_ampl.append(self.sb_ch2_mod_ampl)
		self.w.append(self.hbox_ch2_mod_ampl)

		self.hbox_nco = gui.HBox(margin="10px")
		self.lb_nco = gui.Label("/dev/nco", width="20%", margin="10px")
		self.sd_pinc_nco = gui.Slider(vals.pinc_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_nco.set_oninput_listener(self.sd_pinc_nco_changed)
		self.sb_pinc_nco = gui.SpinBox(vals.pinc_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_nco.set_on_change_listener(self.sb_pinc_nco_changed)
		self.sd_poff_nco = gui.Slider(vals.poff_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_nco.set_oninput_listener(self.sd_poff_nco_changed)
		self.sb_poff_nco = gui.SpinBox(vals.poff_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_nco.set_on_change_listener(self.sb_poff_nco_changed)
		self.cb_pinc_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_nco, width="5%", margin="10px")
		self.cb_pinc_nco.set_on_change_listener(self.cb_pinc_nco_changed)
		self.cb_poff_nco = gui.CheckBoxLabel("poff", vals.cb_poff_nco, width="5%", margin="10px")
		self.cb_poff_nco.set_on_change_listener(self.cb_poff_nco_changed)
		self.hbox_nco.append(self.lb_nco)
		self.hbox_nco.append(self.sd_pinc_nco)
		self.hbox_nco.append(self.sb_pinc_nco)
		self.hbox_nco.append(self.sd_poff_nco)
		self.hbox_nco.append(self.sb_poff_nco)
		self.hbox_nco.append(self.cb_pinc_nco)
		self.hbox_nco.append(self.cb_poff_nco)
		self.w.append(self.hbox_nco)

		return self.w

	def dtext_conf_file_changed(self, widget, value):
		print(value)
		vals.config=value

	def bt_load_changed(self, widget):
		with open(str(vals.config), "r") as f:
			 lf = objectify.fromstring(f.read())

		self.sd_pinc_FM_nco_changed(self.sd_pinc_FM_nco, lf.pinc_FM_nco)
		self.sb_pinc_FM_nco_changed(self.sb_pinc_FM_nco, lf.pinc_FM_nco)
		self.sd_poff_FM_nco_changed(self.sd_poff_FM_nco, lf.poff_FM_nco)
		self.sb_poff_FM_nco_changed(self.sb_poff_FM_nco, lf.poff_FM_nco)
		self.cb_pinc_FM_nco_changed(self.cb_pinc_FM_nco, lf.cb_pinc_FM_nco)
		self.cb_poff_FM_nco_changed(self.cb_poff_FM_nco, lf.cb_poff_FM_nco)
		self.sd_pinc_PM_nco_changed(self.sd_pinc_PM_nco, lf.pinc_PM_nco)
		self.sb_pinc_PM_nco_changed(self.sb_pinc_PM_nco, lf.pinc_PM_nco)
		self.sd_poff_PM_nco_changed(self.sd_poff_PM_nco, lf.poff_PM_nco)
		self.sb_poff_PM_nco_changed(self.sb_poff_PM_nco, lf.poff_PM_nco)
		self.cb_pinc_PM_nco_changed(self.cb_pinc_PM_nco, lf.cb_pinc_PM_nco)
		self.cb_poff_PM_nco_changed(self.cb_poff_PM_nco, lf.cb_poff_PM_nco)
		self.sd_f0_changed(self.sd_f0, lf.f0)
		self.sb_f0_changed(self.sb_f0, lf.f0)
		self.sd_ch1_mod_ampl_changed(self.sd_ch1_mod_ampl, lf.ch1_mod_ampl)
		self.sb_ch1_mod_ampl_changed(self.sd_ch1_mod_ampl, lf.ch1_mod_ampl)
		self.sd_ch2_mod_ampl_changed(self.sb_ch2_mod_ampl, lf.ch2_mod_ampl)
		self.sb_ch2_mod_ampl_changed(self.sb_ch2_mod_ampl, lf.ch2_mod_ampl)
		self.sd_pinc_nco_changed(self.sd_pinc_nco, lf.pinc_nco)
		self.sb_pinc_nco_changed(self.sb_pinc_nco, lf.pinc_nco)
		self.sd_poff_nco_changed(self.sd_poff_nco, lf.poff_nco)
		self.sb_poff_nco_changed(self.sb_poff_nco, lf.poff_nco)
		self.cb_pinc_nco_changed(self.cb_pinc_nco, lf.cb_pinc_nco)
		self.cb_poff_nco_changed(self.cb_poff_nco, lf.cb_poff_nco)
		print("Configuration loaded")

	def bt_save_changed(self, widget):
		try:
			os.remove(str(vals.config))
		except:
			pass
		with open(str(vals.config), "wb") as f:
			f.write(lxml.etree.tostring(vals, pretty_print=True))
		print("Saved")

	def sd_pinc_FM_nco_changed(self, widget, value):
		vals.pinc_FM_nco=value
		print("/dev/FM_nco", 125000000, int(value), 40, int(self.sb_poff_FM_nco.get_value()), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/FM_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_FM_nco.get_value()), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		self.sb_pinc_FM_nco.set_value(int(value))

	def sb_pinc_FM_nco_changed(self, widget, value):
		vals.pinc_FM_nco=value
		print("/dev/FM_nco", 125000000, value, 40, int(self.sb_poff_FM_nco.get_value()), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/FM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_FM_nco.get_value()), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		self.sd_pinc_FM_nco.set_value(value)

	def sd_poff_FM_nco_changed(self, widget, value):
		vals.poff_FM_nco=value
		print("/dev/FM_nco", 125000000, self.sb_pinc_FM_nco.get_value(), 40, int(value), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/FM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_FM_nco.get_value())), 40, int(value), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		self.sb_poff_FM_nco.set_value(value)

	def sb_poff_FM_nco_changed(self, widget, value):
		vals.poff_FM_nco=value
		print("/dev/FM_nco", 125000000, self.sb_pinc_FM_nco.get_value(), 40, int(value), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/FM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_FM_nco.get_value())), 40, int(value), int(self.cb_pinc_FM_nco.get_value()), int(self.cb_poff_FM_nco.get_value()))
		self.sd_poff_FM_nco.set_value(value)

	def cb_pinc_FM_nco_changed(self, widget, value):
		vals.cb_pinc_FM_nco=value
		print("/dev/FM_nco", 125000000, self.sb_pinc_FM_nco.get_value(), 40, int(self.sb_poff_FM_nco.get_value()), int(value=="true"), int(self.cb_poff_FM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/FM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_FM_nco.get_value())), 40, int(self.sb_poff_FM_nco.get_value()), int(value == "true"), int(self.cb_poff_FM_nco.get_value()))
		self.cb_pinc_FM_nco.set_value(int(value=="true"))

	def cb_poff_FM_nco_changed(self, widget, value):
		vals.cb_poff_FM_nco=value
		print("/dev/FM_nco", 125000000, self.sb_pinc_FM_nco.get_value(), 40, int(self.sb_poff_FM_nco.get_value()), int(self.cb_pinc_FM_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/FM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_FM_nco.get_value())), 40, int(self.sb_poff_FM_nco.get_value()), int(self.cb_pinc_FM_nco.get_value()), int(value=="true"))
		self.cb_poff_FM_nco.set_value(int(value=="true"))

	def sd_pinc_PM_nco_changed(self, widget, value):
		vals.pinc_PM_nco=value
		print("/dev/PM_nco", 125000000, int(value), 40, int(self.sb_poff_PM_nco.get_value()), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/PM_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_PM_nco.get_value()), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		self.sb_pinc_PM_nco.set_value(int(value))

	def sb_pinc_PM_nco_changed(self, widget, value):
		vals.pinc_PM_nco=value
		print("/dev/PM_nco", 125000000, value, 40, int(self.sb_poff_PM_nco.get_value()), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/PM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_PM_nco.get_value()), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		self.sd_pinc_PM_nco.set_value(value)

	def sd_poff_PM_nco_changed(self, widget, value):
		vals.poff_PM_nco=value
		print("/dev/PM_nco", 125000000, self.sb_pinc_PM_nco.get_value(), 40, int(value), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/PM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_PM_nco.get_value())), 40, int(value), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		self.sb_poff_PM_nco.set_value(value)

	def sb_poff_PM_nco_changed(self, widget, value):
		vals.poff_PM_nco=value
		print("/dev/PM_nco", 125000000, self.sb_pinc_PM_nco.get_value(), 40, int(value), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/PM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_PM_nco.get_value())), 40, int(value), int(self.cb_pinc_PM_nco.get_value()), int(self.cb_poff_PM_nco.get_value()))
		self.sd_poff_PM_nco.set_value(value)

	def cb_pinc_PM_nco_changed(self, widget, value):
		vals.cb_pinc_PM_nco=value
		print("/dev/PM_nco", 125000000, self.sb_pinc_PM_nco.get_value(), 40, int(self.sb_poff_PM_nco.get_value()), int(value=="true"), int(self.cb_poff_PM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/PM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_PM_nco.get_value())), 40, int(self.sb_poff_PM_nco.get_value()), int(value == "true"), int(self.cb_poff_PM_nco.get_value()))
		self.cb_pinc_PM_nco.set_value(int(value=="true"))

	def cb_poff_PM_nco_changed(self, widget, value):
		vals.cb_poff_PM_nco=value
		print("/dev/PM_nco", 125000000, self.sb_pinc_PM_nco.get_value(), 40, int(self.sb_poff_PM_nco.get_value()), int(self.cb_pinc_PM_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/PM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_PM_nco.get_value())), 40, int(self.sb_poff_PM_nco.get_value()), int(self.cb_pinc_PM_nco.get_value()), int(value=="true"))
		self.cb_poff_PM_nco.set_value(int(value=="true"))

	def sd_f0_changed(self, widget, value):
		vals.f0=value
		print("/dev/f0", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/f0", int(round(int(value)/(125e6/2**40))))
		self.sb_f0.set_value(int(value))

	def sb_f0_changed(self, widget, value):
		vals.f0=value
		print("/dev/f0", value)
		liboscimp_fpga.add_const_set_offset("/dev/f0", int(round(float(value)/(125e6/2**40))))
		self.sd_f0.set_value(int(float(value)))

	def sd_ch1_mod_ampl_changed(self, widget, value):
		vals.ch1_mod_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_ampl FM", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_mod_ampl.set_value(int(value))

	def sb_ch1_mod_ampl_changed(self, widget, value):
		vals.ch1_mod_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_ampl FM", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_mod_ampl.set_value(int(float(value)))

	def sd_ch2_mod_ampl_changed(self, widget, value):
		vals.ch2_mod_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_ampl PM", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_ampl", liboscimp_fpga.CHANB, int(value))
		self.sb_ch2_mod_ampl.set_value(int(value))

	def sb_ch2_mod_ampl_changed(self, widget, value):
		vals.ch2_mod_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_ampl PM", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_ampl", liboscimp_fpga.CHANB, int(value))
		self.sd_ch2_mod_ampl.set_value(int(float(value)))

	def sd_pinc_nco_changed(self, widget, value):
		vals.pinc_nco=value
		print("/dev/nco", 125000000, int(value), 40, int(self.sb_poff_nco.get_value()), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_nco.get_value()), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		self.sb_pinc_nco.set_value(int(value))

	def sb_pinc_nco_changed(self, widget, value):
		vals.pinc_nco=value
		print("/dev/nco", 125000000, value, 40, int(self.sb_poff_nco.get_value()), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_nco.get_value()), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		self.sd_pinc_nco.set_value(value)

	def sd_poff_nco_changed(self, widget, value):
		vals.poff_nco=value
		print("/dev/nco", 125000000, self.sb_pinc_nco.get_value(), 40, int(value), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_nco.get_value())), 40, int(value), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		self.sb_poff_nco.set_value(value)

	def sb_poff_nco_changed(self, widget, value):
		vals.poff_nco=value
		print("/dev/nco", 125000000, self.sb_pinc_nco.get_value(), 40, int(value), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_nco.get_value())), 40, int(value), int(self.cb_pinc_nco.get_value()), int(self.cb_poff_nco.get_value()))
		self.sd_poff_nco.set_value(value)

	def cb_pinc_nco_changed(self, widget, value):
		vals.cb_pinc_nco=value
		print("/dev/nco", 125000000, self.sb_pinc_nco.get_value(), 40, int(self.sb_poff_nco.get_value()), int(value=="true"), int(self.cb_poff_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_nco.get_value())), 40, int(self.sb_poff_nco.get_value()), int(value == "true"), int(self.cb_poff_nco.get_value()))
		self.cb_pinc_nco.set_value(int(value=="true"))

	def cb_poff_nco_changed(self, widget, value):
		vals.cb_poff_nco=value
		print("/dev/nco", 125000000, self.sb_pinc_nco.get_value(), 40, int(self.sb_poff_nco.get_value()), int(self.cb_pinc_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_nco.get_value())), 40, int(self.sb_poff_nco.get_value()), int(self.cb_pinc_nco.get_value()), int(value=="true"))
		self.cb_poff_nco.set_value(int(value=="true"))

start(MyApp, address="0.0.0.0", port=80, title="phase_frequency_modulation_webserver")
