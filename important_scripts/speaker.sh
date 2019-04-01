sleep 5
pulseaudio --start
sleep 5
UUID=$(cat /proc/sys/kernel/random/uuid)
(cd /home/pi/capstone-project-group-23/Capstone_Winter_Work/HA/btmanager &&
	python3 example.py $UUID http://192.168.0.100:3111 &&
	python3 runner.py $UUID http://192.168.0.100:3111)
