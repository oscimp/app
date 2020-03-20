#!/usr/bin/env python

import liboscimp_fpga
import time, struct, ctypes, sys, threading, os, math
import remi.gui as gui
from remi import start, App

import temp_ctrl

liboscimp_fpga.axi_to_dac_set_chan("/dev/proc_out", liboscimp_fpga.CHANA, int(0))

os.system('./zmq_data2ram_proc.py &')
os.system('./zmq_data2ram_adc2.py &')
os.system('./zmq_data2ram_fast.py &')
os.system('./zmq_data2ram_slow.py &')
os.system('./temp_acq.py &')

tctrl = temp_ctrl.TempCtrl(kps=[int(0), int(0)],
                           kis=[int(0), int(0)],
                           omaxs=[8191, 2**30],
                           imaxs=[int(2**36), int(2**36)],
                           oscales=[10,16])
in_ = 0
t = 0
t0 = 0
out= 0

class IniVar:
    def __init__(vars):
        vars.tempo = 500
        vars.t0 = 0
        vars.t_err = 0
Vars=IniVar()

fd=open('/sys/bus/iio/devices/iio:device1/in_voltage-voltage_scale', 'r')
scale=float(fd.read().split()[0])
if scale==0:
        print("erreur d'ouverture\n")
fd.close;

