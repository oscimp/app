#!/usr/bin/env python

import liboscimp_fpga
import ctypes
import os
from lxml import objectify
import lxml.etree
import remi.gui as gui
from remi import start, App

vals = objectify.Element("item")
vals.config = "amplitude_modulation_defconf.xml"
vals.ch1_AM_ampl = 0
vals.AM_depth = 0
vals.pinc_AM_nco = 0
vals.poff_AM_nco = 0
vals.cb_pinc_AM_nco = "true"
vals.cb_poff_AM_nco = "true"

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

		self.hbox_ch1_AM_ampl = gui.HBox(margin="10px")
		self.lb_ch1_AM_ampl = gui.Label("/dev/AM_ampl", width="20%", margin="10px")
		self.sd_ch1_AM_ampl = gui.Slider(vals.ch1_AM_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_AM_ampl.set_oninput_listener(self.sd_ch1_AM_ampl_changed)
		self.sb_ch1_AM_ampl = gui.SpinBox(vals.ch1_AM_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_AM_ampl.set_on_change_listener(self.sb_ch1_AM_ampl_changed)
		self.sd_ch1_AM_ampl_changed(self.sd_ch1_AM_ampl, self.sd_ch1_AM_ampl.get_value())
		self.hbox_ch1_AM_ampl.append(self.lb_ch1_AM_ampl)
		self.hbox_ch1_AM_ampl.append(self.sd_ch1_AM_ampl)
		self.hbox_ch1_AM_ampl.append(self.sb_ch1_AM_ampl)
		self.w.append(self.hbox_ch1_AM_ampl)

		self.hbox_AM_depth = gui.HBox(margin="10px")
		self.lb_AM_depth = gui.Label("/dev/AM_depth", width="20%", margin="10px")
		self.sd_AM_depth = gui.Slider(vals.AM_depth, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_AM_depth.set_oninput_listener(self.sd_AM_depth_changed)
		self.sb_AM_depth = gui.SpinBox(vals.AM_depth, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_AM_depth.set_on_change_listener(self.sb_AM_depth_changed)
		self.sd_AM_depth_changed(self.sd_AM_depth, self.sd_AM_depth.get_value())
		self.hbox_AM_depth.append(self.lb_AM_depth)
		self.hbox_AM_depth.append(self.sd_AM_depth)
		self.hbox_AM_depth.append(self.sb_AM_depth)
		self.w.append(self.hbox_AM_depth)

		self.hbox_AM_nco = gui.HBox(margin="10px")
		self.lb_AM_nco = gui.Label("/dev/AM_nco", width="20%", margin="10px")
		self.sd_pinc_AM_nco = gui.Slider(vals.pinc_AM_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_AM_nco.set_oninput_listener(self.sd_pinc_AM_nco_changed)
		self.sb_pinc_AM_nco = gui.SpinBox(vals.pinc_AM_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_AM_nco.set_on_change_listener(self.sb_pinc_AM_nco_changed)
		self.sd_poff_AM_nco = gui.Slider(vals.poff_AM_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_AM_nco.set_oninput_listener(self.sd_poff_AM_nco_changed)
		self.sb_poff_AM_nco = gui.SpinBox(vals.poff_AM_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_AM_nco.set_on_change_listener(self.sb_poff_AM_nco_changed)
		self.cb_pinc_AM_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_AM_nco, width="5%", margin="10px")
		self.cb_pinc_AM_nco.set_on_change_listener(self.cb_pinc_AM_nco_changed)
		self.cb_poff_AM_nco = gui.CheckBoxLabel("poff", vals.cb_poff_AM_nco, width="5%", margin="10px")
		self.cb_poff_AM_nco.set_on_change_listener(self.cb_poff_AM_nco_changed)
		self.hbox_AM_nco.append(self.lb_AM_nco)
		self.hbox_AM_nco.append(self.sd_pinc_AM_nco)
		self.hbox_AM_nco.append(self.sb_pinc_AM_nco)
		self.hbox_AM_nco.append(self.sd_poff_AM_nco)
		self.hbox_AM_nco.append(self.sb_poff_AM_nco)
		self.hbox_AM_nco.append(self.cb_pinc_AM_nco)
		self.hbox_AM_nco.append(self.cb_poff_AM_nco)
		self.w.append(self.hbox_AM_nco)

		return self.w

	def dtext_conf_file_changed(self, widget, value):
		print(value)
		vals.config=value

	def bt_load_changed(self, widget):
		with open(str(vals.config), "r") as f:
			 lf = objectify.fromstring(f.read())

		self.sd_ch1_AM_ampl_changed(self.sd_ch1_AM_ampl, lf.ch1_AM_ampl)
		self.sb_ch1_AM_ampl_changed(self.sd_ch1_AM_ampl, lf.ch1_AM_ampl)
		self.sd_AM_depth_changed(self.sd_AM_depth, lf.AM_depth)
		self.sb_AM_depth_changed(self.sb_AM_depth, lf.AM_depth)
		self.sd_pinc_AM_nco_changed(self.sd_pinc_AM_nco, lf.pinc_AM_nco)
		self.sb_pinc_AM_nco_changed(self.sb_pinc_AM_nco, lf.pinc_AM_nco)
		self.sd_poff_AM_nco_changed(self.sd_poff_AM_nco, lf.poff_AM_nco)
		self.sb_poff_AM_nco_changed(self.sb_poff_AM_nco, lf.poff_AM_nco)
		self.cb_pinc_AM_nco_changed(self.cb_pinc_AM_nco, lf.cb_pinc_AM_nco)
		self.cb_poff_AM_nco_changed(self.cb_poff_AM_nco, lf.cb_poff_AM_nco)
		print("Configuration loaded")

	def bt_save_changed(self, widget):
		try:
			os.remove(str(vals.config))
		except:
			pass
		with open(str(vals.config), "wb") as f:
			f.write(lxml.etree.tostring(vals, pretty_print=True))
		print("Saved")

	def sd_ch1_AM_ampl_changed(self, widget, value):
		vals.ch1_AM_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/AM_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/AM_ampl", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/AM_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_AM_ampl.set_value(int(value))

	def sb_ch1_AM_ampl_changed(self, widget, value):
		vals.ch1_AM_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/AM_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/AM_ampl", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/AM_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_AM_ampl.set_value(int(float(value)))

	def sd_AM_depth_changed(self, widget, value):
		vals.AM_depth=value
		print("/dev/AM_depth", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/AM_depth", int(value))
		self.sb_AM_depth.set_value(int(value))

	def sb_AM_depth_changed(self, widget, value):
		vals.AM_depth=value
		print("/dev/AM_depth", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/AM_depth", int(value))
		self.sd_AM_depth.set_value(int(float(value)))

	def sd_pinc_AM_nco_changed(self, widget, value):
		vals.pinc_AM_nco=value
		print("/dev/AM_nco", 125000000, int(value), 40, int(self.sb_poff_AM_nco.get_value()), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/AM_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_AM_nco.get_value()), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		self.sb_pinc_AM_nco.set_value(int(value))

	def sb_pinc_AM_nco_changed(self, widget, value):
		vals.pinc_AM_nco=value
		print("/dev/AM_nco", 125000000, value, 40, int(self.sb_poff_AM_nco.get_value()), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/AM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_AM_nco.get_value()), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		self.sd_pinc_AM_nco.set_value(value)

	def sd_poff_AM_nco_changed(self, widget, value):
		vals.poff_AM_nco=value
		print("/dev/AM_nco", 125000000, self.sb_pinc_AM_nco.get_value(), 40, int(value), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/AM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_AM_nco.get_value())), 40, int(value), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		self.sb_poff_AM_nco.set_value(value)

	def sb_poff_AM_nco_changed(self, widget, value):
		vals.poff_AM_nco=value
		print("/dev/AM_nco", 125000000, self.sb_pinc_AM_nco.get_value(), 40, int(value), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/AM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_AM_nco.get_value())), 40, int(value), int(self.cb_pinc_AM_nco.get_value()), int(self.cb_poff_AM_nco.get_value()))
		self.sd_poff_AM_nco.set_value(value)

	def cb_pinc_AM_nco_changed(self, widget, value):
		vals.cb_pinc_AM_nco=value
		print("/dev/AM_nco", 125000000, self.sb_pinc_AM_nco.get_value(), 40, int(self.sb_poff_AM_nco.get_value()), int(value=="true"), int(self.cb_poff_AM_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/AM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_AM_nco.get_value())), 40, int(self.sb_poff_AM_nco.get_value()), int(value == "true"), int(self.cb_poff_AM_nco.get_value()))
		self.cb_pinc_AM_nco.set_value(int(value=="true"))

	def cb_poff_AM_nco_changed(self, widget, value):
		vals.cb_poff_AM_nco=value
		print("/dev/AM_nco", 125000000, self.sb_pinc_AM_nco.get_value(), 40, int(self.sb_poff_AM_nco.get_value()), int(self.cb_pinc_AM_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/AM_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_AM_nco.get_value())), 40, int(self.sb_poff_AM_nco.get_value()), int(self.cb_pinc_AM_nco.get_value()), int(value=="true"))
		self.cb_poff_AM_nco.set_value(int(value=="true"))

start(MyApp, address="0.0.0.0", port=80, title="amplitude_modulation_webserver")
