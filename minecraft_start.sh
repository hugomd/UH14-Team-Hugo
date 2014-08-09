#!/bin/bash

python3 /root/minecraft/minecraft.py
cd /root/minecraft
screen -S "Minecraft" -d  -m /usr/bin/java -Xmx512M -Xms512M -jar /root/minecraft/minecraft_server.jar nogui
