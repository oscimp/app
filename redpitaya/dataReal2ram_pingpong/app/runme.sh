./*_us.sh
#./*_webserver.py &

./zmq_data2ram.py /dev/data2ram 9901 16 1 16384 &
./zmq_data2ram.py /dev/data2ram_pp 9902 16 1 16384 &

# generated with `seq -32768 32767 | shuf -n 16384 -r -o randn.dat`
# or `echo "disp(ceil(randn(2^14,1)*2^(16-1)))" | octave-cli -- | sed 's/ //g' > randn.dat`
./fir_loader.py /dev/axiToRam randn.dat
