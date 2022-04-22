#!/usr/bin/env python

import liboscimp_fpga
import ctypes
import os
import time
from lxml import objectify
import lxml.etree
import remi.gui as gui
from remi import start, App

#Sampling frequency
samp_freq = 125000000

vals = objectify.Element("item")
vals.config = "comb_lock_defconf.xml"
vals.frequency_offset = 0
vals.ch1_matrix_mxi = 0
vals.ch2_matrix_mxi = 0
vals.ch1_matrix_myq = 0
vals.ch2_matrix_myq = 0
vals.kp_pidv3_axi_0 = 0
vals.ki_pidv3_axi_0 = 0
vals.rst_int_pidv3_axi_0 = True
vals.sp_pidv3_axi_0 = 0
vals.sign_pidv3_axi_0 = 0
vals.kp_pidv3_axi_1 = 0
vals.ki_pidv3_axi_1 = 0
vals.rst_int_pidv3_axi_1 = True
vals.sp_pidv3_axi_1 = 0
vals.sign_pidv3_axi_1 = 0
vals.shifterReal_dyn_0 = 9
vals.switchReal_0 = True
vals.switchReal_1 = True
vals.switchReal_2 = True

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

		self.hbox_frequency_offset = gui.HBox(margin="10px")
		self.lb_frequency_offset = gui.Label("/dev/frequency_offset", width="20%", margin="10px")
		self.sd_frequency_offset = gui.Slider(vals.frequency_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_frequency_offset.set_on_change_listener(self.sd_frequency_offset_changed)
		self.sb_frequency_offset = gui.SpinBox(vals.frequency_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_frequency_offset.set_on_change_listener(self.sb_frequency_offset_changed)
		self.sd_frequency_offset_changed(self.sd_frequency_offset, self.sd_frequency_offset.get_value())
		self.hbox_frequency_offset.append(self.lb_frequency_offset)
		self.hbox_frequency_offset.append(self.sd_frequency_offset)
		self.hbox_frequency_offset.append(self.sb_frequency_offset)
		self.w.append(self.hbox_frequency_offset)

		self.hbox_ch1_matrix_mxi = gui.HBox(margin="10px")
		self.lb_ch1_matrix_mxi = gui.Label("/dev/matrix_mxi/1", width="20%", margin="10px")
		self.sd_ch1_matrix_mxi = gui.Slider(vals.ch1_matrix_mxi, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_matrix_mxi.set_on_change_listener(self.sd_ch1_matrix_mxi_changed)
		self.sb_ch1_matrix_mxi = gui.SpinBox(vals.ch1_matrix_mxi, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_matrix_mxi.set_on_change_listener(self.sb_ch1_matrix_mxi_changed)
		self.sd_ch1_matrix_mxi_changed(self.sd_ch1_matrix_mxi, self.sd_ch1_matrix_mxi.get_value())
		self.hbox_ch1_matrix_mxi.append(self.lb_ch1_matrix_mxi)
		self.hbox_ch1_matrix_mxi.append(self.sd_ch1_matrix_mxi)
		self.hbox_ch1_matrix_mxi.append(self.sb_ch1_matrix_mxi)
		self.w.append(self.hbox_ch1_matrix_mxi)

		self.hbox_ch2_matrix_mxi = gui.HBox(margin="10px")
		self.lb_ch2_matrix_mxi = gui.Label("/dev/matrix_mxi/2", width="20%", margin="10px")
		self.sd_ch2_matrix_mxi = gui.Slider(vals.ch2_matrix_mxi, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch2_matrix_mxi.set_on_change_listener(self.sd_ch2_matrix_mxi_changed)
		self.sb_ch2_matrix_mxi = gui.SpinBox(vals.ch2_matrix_mxi, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch2_matrix_mxi.set_on_change_listener(self.sb_ch2_matrix_mxi_changed)
		self.sd_ch2_matrix_mxi_changed(self.sd_ch2_matrix_mxi, self.sd_ch2_matrix_mxi.get_value())
		self.hbox_ch2_matrix_mxi.append(self.lb_ch2_matrix_mxi)
		self.hbox_ch2_matrix_mxi.append(self.sd_ch2_matrix_mxi)
		self.hbox_ch2_matrix_mxi.append(self.sb_ch2_matrix_mxi)
		self.w.append(self.hbox_ch2_matrix_mxi)

		self.hbox_ch1_matrix_myq = gui.HBox(margin="10px")
		self.lb_ch1_matrix_myq = gui.Label("/dev/matrix_myq/1", width="20%", margin="10px")
		self.sd_ch1_matrix_myq = gui.Slider(vals.ch1_matrix_myq, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_matrix_myq.set_on_change_listener(self.sd_ch1_matrix_myq_changed)
		self.sb_ch1_matrix_myq = gui.SpinBox(vals.ch1_matrix_myq, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_matrix_myq.set_on_change_listener(self.sb_ch1_matrix_myq_changed)
		self.sd_ch1_matrix_myq_changed(self.sd_ch1_matrix_myq, self.sd_ch1_matrix_myq.get_value())
		self.hbox_ch1_matrix_myq.append(self.lb_ch1_matrix_myq)
		self.hbox_ch1_matrix_myq.append(self.sd_ch1_matrix_myq)
		self.hbox_ch1_matrix_myq.append(self.sb_ch1_matrix_myq)
		self.w.append(self.hbox_ch1_matrix_myq)

		self.hbox_ch2_matrix_myq = gui.HBox(margin="10px")
		self.lb_ch2_matrix_myq = gui.Label("/dev/matrix_myq/2", width="20%", margin="10px")
		self.sd_ch2_matrix_myq = gui.Slider(vals.ch2_matrix_myq, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch2_matrix_myq.set_on_change_listener(self.sd_ch2_matrix_myq_changed)
		self.sb_ch2_matrix_myq = gui.SpinBox(vals.ch2_matrix_myq, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch2_matrix_myq.set_on_change_listener(self.sb_ch2_matrix_myq_changed)
		self.sd_ch2_matrix_myq_changed(self.sd_ch2_matrix_myq, self.sd_ch2_matrix_myq.get_value())
		self.hbox_ch2_matrix_myq.append(self.lb_ch2_matrix_myq)
		self.hbox_ch2_matrix_myq.append(self.sd_ch2_matrix_myq)
		self.hbox_ch2_matrix_myq.append(self.sb_ch2_matrix_myq)
		self.w.append(self.hbox_ch2_matrix_myq)

		self.hbox_kp_pidv3_axi_0 = gui.HBox(margin="10px")
		self.lb_kp_pidv3_axi_0 = gui.Label("/dev/pidv3_axi_0/kp", width="20%", margin="10px")
		self.sd_kp_pidv3_axi_0 = gui.Slider(vals.kp_pidv3_axi_0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_kp_pidv3_axi_0.set_on_change_listener(self.sd_kp_pidv3_axi_0_changed)
		self.sb_kp_pidv3_axi_0 = gui.SpinBox(vals.kp_pidv3_axi_0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_kp_pidv3_axi_0.set_on_change_listener(self.sb_kp_pidv3_axi_0_changed)
		self.sd_kp_pidv3_axi_0_changed(self.sd_kp_pidv3_axi_0, self.sd_kp_pidv3_axi_0.get_value())
		self.hbox_kp_pidv3_axi_0.append(self.lb_kp_pidv3_axi_0)
		self.hbox_kp_pidv3_axi_0.append(self.sd_kp_pidv3_axi_0)
		self.hbox_kp_pidv3_axi_0.append(self.sb_kp_pidv3_axi_0)
		self.w.append(self.hbox_kp_pidv3_axi_0)

		self.hbox_ki_pidv3_axi_0 = gui.HBox(margin="10px")
		self.lb_ki_pidv3_axi_0 = gui.Label("/dev/pidv3_axi_0/ki", width="20%", margin="10px")
		self.sd_ki_pidv3_axi_0 = gui.Slider(vals.ki_pidv3_axi_0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pidv3_axi_0.set_on_change_listener(self.sd_ki_pidv3_axi_0_changed)
		self.sb_ki_pidv3_axi_0 = gui.SpinBox(vals.ki_pidv3_axi_0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ki_pidv3_axi_0.set_on_change_listener(self.sb_ki_pidv3_axi_0_changed)
		self.sd_ki_pidv3_axi_0_changed(self.sd_ki_pidv3_axi_0, self.sd_ki_pidv3_axi_0.get_value())
		self.cb_rst_int_pidv3_axi_0 = gui.CheckBoxLabel("rst_int", vals.rst_int_pidv3_axi_0, width="5%", margin="10px")
		self.cb_rst_int_pidv3_axi_0.set_on_change_listener(self.cb_rst_int_pidv3_axi_0_changed)
		self.hbox_ki_pidv3_axi_0.append(self.lb_ki_pidv3_axi_0)
		self.hbox_ki_pidv3_axi_0.append(self.sd_ki_pidv3_axi_0)
		self.hbox_ki_pidv3_axi_0.append(self.sb_ki_pidv3_axi_0)
		self.hbox_ki_pidv3_axi_0.append(self.cb_rst_int_pidv3_axi_0)
		self.w.append(self.hbox_ki_pidv3_axi_0)

		self.hbox_sp_pidv3_axi_0 = gui.HBox(margin="10px")
		self.lb_sp_pidv3_axi_0 = gui.Label("/dev/pidv3_axi_0/setpoint", width="20%", margin="10px")
		self.sd_sp_pidv3_axi_0 = gui.Slider(vals.sp_pidv3_axi_0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sp_pidv3_axi_0.set_on_change_listener(self.sd_sp_pidv3_axi_0_changed)
		self.sb_sp_pidv3_axi_0 = gui.SpinBox(vals.sp_pidv3_axi_0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sp_pidv3_axi_0.set_on_change_listener(self.sb_sp_pidv3_axi_0_changed)
		self.sd_sp_pidv3_axi_0_changed(self.sd_sp_pidv3_axi_0, self.sd_sp_pidv3_axi_0.get_value())
		self.hbox_sp_pidv3_axi_0.append(self.lb_sp_pidv3_axi_0)
		self.hbox_sp_pidv3_axi_0.append(self.sd_sp_pidv3_axi_0)
		self.hbox_sp_pidv3_axi_0.append(self.sb_sp_pidv3_axi_0)
		self.w.append(self.hbox_sp_pidv3_axi_0)

		self.hbox_sign_pidv3_axi_0 = gui.HBox(margin="10px")
		self.lb_sign_pidv3_axi_0 = gui.Label("/dev/pidv3_axi_0/sign", width="20%", margin="10px")
		self.sd_sign_pidv3_axi_0 = gui.Slider(vals.sign_pidv3_axi_0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sign_pidv3_axi_0.set_on_change_listener(self.sd_sign_pidv3_axi_0_changed)
		self.sb_sign_pidv3_axi_0 = gui.SpinBox(vals.sign_pidv3_axi_0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sign_pidv3_axi_0.set_on_change_listener(self.sb_sign_pidv3_axi_0_changed)
		self.sd_sign_pidv3_axi_0_changed(self.sd_sign_pidv3_axi_0, self.sd_sign_pidv3_axi_0.get_value())
		self.hbox_pidv3_axi_0 = gui.HBox(margin="10px")
		self.hbox_sign_pidv3_axi_0.append(self.lb_sign_pidv3_axi_0)
		self.hbox_sign_pidv3_axi_0.append(self.sd_sign_pidv3_axi_0)
		self.hbox_sign_pidv3_axi_0.append(self.sb_sign_pidv3_axi_0)
		self.w.append(self.hbox_sign_pidv3_axi_0)

		self.hbox_kp_pidv3_axi_1 = gui.HBox(margin="10px")
		self.lb_kp_pidv3_axi_1 = gui.Label("/dev/pidv3_axi_1/kp", width="20%", margin="10px")
		self.sd_kp_pidv3_axi_1 = gui.Slider(vals.kp_pidv3_axi_1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_kp_pidv3_axi_1.set_on_change_listener(self.sd_kp_pidv3_axi_1_changed)
		self.sb_kp_pidv3_axi_1 = gui.SpinBox(vals.kp_pidv3_axi_1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_kp_pidv3_axi_1.set_on_change_listener(self.sb_kp_pidv3_axi_1_changed)
		self.sd_kp_pidv3_axi_1_changed(self.sd_kp_pidv3_axi_1, self.sd_kp_pidv3_axi_1.get_value())
		self.hbox_kp_pidv3_axi_1.append(self.lb_kp_pidv3_axi_1)
		self.hbox_kp_pidv3_axi_1.append(self.sd_kp_pidv3_axi_1)
		self.hbox_kp_pidv3_axi_1.append(self.sb_kp_pidv3_axi_1)
		self.w.append(self.hbox_kp_pidv3_axi_1)

		self.hbox_ki_pidv3_axi_1 = gui.HBox(margin="10px")
		self.lb_ki_pidv3_axi_1 = gui.Label("/dev/pidv3_axi_1/ki", width="20%", margin="10px")
		self.sd_ki_pidv3_axi_1 = gui.Slider(vals.ki_pidv3_axi_1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pidv3_axi_1.set_on_change_listener(self.sd_ki_pidv3_axi_1_changed)
		self.sb_ki_pidv3_axi_1 = gui.SpinBox(vals.ki_pidv3_axi_1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ki_pidv3_axi_1.set_on_change_listener(self.sb_ki_pidv3_axi_1_changed)
		self.sd_ki_pidv3_axi_1_changed(self.sd_ki_pidv3_axi_1, self.sd_ki_pidv3_axi_1.get_value())
		self.cb_rst_int_pidv3_axi_1 = gui.CheckBoxLabel("rst_int", vals.rst_int_pidv3_axi_1, width="5%", margin="10px")
		self.cb_rst_int_pidv3_axi_1.set_on_change_listener(self.cb_rst_int_pidv3_axi_1_changed)
		self.hbox_ki_pidv3_axi_1.append(self.lb_ki_pidv3_axi_1)
		self.hbox_ki_pidv3_axi_1.append(self.sd_ki_pidv3_axi_1)
		self.hbox_ki_pidv3_axi_1.append(self.sb_ki_pidv3_axi_1)
		self.hbox_ki_pidv3_axi_1.append(self.cb_rst_int_pidv3_axi_1)
		self.w.append(self.hbox_ki_pidv3_axi_1)

		self.hbox_sp_pidv3_axi_1 = gui.HBox(margin="10px")
		self.lb_sp_pidv3_axi_1 = gui.Label("/dev/pidv3_axi_1/setpoint", width="20%", margin="10px")
		self.sd_sp_pidv3_axi_1 = gui.Slider(vals.sp_pidv3_axi_1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sp_pidv3_axi_1.set_on_change_listener(self.sd_sp_pidv3_axi_1_changed)
		self.sb_sp_pidv3_axi_1 = gui.SpinBox(vals.sp_pidv3_axi_1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sp_pidv3_axi_1.set_on_change_listener(self.sb_sp_pidv3_axi_1_changed)
		self.sd_sp_pidv3_axi_1_changed(self.sd_sp_pidv3_axi_1, self.sd_sp_pidv3_axi_1.get_value())
		self.hbox_sp_pidv3_axi_1.append(self.lb_sp_pidv3_axi_1)
		self.hbox_sp_pidv3_axi_1.append(self.sd_sp_pidv3_axi_1)
		self.hbox_sp_pidv3_axi_1.append(self.sb_sp_pidv3_axi_1)
		self.w.append(self.hbox_sp_pidv3_axi_1)

		self.hbox_sign_pidv3_axi_1 = gui.HBox(margin="10px")
		self.lb_sign_pidv3_axi_1 = gui.Label("/dev/pidv3_axi_1/sign", width="20%", margin="10px")
		self.sd_sign_pidv3_axi_1 = gui.Slider(vals.sign_pidv3_axi_1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sign_pidv3_axi_1.set_on_change_listener(self.sd_sign_pidv3_axi_1_changed)
		self.sb_sign_pidv3_axi_1 = gui.SpinBox(vals.sign_pidv3_axi_1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sign_pidv3_axi_1.set_on_change_listener(self.sb_sign_pidv3_axi_1_changed)
		self.sd_sign_pidv3_axi_1_changed(self.sd_sign_pidv3_axi_1, self.sd_sign_pidv3_axi_1.get_value())
		self.hbox_pidv3_axi_1 = gui.HBox(margin="10px")
		self.hbox_sign_pidv3_axi_1.append(self.lb_sign_pidv3_axi_1)
		self.hbox_sign_pidv3_axi_1.append(self.sd_sign_pidv3_axi_1)
		self.hbox_sign_pidv3_axi_1.append(self.sb_sign_pidv3_axi_1)
		self.w.append(self.hbox_sign_pidv3_axi_1)

		self.hbox_shifterReal_dyn_0 = gui.HBox(margin="10px")
		self.lb_shifterReal_dyn_0 = gui.Label("/dev/shifterReal_dyn_0", width="20%", margin="10px")
		self.sd_shifterReal_dyn_0 = gui.Slider(vals.shifterReal_dyn_0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_shifterReal_dyn_0.set_on_change_listener(self.sd_shifterReal_dyn_0_changed)
		self.sb_shifterReal_dyn_0 = gui.SpinBox(vals.shifterReal_dyn_0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_shifterReal_dyn_0.set_on_change_listener(self.sb_shifterReal_dyn_0_changed)
		self.sd_shifterReal_dyn_0_changed(self.sd_shifterReal_dyn_0, self.sd_shifterReal_dyn_0.get_value())
		self.hbox_shifterReal_dyn_0.append(self.lb_shifterReal_dyn_0)
		self.hbox_shifterReal_dyn_0.append(self.sd_shifterReal_dyn_0)
		self.hbox_shifterReal_dyn_0.append(self.sb_shifterReal_dyn_0)
		self.w.append(self.hbox_shifterReal_dyn_0)

		self.hbox_switchReal_0 = gui.HBox(margin="10px")
		self.cb_switchReal_0 = gui.CheckBoxLabel("switchReal_0", vals.switchReal_0, width="5%", margin="10px")
		self.cb_switchReal_0.set_on_change_listener(self.cb_switchReal_0_changed)
		self.hbox_switchReal_0.append(self.cb_switchReal_0)
		self.w.append(self.hbox_switchReal_0)

		self.hbox_switchReal_1 = gui.HBox(margin="10px")
		self.cb_switchReal_1 = gui.CheckBoxLabel("switchReal_1", vals.switchReal_1, width="5%", margin="10px")
		self.cb_switchReal_1.set_on_change_listener(self.cb_switchReal_1_changed)
		self.hbox_switchReal_1.append(self.cb_switchReal_1)
		self.w.append(self.hbox_switchReal_1)

		self.hbox_switchReal_2 = gui.HBox(margin="10px")
		self.cb_switchReal_2 = gui.CheckBoxLabel("switchReal_2", vals.switchReal_2, width="5%", margin="10px")
		self.cb_switchReal_2.set_on_change_listener(self.cb_switchReal_2_changed)
		self.hbox_switchReal_2.append(self.cb_switchReal_2)
		self.w.append(self.hbox_switchReal_2)

		return self.w

	def dtext_conf_file_changed(self, widget, value):
		print(value)
		vals.config=value

	def bt_load_changed(self, widget):
		with open(str(vals.config), "r") as f:
			 lf = objectify.fromstring(f.read())

		self.sd_frequency_offset_changed(self.sd_frequency_offset, lf.frequency_offset)
		self.sb_frequency_offset_changed(self.sb_frequency_offset, lf.frequency_offset)
		self.sd_ch1_matrix_mxi_changed(self.sd_ch1_matrix_mxi, lf.ch1_matrix_mxi)
		self.sb_ch1_matrix_mxi_changed(self.sd_ch1_matrix_mxi, lf.ch1_matrix_mxi)
		self.sd_ch2_matrix_mxi_changed(self.sb_ch2_matrix_mxi, lf.ch2_matrix_mxi)
		self.sb_ch2_matrix_mxi_changed(self.sb_ch2_matrix_mxi, lf.ch2_matrix_mxi)
		self.sd_ch1_matrix_myq_changed(self.sd_ch1_matrix_myq, lf.ch1_matrix_myq)
		self.sb_ch1_matrix_myq_changed(self.sd_ch1_matrix_myq, lf.ch1_matrix_myq)
		self.sd_ch2_matrix_myq_changed(self.sb_ch2_matrix_myq, lf.ch2_matrix_myq)
		self.sb_ch2_matrix_myq_changed(self.sb_ch2_matrix_myq, lf.ch2_matrix_myq)
		self.sd_kp_pidv3_axi_0_changed(self.sd_kp_pidv3_axi_0, lf.kp_pidv3_axi_0)
		self.sb_kp_pidv3_axi_0_changed(self.sb_kp_pidv3_axi_0, lf.kp_pidv3_axi_0)
		self.sd_ki_pidv3_axi_0_changed(self.sd_ki_pidv3_axi_0, lf.ki_pidv3_axi_0)
		self.sb_ki_pidv3_axi_0_changed(self.sb_ki_pidv3_axi_0, lf.ki_pidv3_axi_0)
		self.cb_rst_int_pidv3_axi_0_changed(self.cb_rst_int_pidv3_axi_0, lf.rst_int_pidv3_axi_0)
		self.sd_sp_pidv3_axi_0_changed(self.sd_sp_pidv3_axi_0, lf.sp_pidv3_axi_0)
		self.sb_sp_pidv3_axi_0_changed(self.sb_sp_pidv3_axi_0, lf.sp_pidv3_axi_0)
		self.sd_sign_pidv3_axi_0_changed(self.sd_sign_pidv3_axi_0, lf.sign_pidv3_axi_0)
		self.sb_sign_pidv3_axi_0_changed(self.sb_sign_pidv3_axi_0, lf.sign_pidv3_axi_0)
		self.sd_kp_pidv3_axi_1_changed(self.sd_kp_pidv3_axi_1, lf.kp_pidv3_axi_1)
		self.sb_kp_pidv3_axi_1_changed(self.sb_kp_pidv3_axi_1, lf.kp_pidv3_axi_1)
		self.sd_ki_pidv3_axi_1_changed(self.sd_ki_pidv3_axi_1, lf.ki_pidv3_axi_1)
		self.sb_ki_pidv3_axi_1_changed(self.sb_ki_pidv3_axi_1, lf.ki_pidv3_axi_1)
		self.cb_rst_int_pidv3_axi_1_changed(self.cb_rst_int_pidv3_axi_1, lf.rst_int_pidv3_axi_1)
		self.sd_sp_pidv3_axi_1_changed(self.sd_sp_pidv3_axi_1, lf.sp_pidv3_axi_1)
		self.sb_sp_pidv3_axi_1_changed(self.sb_sp_pidv3_axi_1, lf.sp_pidv3_axi_1)
		self.sd_sign_pidv3_axi_1_changed(self.sd_sign_pidv3_axi_1, lf.sign_pidv3_axi_1)
		self.sb_sign_pidv3_axi_1_changed(self.sb_sign_pidv3_axi_1, lf.sign_pidv3_axi_1)
		self.sd_shifterReal_dyn_0_changed(self.sd_shifterReal_dyn_0, lf.shifterReal_dyn_0)
		self.sb_shifterReal_dyn_0_changed(self.sb_shifterReal_dyn_0, lf.shifterReal_dyn_0)
		self.cb_switchReal_0_changed(self.cb_switchReal_0, lf.switchReal_0)
		self.cb_switchReal_1_changed(self.cb_switchReal_1, lf.switchReal_1)
		self.cb_switchReal_2_changed(self.cb_switchReal_2, lf.switchReal_2)
		print("Configuration loaded")

	def bt_save_changed(self, widget):
		try:
			os.remove(str(vals.config))
		except:
			pass
		with open(str(vals.config), "wb") as f:
			f.write(lxml.etree.tostring(vals, pretty_print=True))
		print("Saved")

	def sd_frequency_offset_changed(self, widget, value):
		vals.frequency_offset=value
		print("/dev/frequency_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/frequency_offset", int(value))
		self.sb_frequency_offset.set_value(int(value))

	def sb_frequency_offset_changed(self, widget, value):
		vals.frequency_offset=value
		print("/dev/frequency_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/frequency_offset", int(value))
		self.sd_frequency_offset.set_value(int(float(value)))

	def sd_ch1_matrix_mxi_changed(self, widget, value):
		vals.ch1_matrix_mxi=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_mxi", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_mxi ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_mxi", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_matrix_mxi.set_value(int(value))

	def sb_ch1_matrix_mxi_changed(self, widget, value):
		vals.ch1_matrix_mxi=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_mxi", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_mxi ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_mxi", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_matrix_mxi.set_value(int(float(value)))

	def sd_ch2_matrix_mxi_changed(self, widget, value):
		vals.ch2_matrix_mxi=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_mxi", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_mxi ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_mxi", liboscimp_fpga.CHANB, int(value))
		self.sb_ch2_matrix_mxi.set_value(int(value))

	def sb_ch2_matrix_mxi_changed(self, widget, value):
		vals.ch2_matrix_mxi=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_mxi", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_mxi ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_mxi", liboscimp_fpga.CHANB, int(value))
		self.sd_ch2_matrix_mxi.set_value(int(float(value)))

	def sd_ch1_matrix_myq_changed(self, widget, value):
		vals.ch1_matrix_myq=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_myq", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_myq ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_myq", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_matrix_myq.set_value(int(value))

	def sb_ch1_matrix_myq_changed(self, widget, value):
		vals.ch1_matrix_myq=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_myq", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_myq ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_myq", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_matrix_myq.set_value(int(float(value)))

	def sd_ch2_matrix_myq_changed(self, widget, value):
		vals.ch2_matrix_myq=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_myq", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_myq ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_myq", liboscimp_fpga.CHANB, int(value))
		self.sb_ch2_matrix_myq.set_value(int(value))

	def sb_ch2_matrix_myq_changed(self, widget, value):
		vals.ch2_matrix_myq=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/matrix_myq", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/matrix_myq ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/matrix_myq", liboscimp_fpga.CHANB, int(value))
		self.sd_ch2_matrix_myq.set_value(int(float(value)))

	def sd_kp_pidv3_axi_0_changed(self, widget, value):
		vals.kp_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_0", liboscimp_fpga.KP, int(value))
		self.sb_kp_pidv3_axi_0.set_value(int(value))

	def sb_kp_pidv3_axi_0_changed(self, widget, value):
		vals.kp_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_0", liboscimp_fpga.KP, int(value))
		self.sd_kp_pidv3_axi_0.set_value(int(float(value)))

	def sd_ki_pidv3_axi_0_changed(self, widget, value):
		vals.ki_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_0", liboscimp_fpga.KI, int(value))
		self.sb_ki_pidv3_axi_0.set_value(int(value))

	def sb_ki_pidv3_axi_0_changed(self, widget, value):
		vals.ki_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_0", liboscimp_fpga.KI, int(value))
		self.sd_ki_pidv3_axi_0.set_value(int(float(value)))

	def cb_rst_int_pidv3_axi_0_changed(self, widget, value):
		vals.rst_int_pidv3_axi_0=value
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pidv3_axi_0", 1)
		print("/dev/pidv3_axi_0/rst_int", int(value==True))
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pidv3_axi_0", int(value==True))
		self.cb_rst_int_pidv3_axi_0.set_value(int(value==True))

	def sd_sp_pidv3_axi_0_changed(self, widget, value):
		vals.sp_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set_setpoint("/dev/pidv3_axi_0", int(value))
		self.sb_sp_pidv3_axi_0.set_value(int(value))

	def sb_sp_pidv3_axi_0_changed(self, widget, value):
		vals.sp_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set_setpoint("/dev/pidv3_axi_0", int(value))
		self.sd_sp_pidv3_axi_0.set_value(int(float(value)))

	def sd_sign_pidv3_axi_0_changed(self, widget, value):
		vals.sign_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pidv3_axi_0", int(value))
		self.sb_sign_pidv3_axi_0.set_value(int(value))

	def sb_sign_pidv3_axi_0_changed(self, widget, value):
		vals.sign_pidv3_axi_0=value
		print("/dev/pidv3_axi_0/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pidv3_axi_0", int(value))
		self.sd_sign_pidv3_axi_0.set_value(int(float(value)))

	def sd_kp_pidv3_axi_1_changed(self, widget, value):
		vals.kp_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_1", liboscimp_fpga.KP, int(value))
		self.sb_kp_pidv3_axi_1.set_value(int(value))

	def sb_kp_pidv3_axi_1_changed(self, widget, value):
		vals.kp_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_1", liboscimp_fpga.KP, int(value))
		self.sd_kp_pidv3_axi_1.set_value(int(float(value)))

	def sd_ki_pidv3_axi_1_changed(self, widget, value):
		vals.ki_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_1", liboscimp_fpga.KI, int(value))
		self.sb_ki_pidv3_axi_1.set_value(int(value))

	def sb_ki_pidv3_axi_1_changed(self, widget, value):
		vals.ki_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pidv3_axi_1", liboscimp_fpga.KI, int(value))
		self.sd_ki_pidv3_axi_1.set_value(int(float(value)))

	def cb_rst_int_pidv3_axi_1_changed(self, widget, value):
		vals.rst_int_pidv3_axi_1=value
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pidv3_axi_1", 1)
		print("/dev/pidv3_axi_1/rst_int", int(value==True))
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pidv3_axi_1", int(value==True))
		self.cb_rst_int_pidv3_axi_1.set_value(int(value==True))

	def sd_sp_pidv3_axi_1_changed(self, widget, value):
		vals.sp_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set_setpoint("/dev/pidv3_axi_1", int(value))
		self.sb_sp_pidv3_axi_1.set_value(int(value))

	def sb_sp_pidv3_axi_1_changed(self, widget, value):
		vals.sp_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set_setpoint("/dev/pidv3_axi_1", int(value))
		self.sd_sp_pidv3_axi_1.set_value(int(float(value)))

	def sd_sign_pidv3_axi_1_changed(self, widget, value):
		vals.sign_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pidv3_axi_1", int(value))
		self.sb_sign_pidv3_axi_1.set_value(int(value))

	def sb_sign_pidv3_axi_1_changed(self, widget, value):
		vals.sign_pidv3_axi_1=value
		print("/dev/pidv3_axi_1/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pidv3_axi_1", int(value))
		self.sd_sign_pidv3_axi_1.set_value(int(float(value)))

	def sd_shifterReal_dyn_0_changed(self, widget, value):
		vals.shifterReal_dyn_0=value
		print("/dev/shifterReal_dyn_0", int(value))
		liboscimp_fpga.shifter_set("/dev/shifterReal_dyn_0", int(value))
		self.sb_shifterReal_dyn_0.set_value(int(value))

	def sb_shifterReal_dyn_0_changed(self, widget, value):
		vals.shifterReal_dyn_0=value
		print("/dev/shifterReal_dyn_0", int(value))
		liboscimp_fpga.shifter_set("/dev/shifterReal_dyn_0", int(value))
		self.sd_shifterReal_dyn_0.set_value(int(float(value)))

	def cb_switchReal_0_changed(self, widget, value):
		vals.switchReal_0=value
		liboscimp_fpga.switch_send_conf("/dev/switchReal_0", 1)
		print("/dev/switchReal_0", int(value==True))
		liboscimp_fpga.switch_send_conf("/dev/switchReal_0", int(value==True))
		self.cb_switchReal_0.set_value(int(value==True))

	def cb_switchReal_1_changed(self, widget, value):
		vals.switchReal_1=value
		liboscimp_fpga.switch_send_conf("/dev/switchReal_1", 1)
		print("/dev/switchReal_1", int(value==True))
		liboscimp_fpga.switch_send_conf("/dev/switchReal_1", int(value==True))
		self.cb_switchReal_1.set_value(int(value==True))

	def cb_switchReal_2_changed(self, widget, value):
		vals.switchReal_2=value
		liboscimp_fpga.switch_send_conf("/dev/switchReal_2", 1)
		print("/dev/switchReal_2", int(value==True))
		liboscimp_fpga.switch_send_conf("/dev/switchReal_2", int(value==True))
		self.cb_switchReal_2.set_value(int(value==True))

start(MyApp, address="0.0.0.0", port=80, title="comb_lock_webserver")
