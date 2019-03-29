# Readme für RoboSchalt mit OpenCV
### Dependecies:

+ [OpenCV](www.alatortsev.com/2018/11/21/installing-opencv-4-0-on-raspberry-pi-3-b/)
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ zusätzlich für [V4L2 Codec](https://www.raspberrypi.org/forums/viewtopic.php?t=62364):  **sudo modprobe bcm2835-v4l2**

Grundsätzlich werden alle Skripte mit **./skriptname.py** oder **python3 skriptname.py** gestartet, lediglich *webservice.py* erfordert **sudo**.
