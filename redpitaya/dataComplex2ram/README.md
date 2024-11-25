## Data2RAM ping-pong demonstration

Loss-less data2ram using a half-full and full FIFO mechanism to avoid
loosing samples during data transfer as occuring with the original data2ram.

Host
----


```bash
cd design
make xpr
make xml
make
make install
cd ..
module_generator dataComplex2ram.xml
cd app
make
make install SUPP_FILE='runme.sh zmq_data2ram.py randn.dat'
grcc zmq_stream.grc
./zmq_stream.py
```

Redpitaya14-125
---------------

```bash
mount /myserver/nfs
cd /myserver/nfs/dataComplex2ram/bin/
./runme.sh
```

should display a GNU Radio tag at fixed index (no sample loss) when using the
ping-pong data2ram and moving index (lost samples) when using the data2ram.
