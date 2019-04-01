#!/bin/bash

(printf "power on\n" && sleep 1) | bluetoothctl
(printf "agent on\n" && sleep 1) | bluetoothctl

sudo killall bluealsa
pulseaudio --start

(printf "connect 94:36:6E:01:B1:A5\n" && sleep 10) | bluetoothctl

pacmd set-card-profile bluez_card.94_36_6E_01_B1_A5 a2dp_sink
pacmd set-default-sink bluez_sink.94_36_6E_01_B1_A5.a2dp_sink

