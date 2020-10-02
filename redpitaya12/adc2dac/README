# ADC to DAC

Basic ADC to DAC pass-through design

## Generate vivado project, bitstream and deploy it
```console
foo@bar:adc2dac$ source /opt/Xilinx/Vivado/2019.2/settings64.sh
foo@bar:adc2dac$ echo $OSCIMP_DIGITAL_NFS
foo@bar:adc2dac$ echo $BOARD_NAME
foo@bar:adc2dac$ cd design
foo@bar:adc2dac/design$ make
foo@bar:adc2dac/design$ make install
```

You can visually check the resulting design with Vivado:
```console
foo@bar:adc2dac/design$ vivado tmp/adc2dac.xpr
```

## Generate device tree and c/python app (optional) and deploy

```console
foo@bar:adc2dac/design$ make xml
foo@bar:adc2dac/design$ cd ..
foo@bar:adc2dac$ module_generator adc2dac.xml
foo@bar:adc2dac$ cd app
foo@bar:adc2dac/app$ make install
```

**OPTIONAL** for python webserver:
```console
foo@bar:adc2dac/app$ webserver_generator ../adc2dac.xml
foo@bar:adc2dac/app$ make install_webserver
```

**OPTIONAL** for c app:
```console
foo@bar:adc2dac/app$ make
foo@bar:adc2dac/app$ make install
```

## Deployed app/bitstream
The structure in your NFS folder should be like this:
```bash
$OSCIMP_DIGITAL_NFS/redpitaya12/
└── adc2dac
    ├── bin
    │   ├── adc2dac.dtbo
    │   ├── adc2dac_us -> c app
    │   ├── adc2dac_us.sh
    │   └── adc2dac_webserver.py -> python webserver
    └── bitstreams
        └── adc2dac_wrapper.bit.bin
 ```

 ## Run
 On redpitaya12
 ```console
root@redpitaya12:~$ mount /usr/local
root@redpitaya12:~$ cd /usr/local/adc2dac/app
root@redpitaya12:/usr/local/adc2dac/app$ ./adc2dac_us.sh
root@redpitaya12:/usr/local/adc2dac/app$ ./adc2dac_webserver.py
 ```

 Use your favorite web browser, connect to your redpitaya12 and enjoy.
