#!/usr/bin/env python3.9

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
	os.remove('launch_my_design.sh')
except:
	pass

with open('launch_my_design.sh', 'a') as f:
	f.write('#### find the local IP\n')
	f.write('MY_IP=$(/sbin/ifconfig eth0 | grep "inet ad" | cut -f2 -d: | awk "{print $1}")\n\n')
	f.write('#### mount the remote nfs folder and go inside it\n')
	f.write('mount /usr/local/\n\n')
	f.write('cd /usr/local/%s/bin/\n\n'%name)
	f.write('#### flash fpga\n')
	f.write('sh %s_us.sh\n\n'%name)
	f.write('#### start webserver\n')
	f.write('screen -dmS webserver ./%s_webserver.py\n'%name)
	f.write('sleep 2\n')
	f.write('wget $MY_IP\n\n')
	f.write('#### your design applications\n')

	for elem in board_driver_array:
		if elem[0] in ['dataComplex_to_ram', 'dataReal_to_ram'] :
			f.write('#screen -dmS /dev/%s ./my_zmq_data2ram_script.py\n'%elem[1])

		if elem[0] in ['firComplex', 'firReal'] :
			f.write('#./my_fir_coeff_loader_script.py /dev/%s my_fir_coeff_file.dat\n'%elem[1])

		if elem[0] in ['fft'] :
			f.write('#./my_fft_coeff_loader_script.py /dev/%s my_fft_coeff_file_re.dat my_fft_coeff_file_im.dat\n'%elem[1])

		if elem[0] in ['windowReal'] :
			f.write('#./my_window_coeff_loader_script.py /dev/%s my_window_coeff_file.dat\n'%elem[1])

print('\nlaunch_my_design.sh in app directory')
print('launch_my_design.sh logs in the remote /root/launch_err.log file\n')
os.chmod('launch_my_design.sh', 0o755)

for elem in board_driver_array:
	if elem[0] in ['dataComplex_to_ram', 'dataReal_to_ram'] :
		print('Do not forget to enable a %s sender scripts in launch_my_design.sh'%elem[1])
	if elem[0] in ['firComplex', 'firReal'] :
		print('Do not forget to enable a %s coefficient loader scripts in launch_my_design.sh'%elem[1])
	if elem[0] in ['fft'] :
		print('Do not forget to enable a %s coefficient loader scripts in launch_my_design.sh'%elem[1])
	if elem[0] in ['windowReal'] :
		print('Do not forget to enable a %s coefficient loader scripts in launch_my_design.sh'%elem[1])