class MyApp(App):
	def __init__(self, *args):
		super(MyApp, self).__init__(*args)

	def main(self):
		self.w = gui.VBox()

		self.hbox_adc1_offset = gui.HBox(margin="10px")
		self.lb_adc1_offset = gui.Label("/dev/adc1_offset", width="20%", margin="10px")
		self.sd_adc1_offset = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_adc1_offset.set_oninput_listener(self.sd_adc1_offset_changed)
		self.sb_adc1_offset = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_adc1_offset.set_on_change_listener(self.sb_adc1_offset_changed)
		self.sd_adc1_offset_changed(self.sd_adc1_offset, self.sd_adc1_offset.get_value())
		self.hbox_adc1_offset.append(self.lb_adc1_offset)
		self.hbox_adc1_offset.append(self.sd_adc1_offset)
		self.hbox_adc1_offset.append(self.sb_adc1_offset)
		self.w.append(self.hbox_adc1_offset)

		self.hbox_adc2_offset = gui.HBox(margin="10px")
		self.lb_adc2_offset = gui.Label("/dev/adc2_offset", width="20%", margin="10px")
		self.sd_adc2_offset = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_adc2_offset.set_oninput_listener(self.sd_adc2_offset_changed)
		self.sb_adc2_offset = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_adc2_offset.set_on_change_listener(self.sb_adc2_offset_changed)
		self.sd_adc2_offset_changed(self.sd_adc2_offset, self.sd_adc2_offset.get_value())
		self.hbox_adc2_offset.append(self.lb_adc2_offset)
		self.hbox_adc2_offset.append(self.sd_adc2_offset)
		self.hbox_adc2_offset.append(self.sb_adc2_offset)
		self.w.append(self.hbox_adc2_offset)

		self.hbox_dac1_offset = gui.HBox(margin="10px")
		self.lb_dac1_offset = gui.Label("/dev/dac1_offset", width="20%", margin="10px")
		self.sd_dac1_offset = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_dac1_offset.set_oninput_listener(self.sd_dac1_offset_changed)
		self.sb_dac1_offset = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_dac1_offset.set_on_change_listener(self.sb_dac1_offset_changed)
		self.sd_dac1_offset_changed(self.sd_dac1_offset, self.sd_dac1_offset.get_value())
		self.hbox_dac1_offset.append(self.lb_dac1_offset)
		self.hbox_dac1_offset.append(self.sd_dac1_offset)
		self.hbox_dac1_offset.append(self.sb_dac1_offset)
		self.w.append(self.hbox_dac1_offset)

		self.hbox_dac2_offset = gui.HBox(margin="10px")
		self.lb_dac2_offset = gui.Label("/dev/dac2_offset", width="20%", margin="10px")
		self.sd_dac2_offset = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_dac2_offset.set_oninput_listener(self.sd_dac2_offset_changed)
		self.sb_dac2_offset = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_dac2_offset.set_on_change_listener(self.sb_dac2_offset_changed)
		self.sd_dac2_offset_changed(self.sd_dac2_offset, self.sd_dac2_offset.get_value())
		self.hbox_dac2_offset.append(self.lb_dac2_offset)
		self.hbox_dac2_offset.append(self.sd_dac2_offset)
		self.hbox_dac2_offset.append(self.sb_dac2_offset)
		self.w.append(self.hbox_dac2_offset)

		self.hbox_demod1_nco = gui.HBox(margin="10px")
		self.lb_demod1_nco = gui.Label("/dev/demod1_nco", width="20%", margin="10px")
		self.sd_pinc_demod1_nco = gui.Slider(0, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_demod1_nco.set_oninput_listener(self.sd_pinc_demod1_nco_changed)
		self.sb_pinc_demod1_nco = gui.SpinBox(0, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_demod1_nco.set_on_change_listener(self.sb_pinc_demod1_nco_changed)
		self.sd_poff_demod1_nco = gui.Slider(0, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_demod1_nco.set_oninput_listener(self.sd_poff_demod1_nco_changed)
		self.sb_poff_demod1_nco = gui.SpinBox(0, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_demod1_nco.set_on_change_listener(self.sb_poff_demod1_nco_changed)
		self.cb_pinc_demod1_nco = gui.CheckBoxLabel("pinc", True, width="5%", margin="10px")
		self.cb_pinc_demod1_nco.set_on_change_listener(self.cb_demod1_nco_changed)
		self.cb_poff_demod1_nco = gui.CheckBoxLabel("poff", True, width="5%", margin="10px")
		self.cb_poff_demod1_nco.set_on_change_listener(self.cb_demod1_nco_changed)
		self.hbox_demod1_nco.append(self.lb_demod1_nco)
		self.hbox_demod1_nco.append(self.sd_pinc_demod1_nco)
		self.hbox_demod1_nco.append(self.sb_pinc_demod1_nco)
		self.hbox_demod1_nco.append(self.sd_poff_demod1_nco)
		self.hbox_demod1_nco.append(self.sb_poff_demod1_nco)
		self.hbox_demod1_nco.append(self.cb_pinc_demod1_nco)
		self.hbox_demod1_nco.append(self.cb_poff_demod1_nco)
		self.w.append(self.hbox_demod1_nco)

		self.hbox_demod2_nco = gui.HBox(margin="10px")
		self.lb_demod2_nco = gui.Label("/dev/demod2_nco", width="20%", margin="10px")
		self.sd_pinc_demod2_nco = gui.Slider(0, 0, 62500000, 1, width="25%", margin="10px")
		self.sd_pinc_demod2_nco.set_oninput_listener(self.sd_pinc_demod2_nco_changed)
		self.sb_pinc_demod2_nco = gui.SpinBox(0, 0, 62500000, 0.02, width="10%", margin="10px")
		self.sb_pinc_demod2_nco.set_on_change_listener(self.sb_pinc_demod2_nco_changed)
		self.sd_poff_demod2_nco = gui.Slider(0, -8192, 8191, 1, width="25%", margin="10px")
		self.sd_poff_demod2_nco.set_oninput_listener(self.sd_poff_demod2_nco_changed)
		self.sb_poff_demod2_nco = gui.SpinBox(0, -8192, 8191, 1, width="10%", margin="10px")
		self.sb_poff_demod2_nco.set_on_change_listener(self.sb_poff_demod2_nco_changed)
		self.cb_pinc_demod2_nco = gui.CheckBoxLabel("pinc", True, width="5%", margin="10px")
		self.cb_pinc_demod2_nco.set_on_change_listener(self.cb_demod2_nco_changed)
		self.cb_poff_demod2_nco = gui.CheckBoxLabel("poff", True, width="5%", margin="10px")
		self.cb_poff_demod2_nco.set_on_change_listener(self.cb_demod2_nco_changed)
		self.hbox_demod2_nco.append(self.lb_demod2_nco)
		self.hbox_demod2_nco.append(self.sd_pinc_demod2_nco)
		self.hbox_demod2_nco.append(self.sb_pinc_demod2_nco)
		self.hbox_demod2_nco.append(self.sd_poff_demod2_nco)
		self.hbox_demod2_nco.append(self.sb_poff_demod2_nco)
		self.hbox_demod2_nco.append(self.cb_pinc_demod2_nco)
		self.hbox_demod2_nco.append(self.cb_poff_demod2_nco)
		self.w.append(self.hbox_demod2_nco)

		self.hbox_kp_pid1 = gui.HBox(margin="10px")
		self.lb_kp_pid1 = gui.Label("/dev/pid1/kp", width="20%", margin="10px")
		self.sd_kp_pid1 = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_kp_pid1.set_oninput_listener(self.sd_kp_pid1_changed)
		self.sb_kp_pid1 = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_kp_pid1.set_on_change_listener(self.sb_kp_pid1_changed)
		self.sd_kp_pid1_changed(self.sd_kp_pid1, self.sd_kp_pid1.get_value())
		self.hbox_kp_pid1.append(self.lb_kp_pid1)
		self.hbox_kp_pid1.append(self.sd_kp_pid1)
		self.hbox_kp_pid1.append(self.sb_kp_pid1)
		self.w.append(self.hbox_kp_pid1)

		self.hbox_ki_pid1 = gui.HBox(margin="10px")
		self.lb_ki_pid1 = gui.Label("/dev/pid1/ki", width="20%", margin="10px")
		self.sd_ki_pid1 = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pid1.set_oninput_listener(self.sd_ki_pid1_changed)
		self.sb_ki_pid1 = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ki_pid1.set_on_change_listener(self.sb_ki_pid1_changed)
		self.sd_ki_pid1_changed(self.sd_ki_pid1, self.sd_ki_pid1.get_value())
		self.cb_rst_int_pid1 = gui.CheckBoxLabel("rst_int", True, width="5%", margin="10px")
		self.cb_rst_int_pid1.set_on_change_listener(self.cb_rst_int_pid1_changed)
		self.hbox_ki_pid1.append(self.lb_ki_pid1)
		self.hbox_ki_pid1.append(self.sd_ki_pid1)
		self.hbox_ki_pid1.append(self.sb_ki_pid1)
		self.hbox_ki_pid1.append(self.cb_rst_int_pid1)
		self.w.append(self.hbox_ki_pid1)

		self.hbox_sp_pid1 = gui.HBox(margin="10px")
		self.lb_sp_pid1 = gui.Label("/dev/pid1/setpoint", width="20%", margin="10px")
		self.sd_sp_pid1 = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sp_pid1.set_oninput_listener(self.sd_sp_pid1_changed)
		self.sb_sp_pid1 = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sp_pid1.set_on_change_listener(self.sb_sp_pid1_changed)
		self.sd_sp_pid1_changed(self.sd_sp_pid1, self.sd_sp_pid1.get_value())
		self.hbox_sp_pid1.append(self.lb_sp_pid1)
		self.hbox_sp_pid1.append(self.sd_sp_pid1)
		self.hbox_sp_pid1.append(self.sb_sp_pid1)
		self.w.append(self.hbox_sp_pid1)

		self.hbox_sign_pid1 = gui.HBox(margin="10px")
		self.lb_sign_pid1 = gui.Label("/dev/pid1/sign", width="20%", margin="10px")
		self.sd_sign_pid1 = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_sign_pid1.set_oninput_listener(self.sd_sign_pid1_changed)
		self.sb_sign_pid1 = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_sign_pid1.set_on_change_listener(self.sb_sign_pid1_changed)
		self.sd_sign_pid1_changed(self.sd_sign_pid1, self.sd_sign_pid1.get_value())
		self.hbox_sign_pid1.append(self.lb_sign_pid1)
		self.hbox_sign_pid1.append(self.sd_sign_pid1)
		self.hbox_sign_pid1.append(self.sb_sign_pid1)
		self.w.append(self.hbox_sign_pid1)

		self.hbox_pid2_kp = gui.HBox(margin="10px")
		self.lb_pid2_kp = gui.Label("pid2_kp", width="20%", margin="10px")
		self.sd_pid2_kp = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_pid2_kp.set_oninput_listener(self.sd_pid2_kp_changed)
		self.sb_pid2_kp = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_pid2_kp.set_on_change_listener(self.sb_pid2_kp_changed)
		self.sd_pid2_kp_changed(self.sd_pid2_kp, self.sd_pid2_kp.get_value())
		self.hbox_pid2_kp.append(self.lb_pid2_kp)
		self.hbox_pid2_kp.append(self.sd_pid2_kp)
		self.hbox_pid2_kp.append(self.sb_pid2_kp)
		self.w.append(self.hbox_pid2_kp)

		self.hbox_ki_pid2 = gui.HBox(margin="10px")
		self.lb_ki_pid2 = gui.Label("/dev/pid2_ki", width="20%", margin="10px")
		self.sd_ki_pid2 = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pid2.set_oninput_listener(self.sd_ki_pid2_changed)
		self.sb_ki_pid2 = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ki_pid2.set_on_change_listener(self.sb_ki_pid2_changed)
		self.sd_ki_pid2_changed(self.sd_ki_pid2, self.sd_ki_pid2.get_value())
		self.cb_rst_int_pid2 = gui.CheckBoxLabel("rst_int", True, width="5%", margin="10px")
		self.cb_rst_int_pid2.set_on_change_listener(self.cb_rst_int_pid2_changed)
		self.hbox_ki_pid2.append(self.lb_ki_pid2)
		self.hbox_ki_pid2.append(self.sd_ki_pid2)
		self.hbox_ki_pid2.append(self.sb_ki_pid2)
		self.hbox_ki_pid2.append(self.cb_rst_int_pid2)
		self.w.append(self.hbox_ki_pid2)

		self.hbox_pid3_kp = gui.HBox(margin="10px")
		self.lb_pid3_kp = gui.Label("pid3_kp", width="20%", margin="10px")
		self.sd_pid3_kp = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_pid3_kp.set_oninput_listener(self.sd_pid3_kp_changed)
		self.sb_pid3_kp = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_pid3_kp.set_on_change_listener(self.sb_pid3_kp_changed)
		self.sd_pid3_kp_changed(self.sd_pid3_kp, self.sd_pid3_kp.get_value())
		self.hbox_pid3_kp.append(self.lb_pid3_kp)
		self.hbox_pid3_kp.append(self.sd_pid3_kp)
		self.hbox_pid3_kp.append(self.sb_pid3_kp)
		self.w.append(self.hbox_pid3_kp)

		self.hbox_ki_pid3 = gui.HBox(margin="10px")
		self.lb_ki_pid3 = gui.Label("/dev/pid3_ki", width="20%", margin="10px")
		self.sd_ki_pid3 = gui.Slider(0, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_ki_pid3.set_oninput_listener(self.sd_ki_pid3_changed)
		self.sb_ki_pid3 = gui.SpinBox(0, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_ki_pid3.set_on_change_listener(self.sb_ki_pid3_changed)
		self.sd_ki_pid3_changed(self.sd_ki_pid3, self.sd_ki_pid3.get_value())
		self.cb_rst_int_pid3 = gui.CheckBoxLabel("rst_int", True, width="5%", margin="10px")
		self.cb_rst_int_pid3.set_on_change_listener(self.cb_rst_int_pid3_changed)
		self.hbox_ki_pid3.append(self.lb_ki_pid3)
		self.hbox_ki_pid3.append(self.sd_ki_pid3)
		self.hbox_ki_pid3.append(self.sb_ki_pid3)
		self.hbox_ki_pid3.append(self.cb_rst_int_pid3)
		self.w.append(self.hbox_ki_pid3)

		self.hbox_pid3_set_point = gui.HBox(margin="10px")
		self.lb_pid3_set_point = gui.Label("pid3_set_point", width="20%", margin="10px")
		self.sd_pid3_set_point = gui.Slider(22, 15, 30, 0.01, width="60%", margin="10px")
		self.sd_pid3_set_point.set_oninput_listener(self.sd_pid3_set_point_changed)
		self.sb_pid3_set_point = gui.SpinBox(22, 15, 30, 0.01, width="20%", margin="10px")
		self.sb_pid3_set_point.set_on_change_listener(self.sb_pid3_set_point_changed)
		self.sd_pid3_set_point_changed(self.sd_pid3_set_point, self.sd_pid3_set_point.get_value())
		self.hbox_pid3_set_point.append(self.lb_pid3_set_point)
		self.hbox_pid3_set_point.append(self.sd_pid3_set_point)
		self.hbox_pid3_set_point.append(self.sb_pid3_set_point)
		self.w.append(self.hbox_pid3_set_point)

		self.hbox_shift_dyn_I = gui.HBox(margin="10px")
		self.lb_shift_dyn_I = gui.Label("/dev/shift_dyn_I", width="20%", margin="10px")
		self.sd_shift_dyn_I = gui.Slider(9, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_shift_dyn_I.set_oninput_listener(self.sd_shift_dyn_I_changed)
		self.sb_shift_dyn_I = gui.SpinBox(9, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_shift_dyn_I.set_on_change_listener(self.sb_shift_dyn_I_changed)
		self.sd_shift_dyn_I_changed(self.sd_shift_dyn_I, self.sd_shift_dyn_I.get_value())
		self.hbox_shift_dyn_I.append(self.lb_shift_dyn_I)
		self.hbox_shift_dyn_I.append(self.sd_shift_dyn_I)
		self.hbox_shift_dyn_I.append(self.sb_shift_dyn_I)
		self.w.append(self.hbox_shift_dyn_I)

		self.hbox_shift_dyn_Q = gui.HBox(margin="10px")
		self.lb_shift_dyn_Q = gui.Label("/dev/shift_dyn_Q", width="20%", margin="10px")
		self.sd_shift_dyn_Q = gui.Slider(9, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_shift_dyn_Q.set_oninput_listener(self.sd_shift_dyn_Q_changed)
		self.sb_shift_dyn_Q = gui.SpinBox(9, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_shift_dyn_Q.set_on_change_listener(self.sb_shift_dyn_Q_changed)
		self.sd_shift_dyn_Q_changed(self.sd_shift_dyn_Q, self.sd_shift_dyn_Q.get_value())
		self.hbox_shift_dyn_Q.append(self.lb_shift_dyn_Q)
		self.hbox_shift_dyn_Q.append(self.sd_shift_dyn_Q)
		self.hbox_shift_dyn_Q.append(self.sb_shift_dyn_Q)
		self.w.append(self.hbox_shift_dyn_Q)

		self.hbox_shift_dyn_2 = gui.HBox(margin="10px")
		self.lb_shift_dyn_2 = gui.Label("/dev/shift_dyn_2", width="20%", margin="10px")
		self.sd_shift_dyn_2 = gui.Slider(9, -8192, 8191, 1, width="60%", margin="10px")
		self.sd_shift_dyn_2.set_oninput_listener(self.sd_shift_dyn_2_changed)
		self.sb_shift_dyn_2 = gui.SpinBox(9, -8192, 8191, 1, width="20%", margin="10px")
		self.sb_shift_dyn_2.set_on_change_listener(self.sb_shift_dyn_2_changed)
		self.sd_shift_dyn_2_changed(self.sd_shift_dyn_2, self.sd_shift_dyn_2.get_value())
		self.hbox_shift_dyn_2.append(self.lb_shift_dyn_2)
		self.hbox_shift_dyn_2.append(self.sd_shift_dyn_2)
		self.hbox_shift_dyn_2.append(self.sb_shift_dyn_2)
		self.w.append(self.hbox_shift_dyn_2)

		self.hbox_tempo = gui.HBox(margin="10px")
		self.lb_tempo = gui.Label("tempo", width="20%", margin="10px")
		self.sd_tempo = gui.Slider(500, 50, 10000, 1, width="60%", margin="10px")
		self.sd_tempo.set_oninput_listener(self.sd_tempo_changed)
		self.sb_tempo = gui.SpinBox(500, 50, 10000, 1, width="20%", margin="10px")
		self.sb_tempo.set_on_change_listener(self.sb_tempo_changed)
		self.sd_tempo_changed(self.sd_tempo, self.sd_tempo.get_value())
		self.hbox_tempo.append(self.lb_tempo)
		self.hbox_tempo.append(self.sd_tempo)
		self.hbox_tempo.append(self.sb_tempo)
		self.w.append(self.hbox_tempo)

		self.hbox_switchIQ = gui.HBox(margin="10px")
		self.cb_switchIQ = gui.CheckBoxLabel("switchIQ", True, width="5%", margin="10px")
		self.cb_switchIQ.set_on_change_listener(self.cb_switchIQ_changed)
		self.hbox_switchIQ.append(self.cb_switchIQ)
		self.w.append(self.hbox_switchIQ)

		return self.w

	def sd_adc1_offset_changed(self, widget, value):
		print("/dev/adc1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/adc1_offset", int(value))
		self.sb_adc1_offset.set_value(int(value))

	def sb_adc1_offset_changed(self, widget, value):
		print("/dev/adc1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/adc1_offset", int(value))
		self.sd_adc1_offset.set_value(int(float(value)))

	def sd_adc2_offset_changed(self, widget, value):
		print("/dev/adc2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/adc2_offset", int(value))
		self.sb_adc2_offset.set_value(int(value))

	def sb_adc2_offset_changed(self, widget, value):
		print("/dev/adc2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/adc2_offset", int(value))
		self.sd_adc2_offset.set_value(int(float(value)))

	def sd_dac1_offset_changed(self, widget, value):
		print("/dev/dac1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac1_offset", int(value))
		self.sb_dac1_offset.set_value(int(value))

	def sb_dac1_offset_changed(self, widget, value):
		print("/dev/dac1_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac1_offset", int(value))
		self.sd_dac1_offset.set_value(int(float(value)))

	def sd_dac2_offset_changed(self, widget, value):
		print("/dev/dac2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac2_offset", int(value))
		self.sb_dac2_offset.set_value(int(value))

	def sb_dac2_offset_changed(self, widget, value):
		print("/dev/dac2_offset", int(value))
		liboscimp_fpga.add_const_set_offset("/dev/dac2_offset", int(value))
		self.sd_dac2_offset.set_value(int(float(value)))

	def sd_pinc_demod1_nco_changed(self, widget, value):
		print("/dev/demod1_nco", 125000000, int(value), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		self.sb_pinc_demod1_nco.set_value(int(value))

	def sb_pinc_demod1_nco_changed(self, widget, value):
		print("/dev/demod1_nco", 125000000, value, 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		self.sd_pinc_demod1_nco.set_value(value)

	def sd_poff_demod1_nco_changed(self, widget, value):
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		self.sb_poff_demod1_nco.set_value(value)

	def sb_poff_demod1_nco_changed(self, widget, value):
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(value), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		self.sd_poff_demod1_nco.set_value(value)

	def cb_demod1_nco_changed(self, widget, value):
		print("/dev/demod1_nco", 125000000, self.sb_pinc_demod1_nco.get_value(), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod1_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod1_nco.get_value())), 40, int(self.sb_poff_demod1_nco.get_value()), int(self.cb_pinc_demod1_nco.get_value()), int(self.cb_poff_demod1_nco.get_value()))

	def sd_pinc_demod2_nco_changed(self, widget, value):
		print("/dev/demod2_nco", 125000000, int(value), 40, int(self.sb_poff_demod2_nco.get_value()), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod2_nco".encode("utf-8"), 125000000, ctypes.c_double(int(value)), 40, int(self.sb_poff_demod2_nco.get_value()), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		self.sb_pinc_demod2_nco.set_value(int(value))

	def sb_pinc_demod2_nco_changed(self, widget, value):
		print("/dev/demod2_nco", 125000000, value, 40, int(self.sb_poff_demod2_nco.get_value()), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(value)), 40, int(self.sb_poff_demod2_nco.get_value()), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		self.sd_pinc_demod2_nco.set_value(value)

	def sd_poff_demod2_nco_changed(self, widget, value):
		print("/dev/demod2_nco", 125000000, self.sb_pinc_demod2_nco.get_value(), 40, int(value), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod2_nco.get_value())), 40, int(value), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		self.sb_poff_demod2_nco.set_value(value)

	def sb_poff_demod2_nco_changed(self, widget, value):
		print("/dev/demod2_nco", 125000000, self.sb_pinc_demod2_nco.get_value(), 40, int(value), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod2_nco.get_value())), 40, int(value), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		self.sd_poff_demod2_nco.set_value(value)

	def cb_demod2_nco_changed(self, widget, value):
		print("/dev/demod2_nco", 125000000, self.sb_pinc_demod2_nco.get_value(), 40, int(self.sb_poff_demod2_nco.get_value()), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))
		liboscimp_fpga.nco_counter_send_conf("/dev/demod2_nco".encode("utf-8"), 125000000, ctypes.c_double(float(self.sb_pinc_demod2_nco.get_value())), 40, int(self.sb_poff_demod2_nco.get_value()), int(self.cb_pinc_demod2_nco.get_value()), int(self.cb_poff_demod2_nco.get_value()))

	def sd_kp_pid1_changed(self, widget, value):
		print("/dev/pid1/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KP, int(value))
		self.sb_kp_pid1.set_value(int(value))

	def sb_kp_pid1_changed(self, widget, value):
		print("/dev/pid1/kp", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KP, int(value))
		self.sd_kp_pid1.set_value(int(float(value)))

	def sd_ki_pid1_changed(self, widget, value):
		print("/dev/pid1/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KI, int(value))
		self.sb_ki_pid1.set_value(int(value))

	def sb_ki_pid1_changed(self, widget, value):
		print("/dev/pid1/ki", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.KI, int(value))
		self.sd_ki_pid1.set_value(int(float(value)))

	def cb_rst_int_pid1_changed(self, widget, value):
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pid1", 1)
		print("/dev/pid1/rst_int", int(self.cb_rst_int_pid1.get_value()))
		liboscimp_fpga.pidv3_axi_set_int_rst("/dev/pid1", int(self.cb_rst_int_pid1.get_value()))

	def sd_sp_pid1_changed(self, widget, value):
		print("/dev/pid1/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.SETPOINT, int(value))
		self.sb_sp_pid1.set_value(int(value))

	def sb_sp_pid1_changed(self, widget, value):
		print("/dev/pid1/setpoint", int(value))
		liboscimp_fpga.pidv3_axi_set("/dev/pid1", liboscimp_fpga.SETPOINT, int(value))
		self.sd_sp_pid1.set_value(int(float(value)))

	def sd_sign_pid1_changed(self, widget, value):
		print("/dev/pid1/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pid1", int(value))
		self.sb_sign_pid1.set_value(int(value))

	def sb_sign_pid1_changed(self, widget, value):
		print("/dev/pid1/sign", int(value))
		liboscimp_fpga.pidv3_axi_set_sign("/dev/pid1", int(value))
		self.sd_sign_pid1.set_value(int(float(value)))

	def sd_pid2_kp_changed(self, widget, value):
		self.sb_pid2_kp.set_value(int(value))
		print("pid2_kp",value)
		tctrl.pid2.kp = int(value)

	def sb_pid2_kp_changed(self, widget, value):
		print("pid2_kp",value)
		tctrl.pid2.kp = int(value)
		self.sd_pid2_kp.set_value(int(float(value)))

	def sd_ki_pid2_changed(self, widget, value):
		self.sb_ki_pid2.set_value(int(value))
		tctrl.pid2.ki = int(value)
		print("pid2_ki",value)

	def sb_ki_pid2_changed(self, widget, value):
		self.sd_ki_pid2.set_value(int(float(value)))
		tctrl.pid2.ki = int(value)
		print("pid2_ki",value)

	def cb_rst_int_pid2_changed(self, widget, value):
		tctrl.pid2.enable_int(True)
		self.cb_rst_int_pid2.get_value()
		print("pid2_rst_int", int(self.cb_rst_int_pid2.get_value()))
		if (int(self.cb_rst_int_pid2.get_value()) % 2) == 1 :
			tctrl.pid2.enable_int(False)
		else:
			tctrl.pid2.enable_int(True)

	def sd_pid3_kp_changed(self, widget, value):
		self.sb_pid3_kp.set_value(int(value))
		tctrl.pid1.kp = int(value)
		print("pid3_kp",value)

	def sb_pid3_kp_changed(self, widget, value):
		tctrl.pid1.kp = int(value)
		self.sd_pid3_kp.set_value(int(float(value)))
		print("pid3_kp",value)

	def sd_ki_pid3_changed(self, widget, value):
		self.sb_ki_pid3.set_value(int(value))
		tctrl.pid1.ki = int(value)
		print("pid3_ki",value)

	def sb_ki_pid3_changed(self, widget, value):
		self.sd_ki_pid3.set_value(int(float(value)))
		tctrl.pid1.ki = int(value)
		print("pid3_ki",value)

	def cb_rst_int_pid3_changed(self, widget, value):
		tctrl.pid1.enable_int(True)
		self.cb_rst_int_pid3.get_value()
		print("pid3_rst_int", int(self.cb_rst_int_pid3.get_value()))
		if (int(self.cb_rst_int_pid3.get_value()) % 2) == 1 :
			tctrl.pid1.enable_int(False)
		else:
			tctrl.pid1.enable_int(True)

	def sd_pid3_set_point_changed(self, widget, value):
		A=0.0012146
		B=0.00021922
		C=0.00000015244
		x=(1/C)*(A-1/(float(value)+273.15))
		y=((B/3/C)**3+(x/2)**2)**0.5
		vint=math.exp(pow((y-(x/2)),1/3.0)-(pow((y+(x/2)),1/3.0)))*0.112/scale
		Vars.t0 = int(vint)
		print("pid3_set_point",value)
		self.sb_pid3_set_point.set_value(float(value))

	def sb_pid3_set_point_changed(self, widget, value):
		A=0.0012146
		B=0.00021922
		C=0.00000015244
		x=(1/C)*(A-1/(float(value)+273.15))
		y=((B/3/C)**3+(x/2)**2)**0.5
		vint=math.exp(pow((y-(x/2)),1/3.0)-(pow((y+(x/2)),1/3.0)))*0.112/scale
		self.sd_pid3_set_point.set_value(float(value))
		print("pid3_set_point",value)
		Vars.t0 = int(vint)

	def sd_shift_dyn_I_changed(self, widget, value):
		print("/dev/shift_dyn_I", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn_I".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sb_shift_dyn_I.set_value(int(value))

	def sb_shift_dyn_I_changed(self, widget, value):
		print("/dev/shift_dyn_I", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn_I".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sd_shift_dyn_I.set_value(int(float(value)))

	def sd_shift_dyn_Q_changed(self, widget, value):
		print("/dev/shift_dyn_Q", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn_Q".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sb_shift_dyn_Q.set_value(int(value))

	def sb_shift_dyn_Q_changed(self, widget, value):
		print("/dev/shift_dyn_Q", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn_Q".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sd_shift_dyn_Q.set_value(int(float(value)))

	def sd_shift_dyn_2_changed(self, widget, value):
		print("/dev/shift_dyn_2", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn_2".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sb_shift_dyn_2.set_value(int(value))

	def sb_shift_dyn_2_changed(self, widget, value):
		print("/dev/shift_dyn_2", ctypes.c_int32(int(value)))
		liboscimp_fpga.shifter_set("/dev/shift_dyn_2".encode("utf-8"), ctypes.c_int32(int(value)))
		self.sd_shift_dyn_2.set_value(int(float(value)))

	def sd_tempo_changed(self, widget, value):
		self.sb_tempo.set_value(int(value))
		print("tempo",int(value))
		Vars.tempo = int(value)

	def sb_tempo_changed(self, widget, value):
		Vars.tempo = int(value)
		print("tempo",int(value))
		self.sd_tempo.set_value(int(float(value)))

	def cb_switchIQ_changed(self, widget, value):
		liboscimp_fpga.switch_send_conf("/dev/swichIQ".encode("utf-8"), 1)
		print("/dev/switchIQ", int(self.cb_switchIQ.get_value()))
		liboscimp_fpga.switch_send_conf("/dev/swichIQ".encode("utf-8"), int(self.cb_switchIQ.get_value()))

def start_server():
	start(MyApp, address="0.0.0.0", port=80, title="demod_pid_only1_adc_ram_dac2_webserver")

threading.Thread(target=start_server).start()

fe=open('/sys/bus/iio/devices/iio:device1/in_voltage0-voltage1_raw', 'r')

def pid_compute():
	with open("/dev/data_proc", "rb") as fd:
		in_recv = fd.read(8192)
		in_recv = struct.unpack('4096h'.encode('utf-8'), in_recv)
		in_ = int(sum(in_recv[0::2])/len(in_recv[0::2]))
	print("IN_dt =",in_)

	try:
		t_inte=fe.read()
	except IOError:
		print("IO error!")
		t_inte=Vars.t_err
	fe.seek(0);
	Vars.t_err=t_inte
	t=int(t_inte.split()[0])
	R=t/0.112*scale
	if R > 0:
		ntc10k=1/(0.0012146+0.00021922*math.log(R)+0.00000015244*math.log(R)**3)-273.15
	else:
		ntc10k=0
		print("Error: bad voltage value") 
	print("IN_t =", ntc10k, "°C")
	[out,cor_pid2]=tctrl.compute(in_, t, Vars.t0)
	liboscimp_fpga.axi_to_dac_set_chan("/dev/proc_out", liboscimp_fpga.CHANA, int(out))
	print("CORR_PID2 =", cor_pid2)
	print("OUT =",out, "\n")
	pid_compute.thread = threading.Timer(Vars.tempo*10**-3, pid_compute)
	pid_compute.thread.start()

pid_compute()
