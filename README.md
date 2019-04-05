# Readme für RoboSchalt mit OpenCV
### Dependecies:

+ [OpenCV](https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/) (ggf. ohne VirtualEnv)
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ zusätzlich für [V4L2 Codec](https://www.raspberrypi.org/forums/viewtopic.php?t=62364):  **sudo modprobe bcm2835-v4l2**

Grundsätzlich werden alle Skripte mit **./skriptname.py** oder **python3 skriptname.py** gestartet, lediglich *webservice.py* erfordert **sudo**.
