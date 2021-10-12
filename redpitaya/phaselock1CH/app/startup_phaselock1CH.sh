./phaselock1CH_us.sh
./fir_loader.py /dev/DemodFIR_125MSa_125MSa fir_lp_4000000_12000000_40dB.dat
./fir_loader.py /dev/DemodFIR_125MSa_25MSa fir_lp_4000000_12000000_40dB.dat
./fir_loader.py /dev/DemodFIR_25MSa_5MSa fir_lp_4000000_12000000_40dB.dat
./zmq_data2ram_fast.py &
./phaselock1CH_webserver.py

