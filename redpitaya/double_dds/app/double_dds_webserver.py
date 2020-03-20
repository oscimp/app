#!/usr/bin/env python

import liboscimp_fpga
import ctypes
import os
from lxml import objectify
import lxml.etree
import remi.gui as gui
from remi import start, App

vals = objectify.Element("item")
vals.config = "double_dds_defconf.xml"
vals.pinc_dds1_nco = 0
vals.poff_dds1_nco = 0
vals.cb_pinc_dds1_nco = "true"
vals.cb_poff_dds1_nco = "true"
vals.dds1_offset = 0
vals.pinc_dds2_nco = 0
vals.poff_dds2_nco = 0
vals.cb_pinc_dds2_nco = "true"
vals.cb_poff_dds2_nco = "true"
vals.dds2_offset = 0
vals.ch1_dds_ampl = 0
vals.ch2_dds_ampl = 0

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

		self.hbox_dds1_nco = gui.HBox(margin="10px")
		self.lb_dds1_nco = gui.Label("/dev/dds1_nco", width="20%", margin="10px")
		self.sd_pinc_dds1_nco = gui.Slider(vals.pinc_dds1_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_dds1_nco.set_oninput_listener(self.sd_pinc_dds1_nco_changed)
		self.sb_pinc_dds1_nco = gui.SpinBox(vals.pinc_dds1_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_dds1_nco.set_on_change_listener(self.sb_pinc_dds1_nco_changed)
		self.sd_poff_dds1_nco = gui.Slider(vals.poff_dds1_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_dds1_nco.set_oninput_listener(self.sd_poff_dds1_nco_changed)
		self.sb_poff_dds1_nco = gui.SpinBox(vals.poff_dds1_nco, -8192, 8191, 1, width="10%", margin="10px")
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

		self.hbox_dds1_offset = gui.HBox(margin="10px")
		self.lb_dds1_offset = gui.Label("/dev/dds1_offset", width="20%", margin="10px")
		self.sd_dds1_offset = gui.Slider(vals.dds1_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_dds1_offset.set_oninput_listener(self.sd_dds1_offset_changed)
		self.sb_dds1_offset = gui.SpinBox(vals.dds1_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_dds1_offset.set_on_change_listener(self.sb_dds1_offset_changed)
		self.sd_dds1_offset_changed(self.sd_dds1_offset, self.sd_dds1_offset.get_value())
		self.hbox_dds1_offset.append(self.lb_dds1_offset)
		self.hbox_dds1_offset.append(self.sd_dds1_offset)
		self.hbox_dds1_offset.append(self.sb_dds1_offset)
		self.w.append(self.hbox_dds1_offset)

		self.hbox_dds2_nco = gui.HBox(margin="10px")
		self.lb_dds2_nco = gui.Label("/dev/dds2_nco", width="20%", margin="10px")
		self.sd_pinc_dds2_nco = gui.Slider(vals.pinc_dds2_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_dds2_nco.set_oninput_listener(self.sd_pinc_dds2_nco_changed)
		self.sb_pinc_dds2_nco = gui.SpinBox(vals.pinc_dds2_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_dds2_nco.set_on_change_listener(self.sb_pinc_dds2_nco_changed)
		self.sd_poff_dds2_nco = gui.Slider(vals.poff_dds2_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_dds2_nco.set_oninput_listener(self.sd_poff_dds2_nco_changed)
		self.sb_poff_dds2_nco = gui.SpinBox(vals.poff_dds2_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_dds2_nco.set_on_change_listener(self.sb_poff_dds2_nco_changed)
		self.cb_pinc_dds2_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_dds2_nco, width="5%", margin="10px")
		self.cb_pinc_dds2_nco.set_on_change_listener(self.cb_pinc_dds2_nco_changed)
		self.cb_poff_dds2_nco = gui.CheckBoxLabel("poff", vals.cb_poff_dds2_nco, width="5%", margin="10px")
		self.cb_poff_dds2_nco.set_on_change_listener(self.cb_poff_dds2_nco_changed)
		self.hbox_dds2_nco.append(self.lb_dds2_nco)
		self.hbox_dds2_nco.append(self.sd_pinc_dds2_nco)
		self.hbox_dds2_nco.append(self.sb_pinc_dds2_nco)
		self.hbox_dds2_nco.append(self.sd_poff_dds2_nco)
		self.hbox_dds2_nco.append(self.sb_poff_dds2_nco)
		self.hbox_dds2_nco.append(self.cb_pinc_dds2_nco)
		self.hbox_dds2_nco.append(self.cb_poff_dds2_nco)
		self.w.append(self.hbox_dds2_nco)

		self.hbox_dds2_offset = gui.HBox(margin="10px")
		self.lb_dds2_offset = gui.Label("/dev/dds2_offset", width="20%", margin="10px")
		self.sd_dds2_offset = gui.Slider(vals.dds2_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_dds2_offset.set_oninput_listener(self.sd_dds2_offset_changed)
		self.sb_dds2_offset = gui.SpinBox(vals.dds2_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_dds2_offset.set_on_change_listener(self.sb_dds2_offset_changed)
		self.sd_dds2_offset_changed(self.sd_dds2_offset, self.sd_dds2_offset.get_value())
		self.hbox_dds2_offset.append(self.lb_dds2_offset)
		self.hbox_dds2_offset.append(self.sd_dds2_offset)
		self.hbox_dds2_offset.append(self.sb_dds2_offset)
		self.w.append(self.hbox_dds2_offset)

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

		self.hbox_ch2_dds_ampl = gui.HBox(margin="10px")
		self.lb_ch2_dds_ampl = gui.Label("/dev/dds_ampl/2", width="20%", margin="10px")
		self.sd_ch2_dds_ampl = gui.Slider(vals.ch2_dds_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch2_dds_ampl.set_oninput_listener(self.sd_ch2_dds_ampl_changed)
		self.sb_ch2_dds_ampl = gui.SpinBox(vals.ch2_dds_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch2_dds_ampl.set_on_change_listener(self.sb_ch2_dds_ampl_changed)
		self.sd_ch2_dds_ampl_changed(self.sd_ch2_dds_ampl, self.sd_ch2_dds_ampl.get_value())
		self.hbox_ch2_dds_ampl.append(self.lb_ch2_dds_ampl)
		self.hbox_ch2_dds_ampl.append(self.sd_ch2_dds_ampl)
		self.hbox_ch2_dds_ampl.append(self.sb_ch2_dds_ampl)
		self.w.append(self.hbox_ch2_dds_ampl)

		return self.w

	def dtext_conf_file_changed(self, widget, value):
		print(value)
		vals.config=value

	def bt_load_changed(self, widget):
		with open(str(vals.config), "r") as f:
			 lf = objectify.fromstring(f.read())

		self.sd_pinc_dds1_nco_changed(self.sd_pinc_dds1_nco, lf.pinc_dds1_nco)
		self.sb_pinc_dds1_nco_changed(self.sb_pinc_dds1_nco, lf.pinc_dds1_nco)
		self.sd_poff_dds1_nco_changed(self.sd_poff_dds1_nco, lf.poff_dds1_nco)
		self.sb_poff_dds1_nco_changed(self.sb_poff_dds1_nco, lf.poff_dds1_nco)
		self.cb_pinc_dds1_nco_changed(self.cb_pinc_dds1_nco, lf.cb_pinc_dds1_nco)
		self.cb_poff_dds1_nco_changed(self.cb_poff_dds1_nco, lf.cb_poff_dds1_nco)
		self.sd_dds1_offset_changed(self.sd_dds1_offset, lf.dds1_offset)
		self.sb_dds1_offset_changed(self.sb_dds1_offset, lf.dds1_offset)
		self.sd_pinc_dds2_nco_changed(self.sd_pinc_dds2_nco, lf.pinc_dds2_nco)
		self.sb_pinc_dds2_nco_changed(self.sb_pinc_dds2_nco, lf.pinc_dds2_nco)
		self.sd_poff_dds2_nco_changed(self.sd_poff_dds2_nco, lf.poff_dds2_nco)
		self.sb_poff_dds2_nco_changed(self.sb_poff_dds2_nco, lf.poff_dds2_nco)
		self.cb_pinc_dds2_nco_changed(self.cb_pinc_dds2_nco, lf.cb_pinc_dds2_nco)
		self.cb_poff_dds2_nco_changed(self.cb_poff_dds2_nco, lf.cb_poff_dds2_nco)
		self.sd_dds2_offset_changed(self.sd_dds2_offset, lf.dds2_offset)
		self.sb_dds2_offset_changed(self.sb_dds2_offset, lf.dds2_offset)
		self.sd_ch1_dds_ampl_changed(self.sd_ch1_dds_ampl, lf.ch1_dds_ampl)
		self.sb_ch1_dds_ampl_changed(self.sd_ch1_dds_ampl, lf.ch1_dds_ampl)
		self.sd_ch2_dds_ampl_changed(self.sb_ch2_dds_ampl, lf.ch2_dds_ampl)
		self.sb_ch2_dds_ampl_changed(self.sb_ch2_dds_ampl, lf.ch2_dds_ampl)
		print("Configuration loaded")

	def bt_save_changed(self, widget):
		try:
			os.remove(str(vals.config))
		except:
			pass
		with open(str(vals.config), "wb") as f:
			f.write(lxml.etree.tostring(vals, pretty_print=True))
		print("Saved")

	def sd_pinc_dds1_nco_changed(self, widget, value):
		vals.pinc_dds1_nco=value
		print("/dev/dds1_nco", 125000000, int(value), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		self.sb_pinc_dds1_nco.set_value(int(value))

	def sb_pinc_dds1_nco_changed(self, widget, value):
		vals.pinc_dds1_nco=value
		print("/dev/dds1_nco", 125000000, value, 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		self.sd_pinc_dds1_nco.set_value(value)

	def sd_poff_dds1_nco_changed(self, widget, value):
		vals.poff_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		self.sb_poff_dds1_nco.set_value(value)

	def sb_poff_dds1_nco_changed(self, widget, value):
		vals.poff_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(value), int(self.cb_pinc_dds1_nco.get_value()), int(self.cb_poff_dds1_nco.get_value()))
		self.sd_poff_dds1_nco.set_value(value)

	def cb_pinc_dds1_nco_changed(self, widget, value):
		vals.cb_pinc_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(self.sb_poff_dds1_nco.get_value()), int(value=="true"), int(self.cb_poff_dds1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(self.sb_poff_dds1_nco.get_value()), int(value == "true"), int(self.cb_poff_dds1_nco.get_value()))
		self.cb_pinc_dds1_nco.set_value(int(value=="true"))

	def cb_poff_dds1_nco_changed(self, widget, value):
		vals.cb_poff_dds1_nco=value
		print("/dev/dds1_nco", 125000000, self.sb_pinc_dds1_nco.get_value(), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds1_nco.get_value())), 40, int(self.sb_poff_dds1_nco.get_value()), int(self.cb_pinc_dds1_nco.get_value()), int(value=="true"))
		self.cb_poff_dds1_nco.set_value(int(value=="true"))

	def sd_dds1_offset_changed(self, widget, value):
		vals.dds1_offset=value
		print("/dev/dds1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dds1_offset", int(value))
		self.sb_dds1_offset.set_value(int(value))

	def sb_dds1_offset_changed(self, widget, value):
		vals.dds1_offset=value
		print("/dev/dds1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dds1_offset", int(value))
		self.sd_dds1_offset.set_value(int(float(value)))

	def sd_pinc_dds2_nco_changed(self, widget, value):
		vals.pinc_dds2_nco=value
		print("/dev/dds2_nco", 125000000, int(value), 40, int(self.sb_poff_dds2_nco.get_value()), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds2_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_dds2_nco.get_value()), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		self.sb_pinc_dds2_nco.set_value(int(value))

	def sb_pinc_dds2_nco_changed(self, widget, value):
		vals.pinc_dds2_nco=value
		print("/dev/dds2_nco", 125000000, value, 40, int(self.sb_poff_dds2_nco.get_value()), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_dds2_nco.get_value()), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		self.sd_pinc_dds2_nco.set_value(value)

	def sd_poff_dds2_nco_changed(self, widget, value):
		vals.poff_dds2_nco=value
		print("/dev/dds2_nco", 125000000, self.sb_pinc_dds2_nco.get_value(), 40, int(value), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds2_nco.get_value())), 40, int(value), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		self.sb_poff_dds2_nco.set_value(value)

	def sb_poff_dds2_nco_changed(self, widget, value):
		vals.poff_dds2_nco=value
		print("/dev/dds2_nco", 125000000, self.sb_pinc_dds2_nco.get_value(), 40, int(value), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds2_nco.get_value())), 40, int(value), int(self.cb_pinc_dds2_nco.get_value()), int(self.cb_poff_dds2_nco.get_value()))
		self.sd_poff_dds2_nco.set_value(value)

	def cb_pinc_dds2_nco_changed(self, widget, value):
		vals.cb_pinc_dds2_nco=value
		print("/dev/dds2_nco", 125000000, self.sb_pinc_dds2_nco.get_value(), 40, int(self.sb_poff_dds2_nco.get_value()), int(value=="true"), int(self.cb_poff_dds2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds2_nco.get_value())), 40, int(self.sb_poff_dds2_nco.get_value()), int(value == "true"), int(self.cb_poff_dds2_nco.get_value()))
		self.cb_pinc_dds2_nco.set_value(int(value=="true"))

	def cb_poff_dds2_nco_changed(self, widget, value):
		vals.cb_poff_dds2_nco=value
		print("/dev/dds2_nco", 125000000, self.sb_pinc_dds2_nco.get_value(), 40, int(self.sb_poff_dds2_nco.get_value()), int(self.cb_pinc_dds2_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/dds2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_dds2_nco.get_value())), 40, int(self.sb_poff_dds2_nco.get_value()), int(self.cb_pinc_dds2_nco.get_value()), int(value=="true"))
		self.cb_poff_dds2_nco.set_value(int(value=="true"))

	def sd_dds2_offset_changed(self, widget, value):
		vals.dds2_offset=value
		print("/dev/dds2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dds2_offset", int(value))
		self.sb_dds2_offset.set_value(int(value))

	def sb_dds2_offset_changed(self, widget, value):
		vals.dds2_offset=value
		print("/dev/dds2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dds2_offset", int(value))
		self.sd_dds2_offset.set_value(int(float(value)))

	def sd_ch1_dds_ampl_changed(self, widget, value):
		vals.ch1_dds_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_dds_ampl.set_value(int(value))

	def sb_ch1_dds_ampl_changed(self, widget, value):
		vals.ch1_dds_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_dds_ampl.set_value(int(float(value)))

	def sd_ch2_dds_ampl_changed(self, widget, value):
		vals.ch2_dds_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_ampl ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANB, int(value))
		self.sb_ch2_dds_ampl.set_value(int(value))

	def sb_ch2_dds_ampl_changed(self, widget, value):
		vals.ch2_dds_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/dds_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/dds_ampl ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/dds_ampl", liboscimp_fpga.CHANB, int(value))
		self.sd_ch2_dds_ampl.set_value(int(float(value)))

start(MyApp, address="0.0.0.0", port=80, title="double_dds_webserver")
