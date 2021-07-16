autorun generator
===================

Introduction
------------
The autorun_generator generates a bash script that can be launched at the board startup. This includes: 
- mounting the remote nfs folder,
- going inside the repertory of the FPGA design,
- flashing the FPGA,
- starting the webserver app,
- other extra applications you need to be launched at the startup (fir coeff loader, zmq sender...).

The generated `launch_my_design.sh` file must be placed in the `/usr/bin directory` of the board.
The file `S90wakeupscript` must be placed in the `/etc/init.d` directory of the board.

The logs of the launch script are recorded in the `launch_err.log` file stored in the `/root` directory of the board. 


Test it
-------

- Source the file containing the environement variables (sample [here](https://github.com/oscimp/oscimpDigital/blob/master/settings.sh.sample))
- Go to your project directory. For instance [double_iq_pid_vco](https://github.com/oscimp/app/tree/master/redpitaya/double_iq_pid_vco).

```shell
cd %fpga_designs_repo/double_iq_pid_vco/design/
```

- Generate the xml file associated to your project:

```shell
make xml
```

- Go to the upstream folder

```shell
cd ../
```

- Verify in the resulting `double_iq_pid_vco.xml` file that the IPs that use the AXI bus are all represented and have the good address.   

- Generate the autorun script:

```shell
autorun_generator.py double_iq_pid_vco.xml
```

Output:
```
launch_my_design.sh in app directory
launch_my_design.sh logs in the remote /root/launch_err.log file

Do not forget to enable a dataReal_to_ram_fast sender scripts in launch_my_design.sh
Do not forget to enable a dataReal_to_ram_slow sender scripts in launch_my_design.sh
Do not forget to enable a firReal_0 coefficient loader scripts in launch_my_design.sh
Do not forget to enable a firReal_1 coefficient loader scripts in launch_my_design.sh
```

Example of `launch_my_design.sh` script generated for the design [double_iq_pid_vco](https://github.com/oscimp/app/tree/master/redpitaya/double_iq_pid_vco):

```shell
#### find the local IP
MY_IP=$(/sbin/ifconfig eth0 | grep "inet ad" | cut -f2 -d: | awk "{print $1}")

#### mount the remote nfs folder and go inside it
mount /usr/local/

cd /usr/local/double_iq_pid_vco/bin/

#### flash fpga
sh double_iq_pid_vco_us.sh

#### start webserver
screen -dmS webserver ./double_iq_pid_vco_webserver.py
sleep 2
wget $MY_IP

#### your design applications
#screen -dmS dataReal_to_ram_fast ./my_zmq_data2ram_script.py
#screen -dmS dataReal_to_ram_slow ./my_zmq_data2ram_script.py
#./my_fir_coeff_loader_script.py /dev/firReal_0 my_fir_coeff_file.dat
#./my_fir_coeff_loader_script.py /dev/firReal_1 my_fir_coeff_file.dat

```

- The `launch_my_design.sh` script must be edited to include the running of scripts that are specific to your FPGA design. For instance the design [double_iq_pid_vco](https://github.com/oscimp/app/tree/master/redpitaya/double_iq_pid_vco)
includes two dataReal_to_ram blocks and two firReal blocks. The firReal recquires the load of coefficiens to work (example [here](https://github.com/oscimp/app/blob/903e5c141b3578e9b8974532a17a3fe84010f0fc/redpitaya/double_iq_pid_vco/app/fir_loader.py)), and the dataReal_to_ram may recquire a data sender script (example [here](https://github.com/oscimp/app/blob/903e5c141b3578e9b8974532a17a3fe84010f0fc/redpitaya/double_iq_pid_vco/app/zmq_data2ram_fast.py)). Go to the app directory to edit the launch script:

```shell
cd app
vi launch_my_design.sh
```

- Then edit the launch script according to your specific application.


- Finally install the launch scripts in the target board, at IP XXX.XXX.XXX.XXX:

```shell
make install_autorun_ssh IP=XXX.XXX.XXX.XXX
```

- You are done! Reboot the board and verify the content of the `launch_err.log` log file and verify that everything runs perfectly.
