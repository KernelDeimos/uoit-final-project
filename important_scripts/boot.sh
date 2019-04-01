#!/bin/bash
sudo -u pi screen -S btsetup -dm ./btsetup.sh
sleep 12
sudo -u pi screen -S btspeaker -dm ./speaker.sh

