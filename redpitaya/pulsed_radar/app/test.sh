./radar_red_us bypass_mean 1
sleep 1
./radar_red_us tempo
mv mode_tempo_00.dat mode_tempo_00_sans.dat
./radar_red_us bypass_mean 0

./radar_red_us iter 1
sleep 1
./radar_red_us tempo
mv mode_tempo_00.dat mode_tempo_00_1.dat

./radar_red_us iter 16
sleep 1
./radar_red_us tempo
mv mode_tempo_00.dat mode_tempo_00_16.dat

./radar_red_us iter 64
sleep 1
./radar_red_us tempo
mv mode_tempo_00.dat mode_tempo_00_64.dat

./radar_red_us iter 512
sleep 1
./radar_red_us tempo
mv mode_tempo_00.dat mode_tempo_00_512.dat
