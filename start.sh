cd /home/rodrigo/hexapod
screen -dmS Hexapod python hexapod/jetson_nano/hexapod_TCP_MP.py
sleep 10
screen -dmS Joystick python PC/FRSky_TCP.py

#python3 hexapod/jetson_nano/hexapod_secuencias.py
