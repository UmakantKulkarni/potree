#!/usr/bin/env bash

for i in $(seq 10 15); 
do 
	for j in $(seq 1 6); 
	do 
		echo "Working on cam_pos = $i and target_pos = $j"
		nohup tcpdump -i lo0 -w static_${i}_${j}.pcap &
		python3 get_data.py -i 127.0.0.1 -c $i -t $j
		pkill -f tcpdump
		pkill -f tcpdump
	done
done