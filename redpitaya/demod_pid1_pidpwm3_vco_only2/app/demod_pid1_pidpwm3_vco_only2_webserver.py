#!/usr/bin/env python

import liboscimp_fpga
import ctypes
import os
from lxml import objectify
import lxml.etree
import remi.gui as gui
from remi import start, App

vals = objectify.Element("item")
vals.config = "demod_pid1_pidpwm3_vco_only2_defconf.xml"
vals.adc1_offset = 0
vals.dac1_offset = 0
vals.dac2_offset = 0
vals.pinc_demod_nco = 0
vals.poff_demod_nco = 0
vals.cb_pinc_demod_nco = "true"
vals.cb_poff_demod_nco = "true"
vals.ch1_mod_input_ampl = 0
vals.pinc_mod_input_nco = 0
vals.poff_mod_input_nco = 0
vals.cb_pinc_mod_input_nco = "true"
vals.cb_poff_mod_input_nco = "true"
vals.pinc_mod_nco = 0
vals.poff_mod_nco = 0
vals.cb_pinc_mod_nco = "true"
vals.cb_poff_mod_nco = "true"
vals.ch1_mod_nco_ampl = 0
vals.pinc_mod_out1_nco = 0
vals.poff_mod_out1_nco = 0
vals.cb_pinc_mod_out1_nco = "true"
vals.cb_poff_mod_out1_nco = "true"
vals.pinc_mod_out2_nco = 0
vals.poff_mod_out2_nco = 0
vals.cb_pinc_mod_out2_nco = "true"
vals.cb_poff_mod_out2_nco = "true"
vals.ch1_mod_out_ampl = 0
vals.ch2_mod_out_ampl = 0
vals.kp_pid1 = 0
vals.ki_pid1 = 0
vals.rst_int_pid1 = "true"
vals.sp_pid1 = 0
vals.sign_pid1 = 0
vals.kp_pid2 = 0
vals.ki_pid2 = 0
vals.rst_int_pid2 = "true"
vals.sp_pid2 = 0
vals.sign_pid2 = 0
vals.pwm_offset = 0
vals.shift_dyn = 9

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

		self.hbox_adc1_offset = gui.HBox(margin="10px")
		self.lb_adc1_offset = gui.Label("/dev/adc1_offset", width="20%", margin="10px")
		self.sd_adc1_offset = gui.Slider(vals.adc1_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_adc1_offset.set_oninput_listener(self.sd_adc1_offset_changed)
		self.sb_adc1_offset = gui.SpinBox(vals.adc1_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_adc1_offset.set_on_change_listener(self.sb_adc1_offset_changed)
		self.sd_adc1_offset_changed(self.sd_adc1_offset, self.sd_adc1_offset.get_value())
		self.hbox_adc1_offset.append(self.lb_adc1_offset)
		self.hbox_adc1_offset.append(self.sd_adc1_offset)
		self.hbox_adc1_offset.append(self.sb_adc1_offset)
		self.w.append(self.hbox_adc1_offset)

		self.hbox_dac1_offset = gui.HBox(margin="10px")
		self.lb_dac1_offset = gui.Label("/dev/dac1_offset", width="20%", margin="10px")
		self.sd_dac1_offset = gui.Slider(vals.dac1_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_dac1_offset.set_oninput_listener(self.sd_dac1_offset_changed)
		self.sb_dac1_offset = gui.SpinBox(vals.dac1_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_dac1_offset.set_on_change_listener(self.sb_dac1_offset_changed)
		self.sd_dac1_offset_changed(self.sd_dac1_offset, self.sd_dac1_offset.get_value())
		self.hbox_dac1_offset.append(self.lb_dac1_offset)
		self.hbox_dac1_offset.append(self.sd_dac1_offset)
		self.hbox_dac1_offset.append(self.sb_dac1_offset)
		self.w.append(self.hbox_dac1_offset)

		self.hbox_dac2_offset = gui.HBox(margin="10px")
		self.lb_dac2_offset = gui.Label("/dev/dac2_offset", width="20%", margin="10px")
		self.sd_dac2_offset = gui.Slider(vals.dac2_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_dac2_offset.set_oninput_listener(self.sd_dac2_offset_changed)
		self.sb_dac2_offset = gui.SpinBox(vals.dac2_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_dac2_offset.set_on_change_listener(self.sb_dac2_offset_changed)
		self.sd_dac2_offset_changed(self.sd_dac2_offset, self.sd_dac2_offset.get_value())
		self.hbox_dac2_offset.append(self.lb_dac2_offset)
		self.hbox_dac2_offset.append(self.sd_dac2_offset)
		self.hbox_dac2_offset.append(self.sb_dac2_offset)
		self.w.append(self.hbox_dac2_offset)

		self.hbox_demod_nco = gui.HBox(margin="10px")
		self.lb_demod_nco = gui.Label("/dev/demod_nco", width="20%", margin="10px")
		self.sd_pinc_demod_nco = gui.Slider(vals.pinc_demod_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_demod_nco.set_oninput_listener(self.sd_pinc_demod_nco_changed)
		self.sb_pinc_demod_nco = gui.SpinBox(vals.pinc_demod_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_demod_nco.set_on_change_listener(self.sb_pinc_demod_nco_changed)
		self.sd_poff_demod_nco = gui.Slider(vals.poff_demod_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_demod_nco.set_oninput_listener(self.sd_poff_demod_nco_changed)
		self.sb_poff_demod_nco = gui.SpinBox(vals.poff_demod_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_demod_nco.set_on_change_listener(self.sb_poff_demod_nco_changed)
		self.cb_pinc_demod_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_demod_nco, width="5%", margin="10px")
		self.cb_pinc_demod_nco.set_on_change_listener(self.cb_pinc_demod_nco_changed)
		self.cb_poff_demod_nco = gui.CheckBoxLabel("poff", vals.cb_poff_demod_nco, width="5%", margin="10px")
		self.cb_poff_demod_nco.set_on_change_listener(self.cb_poff_demod_nco_changed)
		self.hbox_demod_nco.append(self.lb_demod_nco)
		self.hbox_demod_nco.append(self.sd_pinc_demod_nco)
		self.hbox_demod_nco.append(self.sb_pinc_demod_nco)
		self.hbox_demod_nco.append(self.sd_poff_demod_nco)
		self.hbox_demod_nco.append(self.sb_poff_demod_nco)
		self.hbox_demod_nco.append(self.cb_pinc_demod_nco)
		self.hbox_demod_nco.append(self.cb_poff_demod_nco)
		self.w.append(self.hbox_demod_nco)

		self.hbox_ch1_mod_input_ampl = gui.HBox(margin="10px")
		self.lb_ch1_mod_input_ampl = gui.Label("/dev/mod_input_ampl/1", width="20%", margin="10px")
		self.sd_ch1_mod_input_ampl = gui.Slider(vals.ch1_mod_input_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_mod_input_ampl.set_oninput_listener(self.sd_ch1_mod_input_ampl_changed)
		self.sb_ch1_mod_input_ampl = gui.SpinBox(vals.ch1_mod_input_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_mod_input_ampl.set_on_change_listener(self.sb_ch1_mod_input_ampl_changed)
		self.sd_ch1_mod_input_ampl_changed(self.sd_ch1_mod_input_ampl, self.sd_ch1_mod_input_ampl.get_value())
		self.hbox_ch1_mod_input_ampl.append(self.lb_ch1_mod_input_ampl)
		self.hbox_ch1_mod_input_ampl.append(self.sd_ch1_mod_input_ampl)
		self.hbox_ch1_mod_input_ampl.append(self.sb_ch1_mod_input_ampl)
		self.w.append(self.hbox_ch1_mod_input_ampl)

		self.hbox_mod_input_nco = gui.HBox(margin="10px")
		self.lb_mod_input_nco = gui.Label("/dev/mod_input_nco", width="20%", margin="10px")
		self.sd_pinc_mod_input_nco = gui.Slider(vals.pinc_mod_input_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_mod_input_nco.set_oninput_listener(self.sd_pinc_mod_input_nco_changed)
		self.sb_pinc_mod_input_nco = gui.SpinBox(vals.pinc_mod_input_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_mod_input_nco.set_on_change_listener(self.sb_pinc_mod_input_nco_changed)
		self.sd_poff_mod_input_nco = gui.Slider(vals.poff_mod_input_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_mod_input_nco.set_oninput_listener(self.sd_poff_mod_input_nco_changed)
		self.sb_poff_mod_input_nco = gui.SpinBox(vals.poff_mod_input_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_mod_input_nco.set_on_change_listener(self.sb_poff_mod_input_nco_changed)
		self.cb_pinc_mod_input_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_mod_input_nco, width="5%", margin="10px")
		self.cb_pinc_mod_input_nco.set_on_change_listener(self.cb_pinc_mod_input_nco_changed)
		self.cb_poff_mod_input_nco = gui.CheckBoxLabel("poff", vals.cb_poff_mod_input_nco, width="5%", margin="10px")
		self.cb_poff_mod_input_nco.set_on_change_listener(self.cb_poff_mod_input_nco_changed)
		self.hbox_mod_input_nco.append(self.lb_mod_input_nco)
		self.hbox_mod_input_nco.append(self.sd_pinc_mod_input_nco)
		self.hbox_mod_input_nco.append(self.sb_pinc_mod_input_nco)
		self.hbox_mod_input_nco.append(self.sd_poff_mod_input_nco)
		self.hbox_mod_input_nco.append(self.sb_poff_mod_input_nco)
		self.hbox_mod_input_nco.append(self.cb_pinc_mod_input_nco)
		self.hbox_mod_input_nco.append(self.cb_poff_mod_input_nco)
		self.w.append(self.hbox_mod_input_nco)

		self.hbox_mod_nco = gui.HBox(margin="10px")
		self.lb_mod_nco = gui.Label("/dev/mod_nco", width="20%", margin="10px")
		self.sd_pinc_mod_nco = gui.Slider(vals.pinc_mod_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_mod_nco.set_oninput_listener(self.sd_pinc_mod_nco_changed)
		self.sb_pinc_mod_nco = gui.SpinBox(vals.pinc_mod_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_mod_nco.set_on_change_listener(self.sb_pinc_mod_nco_changed)
		self.sd_poff_mod_nco = gui.Slider(vals.poff_mod_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_mod_nco.set_oninput_listener(self.sd_poff_mod_nco_changed)
		self.sb_poff_mod_nco = gui.SpinBox(vals.poff_mod_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_mod_nco.set_on_change_listener(self.sb_poff_mod_nco_changed)
		self.cb_pinc_mod_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_mod_nco, width="5%", margin="10px")
		self.cb_pinc_mod_nco.set_on_change_listener(self.cb_pinc_mod_nco_changed)
		self.cb_poff_mod_nco = gui.CheckBoxLabel("poff", vals.cb_poff_mod_nco, width="5%", margin="10px")
		self.cb_poff_mod_nco.set_on_change_listener(self.cb_poff_mod_nco_changed)
		self.hbox_mod_nco.append(self.lb_mod_nco)
		self.hbox_mod_nco.append(self.sd_pinc_mod_nco)
		self.hbox_mod_nco.append(self.sb_pinc_mod_nco)
		self.hbox_mod_nco.append(self.sd_poff_mod_nco)
		self.hbox_mod_nco.append(self.sb_poff_mod_nco)
		self.hbox_mod_nco.append(self.cb_pinc_mod_nco)
		self.hbox_mod_nco.append(self.cb_poff_mod_nco)
		self.w.append(self.hbox_mod_nco)

		self.hbox_ch1_mod_nco_ampl = gui.HBox(margin="10px")
		self.lb_ch1_mod_nco_ampl = gui.Label("/dev/mod_nco_ampl/1", width="20%", margin="10px")
		self.sd_ch1_mod_nco_ampl = gui.Slider(vals.ch1_mod_nco_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_mod_nco_ampl.set_oninput_listener(self.sd_ch1_mod_nco_ampl_changed)
		self.sb_ch1_mod_nco_ampl = gui.SpinBox(vals.ch1_mod_nco_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_mod_nco_ampl.set_on_change_listener(self.sb_ch1_mod_nco_ampl_changed)
		self.sd_ch1_mod_nco_ampl_changed(self.sd_ch1_mod_nco_ampl, self.sd_ch1_mod_nco_ampl.get_value())
		self.hbox_ch1_mod_nco_ampl.append(self.lb_ch1_mod_nco_ampl)
		self.hbox_ch1_mod_nco_ampl.append(self.sd_ch1_mod_nco_ampl)
		self.hbox_ch1_mod_nco_ampl.append(self.sb_ch1_mod_nco_ampl)
		self.w.append(self.hbox_ch1_mod_nco_ampl)

		self.hbox_mod_out1_nco = gui.HBox(margin="10px")
		self.lb_mod_out1_nco = gui.Label("/dev/mod_out1_nco", width="20%", margin="10px")
		self.sd_pinc_mod_out1_nco = gui.Slider(vals.pinc_mod_out1_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_mod_out1_nco.set_oninput_listener(self.sd_pinc_mod_out1_nco_changed)
		self.sb_pinc_mod_out1_nco = gui.SpinBox(vals.pinc_mod_out1_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_mod_out1_nco.set_on_change_listener(self.sb_pinc_mod_out1_nco_changed)
		self.sd_poff_mod_out1_nco = gui.Slider(vals.poff_mod_out1_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_mod_out1_nco.set_oninput_listener(self.sd_poff_mod_out1_nco_changed)
		self.sb_poff_mod_out1_nco = gui.SpinBox(vals.poff_mod_out1_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_mod_out1_nco.set_on_change_listener(self.sb_poff_mod_out1_nco_changed)
		self.cb_pinc_mod_out1_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_mod_out1_nco, width="5%", margin="10px")
		self.cb_pinc_mod_out1_nco.set_on_change_listener(self.cb_pinc_mod_out1_nco_changed)
		self.cb_poff_mod_out1_nco = gui.CheckBoxLabel("poff", vals.cb_poff_mod_out1_nco, width="5%", margin="10px")
		self.cb_poff_mod_out1_nco.set_on_change_listener(self.cb_poff_mod_out1_nco_changed)
		self.hbox_mod_out1_nco.append(self.lb_mod_out1_nco)
		self.hbox_mod_out1_nco.append(self.sd_pinc_mod_out1_nco)
		self.hbox_mod_out1_nco.append(self.sb_pinc_mod_out1_nco)
		self.hbox_mod_out1_nco.append(self.sd_poff_mod_out1_nco)
		self.hbox_mod_out1_nco.append(self.sb_poff_mod_out1_nco)
		self.hbox_mod_out1_nco.append(self.cb_pinc_mod_out1_nco)
		self.hbox_mod_out1_nco.append(self.cb_poff_mod_out1_nco)
		self.w.append(self.hbox_mod_out1_nco)

		self.hbox_mod_out2_nco = gui.HBox(margin="10px")
		self.lb_mod_out2_nco = gui.Label("/dev/mod_out2_nco", width="20%", margin="10px")
		self.sd_pinc_mod_out2_nco = gui.Slider(vals.pinc_mod_out2_nco, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_mod_out2_nco.set_oninput_listener(self.sd_pinc_mod_out2_nco_changed)
		self.sb_pinc_mod_out2_nco = gui.SpinBox(vals.pinc_mod_out2_nco, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_mod_out2_nco.set_on_change_listener(self.sb_pinc_mod_out2_nco_changed)
		self.sd_poff_mod_out2_nco = gui.Slider(vals.poff_mod_out2_nco, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_mod_out2_nco.set_oninput_listener(self.sd_poff_mod_out2_nco_changed)
		self.sb_poff_mod_out2_nco = gui.SpinBox(vals.poff_mod_out2_nco, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_mod_out2_nco.set_on_change_listener(self.sb_poff_mod_out2_nco_changed)
		self.cb_pinc_mod_out2_nco = gui.CheckBoxLabel("pinc", vals.cb_pinc_mod_out2_nco, width="5%", margin="10px")
		self.cb_pinc_mod_out2_nco.set_on_change_listener(self.cb_pinc_mod_out2_nco_changed)
		self.cb_poff_mod_out2_nco = gui.CheckBoxLabel("poff", vals.cb_poff_mod_out2_nco, width="5%", margin="10px")
		self.cb_poff_mod_out2_nco.set_on_change_listener(self.cb_poff_mod_out2_nco_changed)
		self.hbox_mod_out2_nco.append(self.lb_mod_out2_nco)
		self.hbox_mod_out2_nco.append(self.sd_pinc_mod_out2_nco)
		self.hbox_mod_out2_nco.append(self.sb_pinc_mod_out2_nco)
		self.hbox_mod_out2_nco.append(self.sd_poff_mod_out2_nco)
		self.hbox_mod_out2_nco.append(self.sb_poff_mod_out2_nco)
		self.hbox_mod_out2_nco.append(self.cb_pinc_mod_out2_nco)
		self.hbox_mod_out2_nco.append(self.cb_poff_mod_out2_nco)
		self.w.append(self.hbox_mod_out2_nco)

		self.hbox_ch1_mod_out_ampl = gui.HBox(margin="10px")
		self.lb_ch1_mod_out_ampl = gui.Label("/dev/mod_out_ampl/1", width="20%", margin="10px")
		self.sd_ch1_mod_out_ampl = gui.Slider(vals.ch1_mod_out_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch1_mod_out_ampl.set_oninput_listener(self.sd_ch1_mod_out_ampl_changed)
		self.sb_ch1_mod_out_ampl = gui.SpinBox(vals.ch1_mod_out_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch1_mod_out_ampl.set_on_change_listener(self.sb_ch1_mod_out_ampl_changed)
		self.sd_ch1_mod_out_ampl_changed(self.sd_ch1_mod_out_ampl, self.sd_ch1_mod_out_ampl.get_value())
		self.hbox_ch1_mod_out_ampl.append(self.lb_ch1_mod_out_ampl)
		self.hbox_ch1_mod_out_ampl.append(self.sd_ch1_mod_out_ampl)
		self.hbox_ch1_mod_out_ampl.append(self.sb_ch1_mod_out_ampl)
		self.w.append(self.hbox_ch1_mod_out_ampl)

		self.hbox_ch2_mod_out_ampl = gui.HBox(margin="10px")
		self.lb_ch2_mod_out_ampl = gui.Label("/dev/mod_out_ampl/2", width="20%", margin="10px")
		self.sd_ch2_mod_out_ampl = gui.Slider(vals.ch2_mod_out_ampl, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ch2_mod_out_ampl.set_oninput_listener(self.sd_ch2_mod_out_ampl_changed)
		self.sb_ch2_mod_out_ampl = gui.SpinBox(vals.ch2_mod_out_ampl, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ch2_mod_out_ampl.set_on_change_listener(self.sb_ch2_mod_out_ampl_changed)
		self.sd_ch2_mod_out_ampl_changed(self.sd_ch2_mod_out_ampl, self.sd_ch2_mod_out_ampl.get_value())
		self.hbox_ch2_mod_out_ampl.append(self.lb_ch2_mod_out_ampl)
		self.hbox_ch2_mod_out_ampl.append(self.sd_ch2_mod_out_ampl)
		self.hbox_ch2_mod_out_ampl.append(self.sb_ch2_mod_out_ampl)
		self.w.append(self.hbox_ch2_mod_out_ampl)

		self.hbox_kp_pid1 = gui.HBox(margin="10px")
		self.lb_kp_pid1 = gui.Label("/dev/pid1/kp", width="20%", margin="10px")
		self.sd_kp_pid1 = gui.Slider(vals.kp_pid1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_kp_pid1.set_oninput_listener(self.sd_kp_pid1_changed)
		self.sb_kp_pid1 = gui.SpinBox(vals.kp_pid1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_kp_pid1.set_on_change_listener(self.sb_kp_pid1_changed)
		self.sd_kp_pid1_changed(self.sd_kp_pid1, self.sd_kp_pid1.get_value())
		self.hbox_kp_pid1.append(self.lb_kp_pid1)
		self.hbox_kp_pid1.append(self.sd_kp_pid1)
		self.hbox_kp_pid1.append(self.sb_kp_pid1)
		self.w.append(self.hbox_kp_pid1)

		self.hbox_ki_pid1 = gui.HBox(margin="10px")
		self.lb_ki_pid1 = gui.Label("/dev/pid1/ki", width="20%", margin="10px")
		self.sd_ki_pid1 = gui.Slider(vals.ki_pid1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pid1.set_oninput_listener(self.sd_ki_pid1_changed)
		self.sb_ki_pid1 = gui.SpinBox(vals.ki_pid1, -8192, 8191, 1, width="20%", margin="10px")
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
		self.sd_sp_pid1 = gui.Slider(vals.sp_pid1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sp_pid1.set_oninput_listener(self.sd_sp_pid1_changed)
		self.sb_sp_pid1 = gui.SpinBox(vals.sp_pid1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sp_pid1.set_on_change_listener(self.sb_sp_pid1_changed)
		self.sd_sp_pid1_changed(self.sd_sp_pid1, self.sd_sp_pid1.get_value())
		self.hbox_sp_pid1.append(self.lb_sp_pid1)
		self.hbox_sp_pid1.append(self.sd_sp_pid1)
		self.hbox_sp_pid1.append(self.sb_sp_pid1)
		self.w.append(self.hbox_sp_pid1)

		self.hbox_sign_pid1 = gui.HBox(margin="10px")
		self.lb_sign_pid1 = gui.Label("/dev/pid1/sign", width="20%", margin="10px")
		self.sd_sign_pid1 = gui.Slider(vals.sign_pid1, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sign_pid1.set_oninput_listener(self.sd_sign_pid1_changed)
		self.sb_sign_pid1 = gui.SpinBox(vals.sign_pid1, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sign_pid1.set_on_change_listener(self.sb_sign_pid1_changed)
		self.sd_sign_pid1_changed(self.sd_sign_pid1, self.sd_sign_pid1.get_value())
		self.hbox_sign_pid1.append(self.lb_sign_pid1)
		self.hbox_sign_pid1.append(self.sd_sign_pid1)
		self.hbox_sign_pid1.append(self.sb_sign_pid1)
		self.w.append(self.hbox_sign_pid1)

		self.hbox_kp_pid2 = gui.HBox(margin="10px")
		self.lb_kp_pid2 = gui.Label("/dev/pid2/kp", width="20%", margin="10px")
		self.sd_kp_pid2 = gui.Slider(vals.kp_pid2, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_kp_pid2.set_oninput_listener(self.sd_kp_pid2_changed)
		self.sb_kp_pid2 = gui.SpinBox(vals.kp_pid2, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_kp_pid2.set_on_change_listener(self.sb_kp_pid2_changed)
		self.sd_kp_pid2_changed(self.sd_kp_pid2, self.sd_kp_pid2.get_value())
		self.hbox_kp_pid2.append(self.lb_kp_pid2)
		self.hbox_kp_pid2.append(self.sd_kp_pid2)
		self.hbox_kp_pid2.append(self.sb_kp_pid2)
		self.w.append(self.hbox_kp_pid2)

		self.hbox_ki_pid2 = gui.HBox(margin="10px")
		self.lb_ki_pid2 = gui.Label("/dev/pid2/ki", width="20%", margin="10px")
		self.sd_ki_pid2 = gui.Slider(vals.ki_pid2, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pid2.set_oninput_listener(self.sd_ki_pid2_changed)
		self.sb_ki_pid2 = gui.SpinBox(vals.ki_pid2, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ki_pid2.set_on_change_listener(self.sb_ki_pid2_changed)
		self.sd_ki_pid2_changed(self.sd_ki_pid2, self.sd_ki_pid2.get_value())
		self.cb_rst_int_pid2 = gui.CheckBoxLabel("rst_int", vals.rst_int_pid2, width="5%", margin="10px")
		self.cb_rst_int_pid2.set_on_change_listener(self.cb_rst_int_pid2_changed)
		self.hbox_ki_pid2.append(self.lb_ki_pid2)
		self.hbox_ki_pid2.append(self.sd_ki_pid2)
		self.hbox_ki_pid2.append(self.sb_ki_pid2)
		self.hbox_ki_pid2.append(self.cb_rst_int_pid2)
		self.w.append(self.hbox_ki_pid2)

		self.hbox_sp_pid2 = gui.HBox(margin="10px")
		self.lb_sp_pid2 = gui.Label("/dev/pid2/setpoint", width="20%", margin="10px")
		self.sd_sp_pid2 = gui.Slider(vals.sp_pid2, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sp_pid2.set_oninput_listener(self.sd_sp_pid2_changed)
		self.sb_sp_pid2 = gui.SpinBox(vals.sp_pid2, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sp_pid2.set_on_change_listener(self.sb_sp_pid2_changed)
		self.sd_sp_pid2_changed(self.sd_sp_pid2, self.sd_sp_pid2.get_value())
		self.hbox_sp_pid2.append(self.lb_sp_pid2)
		self.hbox_sp_pid2.append(self.sd_sp_pid2)
		self.hbox_sp_pid2.append(self.sb_sp_pid2)
		self.w.append(self.hbox_sp_pid2)

		self.hbox_sign_pid2 = gui.HBox(margin="10px")
		self.lb_sign_pid2 = gui.Label("/dev/pid2/sign", width="20%", margin="10px")
		self.sd_sign_pid2 = gui.Slider(vals.sign_pid2, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sign_pid2.set_oninput_listener(self.sd_sign_pid2_changed)
		self.sb_sign_pid2 = gui.SpinBox(vals.sign_pid2, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sign_pid2.set_on_change_listener(self.sb_sign_pid2_changed)
		self.sd_sign_pid2_changed(self.sd_sign_pid2, self.sd_sign_pid2.get_value())
		self.hbox_sign_pid2.append(self.lb_sign_pid2)
		self.hbox_sign_pid2.append(self.sd_sign_pid2)
		self.hbox_sign_pid2.append(self.sb_sign_pid2)
		self.w.append(self.hbox_sign_pid2)

		self.hbox_pwm_offset = gui.HBox(margin="10px")
		self.lb_pwm_offset = gui.Label("/dev/pwm_offset", width="20%", margin="10px")
		self.sd_pwm_offset = gui.Slider(vals.pwm_offset, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_pwm_offset.set_oninput_listener(self.sd_pwm_offset_changed)
		self.sb_pwm_offset = gui.SpinBox(vals.pwm_offset, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_pwm_offset.set_on_change_listener(self.sb_pwm_offset_changed)
		self.sd_pwm_offset_changed(self.sd_pwm_offset, self.sd_pwm_offset.get_value())
		self.hbox_pwm_offset.append(self.lb_pwm_offset)
		self.hbox_pwm_offset.append(self.sd_pwm_offset)
		self.hbox_pwm_offset.append(self.sb_pwm_offset)
		self.w.append(self.hbox_pwm_offset)

		self.hbox_shift_dyn = gui.HBox(margin="10px")
		self.lb_shift_dyn = gui.Label("/dev/shift_dyn", width="20%", margin="10px")
		self.sd_shift_dyn = gui.Slider(vals.shift_dyn, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_shift_dyn.set_oninput_listener(self.sd_shift_dyn_changed)
		self.sb_shift_dyn = gui.SpinBox(vals.shift_dyn, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_shift_dyn.set_on_change_listener(self.sb_shift_dyn_changed)
		self.sd_shift_dyn_changed(self.sd_shift_dyn, self.sd_shift_dyn.get_value())
		self.hbox_shift_dyn.append(self.lb_shift_dyn)
		self.hbox_shift_dyn.append(self.sd_shift_dyn)
		self.hbox_shift_dyn.append(self.sb_shift_dyn)
		self.w.append(self.hbox_shift_dyn)

		return self.w

	def dtext_conf_file_changed(self, widget, value):
		print(value)
		vals.config=value

	def bt_load_changed(self, widget):
		with open(str(vals.config), "r") as f:
			 lf = objectify.fromstring(f.read())

		self.sd_adc1_offset_changed(self.sd_adc1_offset, lf.adc1_offset)
		self.sb_adc1_offset_changed(self.sb_adc1_offset, lf.adc1_offset)
		self.sd_dac1_offset_changed(self.sd_dac1_offset, lf.dac1_offset)
		self.sb_dac1_offset_changed(self.sb_dac1_offset, lf.dac1_offset)
		self.sd_dac2_offset_changed(self.sd_dac2_offset, lf.dac2_offset)
		self.sb_dac2_offset_changed(self.sb_dac2_offset, lf.dac2_offset)
		self.sd_pinc_demod_nco_changed(self.sd_pinc_demod_nco, lf.pinc_demod_nco)
		self.sb_pinc_demod_nco_changed(self.sb_pinc_demod_nco, lf.pinc_demod_nco)
		self.sd_poff_demod_nco_changed(self.sd_poff_demod_nco, lf.poff_demod_nco)
		self.sb_poff_demod_nco_changed(self.sb_poff_demod_nco, lf.poff_demod_nco)
		self.cb_pinc_demod_nco_changed(self.cb_pinc_demod_nco, lf.cb_pinc_demod_nco)
		self.cb_poff_demod_nco_changed(self.cb_poff_demod_nco, lf.cb_poff_demod_nco)
		self.sd_ch1_mod_input_ampl_changed(self.sd_ch1_mod_input_ampl, lf.ch1_mod_input_ampl)
		self.sb_ch1_mod_input_ampl_changed(self.sd_ch1_mod_input_ampl, lf.ch1_mod_input_ampl)
		self.sd_pinc_mod_input_nco_changed(self.sd_pinc_mod_input_nco, lf.pinc_mod_input_nco)
		self.sb_pinc_mod_input_nco_changed(self.sb_pinc_mod_input_nco, lf.pinc_mod_input_nco)
		self.sd_poff_mod_input_nco_changed(self.sd_poff_mod_input_nco, lf.poff_mod_input_nco)
		self.sb_poff_mod_input_nco_changed(self.sb_poff_mod_input_nco, lf.poff_mod_input_nco)
		self.cb_pinc_mod_input_nco_changed(self.cb_pinc_mod_input_nco, lf.cb_pinc_mod_input_nco)
		self.cb_poff_mod_input_nco_changed(self.cb_poff_mod_input_nco, lf.cb_poff_mod_input_nco)
		self.sd_pinc_mod_nco_changed(self.sd_pinc_mod_nco, lf.pinc_mod_nco)
		self.sb_pinc_mod_nco_changed(self.sb_pinc_mod_nco, lf.pinc_mod_nco)
		self.sd_poff_mod_nco_changed(self.sd_poff_mod_nco, lf.poff_mod_nco)
		self.sb_poff_mod_nco_changed(self.sb_poff_mod_nco, lf.poff_mod_nco)
		self.cb_pinc_mod_nco_changed(self.cb_pinc_mod_nco, lf.cb_pinc_mod_nco)
		self.cb_poff_mod_nco_changed(self.cb_poff_mod_nco, lf.cb_poff_mod_nco)
		self.sd_ch1_mod_nco_ampl_changed(self.sd_ch1_mod_nco_ampl, lf.ch1_mod_nco_ampl)
		self.sb_ch1_mod_nco_ampl_changed(self.sd_ch1_mod_nco_ampl, lf.ch1_mod_nco_ampl)
		self.sd_pinc_mod_out1_nco_changed(self.sd_pinc_mod_out1_nco, lf.pinc_mod_out1_nco)
		self.sb_pinc_mod_out1_nco_changed(self.sb_pinc_mod_out1_nco, lf.pinc_mod_out1_nco)
		self.sd_poff_mod_out1_nco_changed(self.sd_poff_mod_out1_nco, lf.poff_mod_out1_nco)
		self.sb_poff_mod_out1_nco_changed(self.sb_poff_mod_out1_nco, lf.poff_mod_out1_nco)
		self.cb_pinc_mod_out1_nco_changed(self.cb_pinc_mod_out1_nco, lf.cb_pinc_mod_out1_nco)
		self.cb_poff_mod_out1_nco_changed(self.cb_poff_mod_out1_nco, lf.cb_poff_mod_out1_nco)
		self.sd_pinc_mod_out2_nco_changed(self.sd_pinc_mod_out2_nco, lf.pinc_mod_out2_nco)
		self.sb_pinc_mod_out2_nco_changed(self.sb_pinc_mod_out2_nco, lf.pinc_mod_out2_nco)
		self.sd_poff_mod_out2_nco_changed(self.sd_poff_mod_out2_nco, lf.poff_mod_out2_nco)
		self.sb_poff_mod_out2_nco_changed(self.sb_poff_mod_out2_nco, lf.poff_mod_out2_nco)
		self.cb_pinc_mod_out2_nco_changed(self.cb_pinc_mod_out2_nco, lf.cb_pinc_mod_out2_nco)
		self.cb_poff_mod_out2_nco_changed(self.cb_poff_mod_out2_nco, lf.cb_poff_mod_out2_nco)
		self.sd_ch1_mod_out_ampl_changed(self.sd_ch1_mod_out_ampl, lf.ch1_mod_out_ampl)
		self.sb_ch1_mod_out_ampl_changed(self.sd_ch1_mod_out_ampl, lf.ch1_mod_out_ampl)
		self.sd_ch2_mod_out_ampl_changed(self.sb_ch2_mod_out_ampl, lf.ch2_mod_out_ampl)
		self.sb_ch2_mod_out_ampl_changed(self.sb_ch2_mod_out_ampl, lf.ch2_mod_out_ampl)
		self.sd_kp_pid1_changed(self.sd_kp_pid1, lf.kp_pid1)
		self.sb_kp_pid1_changed(self.sb_kp_pid1, lf.kp_pid1)
		self.sd_ki_pid1_changed(self.sd_ki_pid1, lf.ki_pid1)
		self.sb_ki_pid1_changed(self.sb_ki_pid1, lf.ki_pid1)
		self.cb_rst_int_pid1_changed(self.cb_rst_int_pid1, lf.rst_int_pid1)
		self.sd_sp_pid1_changed(self.sd_sp_pid1, lf.sp_pid1)
		self.sb_sp_pid1_changed(self.sb_sp_pid1, lf.sp_pid1)
		self.sd_sign_pid1_changed(self.sd_sign_pid1, lf.sign_pid1)
		self.sb_sign_pid1_changed(self.sb_sign_pid1, lf.sign_pid1)
		self.sd_kp_pid2_changed(self.sd_kp_pid2, lf.kp_pid2)
		self.sb_kp_pid2_changed(self.sb_kp_pid2, lf.kp_pid2)
		self.sd_ki_pid2_changed(self.sd_ki_pid2, lf.ki_pid2)
		self.sb_ki_pid2_changed(self.sb_ki_pid2, lf.ki_pid2)
		self.cb_rst_int_pid2_changed(self.cb_rst_int_pid2, lf.rst_int_pid2)
		self.sd_sp_pid2_changed(self.sd_sp_pid2, lf.sp_pid2)
		self.sb_sp_pid2_changed(self.sb_sp_pid2, lf.sp_pid2)
		self.sd_sign_pid2_changed(self.sd_sign_pid2, lf.sign_pid2)
		self.sb_sign_pid2_changed(self.sb_sign_pid2, lf.sign_pid2)
		self.sd_pwm_offset_changed(self.sd_pwm_offset, lf.pwm_offset)
		self.sb_pwm_offset_changed(self.sb_pwm_offset, lf.pwm_offset)
		self.sd_shift_dyn_changed(self.sd_shift_dyn, lf.shift_dyn)
		self.sb_shift_dyn_changed(self.sb_shift_dyn, lf.shift_dyn)
		print("Configuration loaded")

	def bt_save_changed(self, widget):
		try:
			os.remove(str(vals.config))
		except:
			pass
		with open(str(vals.config), "wb") as f:
			f.write(lxml.etree.tostring(vals, pretty_print=True))
		print("Saved")

	def sd_adc1_offset_changed(self, widget, value):
		vals.adc1_offset=value
		print("/dev/adc1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/adc1_offset", int(value))
		self.sb_adc1_offset.set_value(int(value))

	def sb_adc1_offset_changed(self, widget, value):
		vals.adc1_offset=value
		print("/dev/adc1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/adc1_offset", int(value))
		self.sd_adc1_offset.set_value(int(float(value)))

	def sd_dac1_offset_changed(self, widget, value):
		vals.dac1_offset=value
		print("/dev/dac1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac1_offset", int(value))
		self.sb_dac1_offset.set_value(int(value))

	def sb_dac1_offset_changed(self, widget, value):
		vals.dac1_offset=value
		print("/dev/dac1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac1_offset", int(value))
		self.sd_dac1_offset.set_value(int(float(value)))

	def sd_dac2_offset_changed(self, widget, value):
		vals.dac2_offset=value
		print("/dev/dac2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac2_offset", int(value))
		self.sb_dac2_offset.set_value(int(value))

	def sb_dac2_offset_changed(self, widget, value):
		vals.dac2_offset=value
		print("/dev/dac2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac2_offset", int(value))
		self.sd_dac2_offset.set_value(int(float(value)))

	def sd_pinc_demod_nco_changed(self, widget, value):
		vals.pinc_demod_nco=value
		print("/dev/demod_nco", 125000000, int(value), 40, int(self.sb_poff_demod_nco.get_value()), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_demod_nco.get_value()), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		self.sb_pinc_demod_nco.set_value(int(value))

	def sb_pinc_demod_nco_changed(self, widget, value):
		vals.pinc_demod_nco=value
		print("/dev/demod_nco", 125000000, value, 40, int(self.sb_poff_demod_nco.get_value()), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_demod_nco.get_value()), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		self.sd_pinc_demod_nco.set_value(value)

	def sd_poff_demod_nco_changed(self, widget, value):
		vals.poff_demod_nco=value
		print("/dev/demod_nco", 125000000, self.sb_pinc_demod_nco.get_value(), 40, int(value), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod_nco.get_value())), 40, int(value), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		self.sb_poff_demod_nco.set_value(value)

	def sb_poff_demod_nco_changed(self, widget, value):
		vals.poff_demod_nco=value
		print("/dev/demod_nco", 125000000, self.sb_pinc_demod_nco.get_value(), 40, int(value), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod_nco.get_value())), 40, int(value), int(self.cb_pinc_demod_nco.get_value()), int(self.cb_poff_demod_nco.get_value()))
		self.sd_poff_demod_nco.set_value(value)

	def cb_pinc_demod_nco_changed(self, widget, value):
		vals.cb_pinc_demod_nco=value
		print("/dev/demod_nco", 125000000, self.sb_pinc_demod_nco.get_value(), 40, int(self.sb_poff_demod_nco.get_value()), int(value=="true"), int(self.cb_poff_demod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod_nco.get_value())), 40, int(self.sb_poff_demod_nco.get_value()), int(value == "true"), int(self.cb_poff_demod_nco.get_value()))
		self.cb_pinc_demod_nco.set_value(int(value=="true"))

	def cb_poff_demod_nco_changed(self, widget, value):
		vals.cb_poff_demod_nco=value
		print("/dev/demod_nco", 125000000, self.sb_pinc_demod_nco.get_value(), 40, int(self.sb_poff_demod_nco.get_value()), int(self.cb_pinc_demod_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod_nco.get_value())), 40, int(self.sb_poff_demod_nco.get_value()), int(self.cb_pinc_demod_nco.get_value()), int(value=="true"))
		self.cb_poff_demod_nco.set_value(int(value=="true"))

	def sd_ch1_mod_input_ampl_changed(self, widget, value):
		vals.ch1_mod_input_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_input_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_input_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_input_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_mod_input_ampl.set_value(int(value))

	def sb_ch1_mod_input_ampl_changed(self, widget, value):
		vals.ch1_mod_input_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_input_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_input_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_input_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_mod_input_ampl.set_value(int(float(value)))

	def sd_pinc_mod_input_nco_changed(self, widget, value):
		vals.pinc_mod_input_nco=value
		print("/dev/mod_input_nco", 125000000, int(value), 40, int(self.sb_poff_mod_input_nco.get_value()), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_input_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_mod_input_nco.get_value()), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		self.sb_pinc_mod_input_nco.set_value(int(value))

	def sb_pinc_mod_input_nco_changed(self, widget, value):
		vals.pinc_mod_input_nco=value
		print("/dev/mod_input_nco", 125000000, value, 40, int(self.sb_poff_mod_input_nco.get_value()), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_input_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_mod_input_nco.get_value()), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		self.sd_pinc_mod_input_nco.set_value(value)

	def sd_poff_mod_input_nco_changed(self, widget, value):
		vals.poff_mod_input_nco=value
		print("/dev/mod_input_nco", 125000000, self.sb_pinc_mod_input_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_input_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_input_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		self.sb_poff_mod_input_nco.set_value(value)

	def sb_poff_mod_input_nco_changed(self, widget, value):
		vals.poff_mod_input_nco=value
		print("/dev/mod_input_nco", 125000000, self.sb_pinc_mod_input_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_input_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_input_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_input_nco.get_value()), int(self.cb_poff_mod_input_nco.get_value()))
		self.sd_poff_mod_input_nco.set_value(value)

	def cb_pinc_mod_input_nco_changed(self, widget, value):
		vals.cb_pinc_mod_input_nco=value
		print("/dev/mod_input_nco", 125000000, self.sb_pinc_mod_input_nco.get_value(), 40, int(self.sb_poff_mod_input_nco.get_value()), int(value=="true"), int(self.cb_poff_mod_input_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_input_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_input_nco.get_value())), 40, int(self.sb_poff_mod_input_nco.get_value()), int(value == "true"), int(self.cb_poff_mod_input_nco.get_value()))
		self.cb_pinc_mod_input_nco.set_value(int(value=="true"))

	def cb_poff_mod_input_nco_changed(self, widget, value):
		vals.cb_poff_mod_input_nco=value
		print("/dev/mod_input_nco", 125000000, self.sb_pinc_mod_input_nco.get_value(), 40, int(self.sb_poff_mod_input_nco.get_value()), int(self.cb_pinc_mod_input_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_input_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_input_nco.get_value())), 40, int(self.sb_poff_mod_input_nco.get_value()), int(self.cb_pinc_mod_input_nco.get_value()), int(value=="true"))
		self.cb_poff_mod_input_nco.set_value(int(value=="true"))

	def sd_pinc_mod_nco_changed(self, widget, value):
		vals.pinc_mod_nco=value
		print("/dev/mod_nco", 125000000, int(value), 40, int(self.sb_poff_mod_nco.get_value()), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_mod_nco.get_value()), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		self.sb_pinc_mod_nco.set_value(int(value))

	def sb_pinc_mod_nco_changed(self, widget, value):
		vals.pinc_mod_nco=value
		print("/dev/mod_nco", 125000000, value, 40, int(self.sb_poff_mod_nco.get_value()), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_mod_nco.get_value()), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		self.sd_pinc_mod_nco.set_value(value)

	def sd_poff_mod_nco_changed(self, widget, value):
		vals.poff_mod_nco=value
		print("/dev/mod_nco", 125000000, self.sb_pinc_mod_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		self.sb_poff_mod_nco.set_value(value)

	def sb_poff_mod_nco_changed(self, widget, value):
		vals.poff_mod_nco=value
		print("/dev/mod_nco", 125000000, self.sb_pinc_mod_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_nco.get_value()), int(self.cb_poff_mod_nco.get_value()))
		self.sd_poff_mod_nco.set_value(value)

	def cb_pinc_mod_nco_changed(self, widget, value):
		vals.cb_pinc_mod_nco=value
		print("/dev/mod_nco", 125000000, self.sb_pinc_mod_nco.get_value(), 40, int(self.sb_poff_mod_nco.get_value()), int(value=="true"), int(self.cb_poff_mod_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_nco.get_value())), 40, int(self.sb_poff_mod_nco.get_value()), int(value == "true"), int(self.cb_poff_mod_nco.get_value()))
		self.cb_pinc_mod_nco.set_value(int(value=="true"))

	def cb_poff_mod_nco_changed(self, widget, value):
		vals.cb_poff_mod_nco=value
		print("/dev/mod_nco", 125000000, self.sb_pinc_mod_nco.get_value(), 40, int(self.sb_poff_mod_nco.get_value()), int(self.cb_pinc_mod_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_nco.get_value())), 40, int(self.sb_poff_mod_nco.get_value()), int(self.cb_pinc_mod_nco.get_value()), int(value=="true"))
		self.cb_poff_mod_nco.set_value(int(value=="true"))

	def sd_ch1_mod_nco_ampl_changed(self, widget, value):
		vals.ch1_mod_nco_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_nco_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_nco_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_nco_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_mod_nco_ampl.set_value(int(value))

	def sb_ch1_mod_nco_ampl_changed(self, widget, value):
		vals.ch1_mod_nco_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_nco_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_nco_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_nco_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_mod_nco_ampl.set_value(int(float(value)))

	def sd_pinc_mod_out1_nco_changed(self, widget, value):
		vals.pinc_mod_out1_nco=value
		print("/dev/mod_out1_nco", 125000000, int(value), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out1_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		self.sb_pinc_mod_out1_nco.set_value(int(value))

	def sb_pinc_mod_out1_nco_changed(self, widget, value):
		vals.pinc_mod_out1_nco=value
		print("/dev/mod_out1_nco", 125000000, value, 40, int(self.sb_poff_mod_out1_nco.get_value()), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		self.sd_pinc_mod_out1_nco.set_value(value)

	def sd_poff_mod_out1_nco_changed(self, widget, value):
		vals.poff_mod_out1_nco=value
		print("/dev/mod_out1_nco", 125000000, self.sb_pinc_mod_out1_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out1_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		self.sb_poff_mod_out1_nco.set_value(value)

	def sb_poff_mod_out1_nco_changed(self, widget, value):
		vals.poff_mod_out1_nco=value
		print("/dev/mod_out1_nco", 125000000, self.sb_pinc_mod_out1_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out1_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_out1_nco.get_value()), int(self.cb_poff_mod_out1_nco.get_value()))
		self.sd_poff_mod_out1_nco.set_value(value)

	def cb_pinc_mod_out1_nco_changed(self, widget, value):
		vals.cb_pinc_mod_out1_nco=value
		print("/dev/mod_out1_nco", 125000000, self.sb_pinc_mod_out1_nco.get_value(), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(value=="true"), int(self.cb_poff_mod_out1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out1_nco.get_value())), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(value == "true"), int(self.cb_poff_mod_out1_nco.get_value()))
		self.cb_pinc_mod_out1_nco.set_value(int(value=="true"))

	def cb_poff_mod_out1_nco_changed(self, widget, value):
		vals.cb_poff_mod_out1_nco=value
		print("/dev/mod_out1_nco", 125000000, self.sb_pinc_mod_out1_nco.get_value(), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(self.cb_pinc_mod_out1_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out1_nco.get_value())), 40, int(self.sb_poff_mod_out1_nco.get_value()), int(self.cb_pinc_mod_out1_nco.get_value()), int(value=="true"))
		self.cb_poff_mod_out1_nco.set_value(int(value=="true"))

	def sd_pinc_mod_out2_nco_changed(self, widget, value):
		vals.pinc_mod_out2_nco=value
		print("/dev/mod_out2_nco", 125000000, int(value), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out2_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		self.sb_pinc_mod_out2_nco.set_value(int(value))

	def sb_pinc_mod_out2_nco_changed(self, widget, value):
		vals.pinc_mod_out2_nco=value
		print("/dev/mod_out2_nco", 125000000, value, 40, int(self.sb_poff_mod_out2_nco.get_value()), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		self.sd_pinc_mod_out2_nco.set_value(value)

	def sd_poff_mod_out2_nco_changed(self, widget, value):
		vals.poff_mod_out2_nco=value
		print("/dev/mod_out2_nco", 125000000, self.sb_pinc_mod_out2_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out2_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		self.sb_poff_mod_out2_nco.set_value(value)

	def sb_poff_mod_out2_nco_changed(self, widget, value):
		vals.poff_mod_out2_nco=value
		print("/dev/mod_out2_nco", 125000000, self.sb_pinc_mod_out2_nco.get_value(), 40, int(value), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out2_nco.get_value())), 40, int(value), int(self.cb_pinc_mod_out2_nco.get_value()), int(self.cb_poff_mod_out2_nco.get_value()))
		self.sd_poff_mod_out2_nco.set_value(value)

	def cb_pinc_mod_out2_nco_changed(self, widget, value):
		vals.cb_pinc_mod_out2_nco=value
		print("/dev/mod_out2_nco", 125000000, self.sb_pinc_mod_out2_nco.get_value(), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(value=="true"), int(self.cb_poff_mod_out2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out2_nco.get_value())), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(value == "true"), int(self.cb_poff_mod_out2_nco.get_value()))
		self.cb_pinc_mod_out2_nco.set_value(int(value=="true"))

	def cb_poff_mod_out2_nco_changed(self, widget, value):
		vals.cb_poff_mod_out2_nco=value
		print("/dev/mod_out2_nco", 125000000, self.sb_pinc_mod_out2_nco.get_value(), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(self.cb_pinc_mod_out2_nco.get_value()), int(value=="true"))
		liboscimp_fpga.nco_counter_send_conf("/dev/mod_out2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_mod_out2_nco.get_value())), 40, int(self.sb_poff_mod_out2_nco.get_value()), int(self.cb_pinc_mod_out2_nco.get_value()), int(value=="true"))
		self.cb_poff_mod_out2_nco.set_value(int(value=="true"))

	def sd_ch1_mod_out_ampl_changed(self, widget, value):
		vals.ch1_mod_out_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_out_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_out_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_out_ampl", liboscimp_fpga.CHANA, int(value))
		self.sb_ch1_mod_out_ampl.set_value(int(value))

	def sb_ch1_mod_out_ampl_changed(self, widget, value):
		vals.ch1_mod_out_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_out_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_out_ampl ch1", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_out_ampl", liboscimp_fpga.CHANA, int(value))
		self.sd_ch1_mod_out_ampl.set_value(int(float(value)))

	def sd_ch2_mod_out_ampl_changed(self, widget, value):
		vals.ch2_mod_out_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_out_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_out_ampl ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_out_ampl", liboscimp_fpga.CHANB, int(value))
		self.sb_ch2_mod_out_ampl.set_value(int(value))

	def sb_ch2_mod_out_ampl_changed(self, widget, value):
		vals.ch2_mod_out_ampl=value
		liboscimp_fpga.axi_to_dac_conf_enable("/dev/mod_out_ampl", liboscimp_fpga.BOTH_ALWAYS_HIGH)
		print("/dev/mod_out_ampl ch2", int(value))
		liboscimp_fpga.axi_to_dac_set_chan("/dev/mod_out_ampl", liboscimp_fpga.CHANB, int(value))
		self.sd_ch2_mod_out_ampl.set_value(int(float(value)))

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
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.SETPOINT, int(value))
		self.sb_sp_pid1.set_value(int(value))

	def sb_sp_pid1_changed(self, widget, value):
		vals.sp_pid1=value
		print("/dev/pid1/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.SETPOINT, int(value))
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

	def sd_kp_pid2_changed(self, widget, value):
		vals.kp_pid2=value
		print("/dev/pid2/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid2", liboscimp_fpga.KP, int(value))
		self.sb_kp_pid2.set_value(int(value))

	def sb_kp_pid2_changed(self, widget, value):
		vals.kp_pid2=value
		print("/dev/pid2/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid2", liboscimp_fpga.KP, int(value))
		self.sd_kp_pid2.set_value(int(float(value)))

	def sd_ki_pid2_changed(self, widget, value):
		vals.ki_pid2=value
		print("/dev/pid2/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid2", liboscimp_fpga.KI, int(value))
		self.sb_ki_pid2.set_value(int(value))

	def sb_ki_pid2_changed(self, widget, value):
		vals.ki_pid2=value
		print("/dev/pid2/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid2", liboscimp_fpga.KI, int(value))
		self.sd_ki_pid2.set_value(int(float(value)))

	def cb_rst_int_pid2_changed(self, widget, value):
		vals.rst_int_pid2=value
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pid2", 1)
		print("/dev/pid2/rst_int", int(value=="true"))
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pid2", int(value=="true"))
		self.cb_rst_int_pid2.set_value(int(value=="true"))

	def sd_sp_pid2_changed(self, widget, value):
		vals.sp_pid2=value
		print("/dev/pid2/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid2", liboscimp_fpga.SETPOINT, int(value))
		self.sb_sp_pid2.set_value(int(value))

	def sb_sp_pid2_changed(self, widget, value):
		vals.sp_pid2=value
		print("/dev/pid2/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid2", liboscimp_fpga.SETPOINT, int(value))
		self.sd_sp_pid2.set_value(int(float(value)))

	def sd_sign_pid2_changed(self, widget, value):
		vals.sign_pid2=value
		print("/dev/pid2/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pid2", int(value))
		self.sb_sign_pid2.set_value(int(value))

	def sb_sign_pid2_changed(self, widget, value):
		vals.sign_pid2=value
		print("/dev/pid2/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pid2", int(value))
		self.sd_sign_pid2.set_value(int(float(value)))

	def sd_pwm_offset_changed(self, widget, value):
		vals.pwm_offset=value
		print("/dev/pwm_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/pwm_offset", int(value))
		self.sb_pwm_offset.set_value(int(value))

	def sb_pwm_offset_changed(self, widget, value):
		vals.pwm_offset=value
		print("/dev/pwm_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/pwm_offset", int(value))
		self.sd_pwm_offset.set_value(int(float(value)))

	def sd_shift_dyn_changed(self, widget, value):
		vals.shift_dyn=value
		print("/dev/shift_dyn", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sb_shift_dyn.set_value(int(value))

	def sb_shift_dyn_changed(self, widget, value):
		vals.shift_dyn=value
		print("/dev/shift_dyn", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sd_shift_dyn.set_value(int(float(value)))

start(MyApp, address="0.0.0.0", port=80, title="demod_pid1_pidpwm3_vco_only2_webserver")
