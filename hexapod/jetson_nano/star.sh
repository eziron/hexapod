renice -n 1 $$

cd /home/rodrigo/hexapod
git pull origin master

/usr/bin/screen -dmS hexapod python /home/rodrigo/hexapod/hexapod/jetson_nano/hexapod_x360.py