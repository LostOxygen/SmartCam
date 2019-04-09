# Readme für RoboSchalt mit OpenCV
### Dependecies:
(bestenfalls in dieser Reihenfolge installieren)
*Es wird zwingend Python3 benötigt!*
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ [NumPy](http://www.numpy.org/): **sudo pip3 install numpy**
+ [OpenCV](http://www.codebind.com/cpp-tutorial/install-opencv-ubuntu-cpp/)
+ wichtig: für einen Raspberrypi mit Debian gibt es das Paket *libfaac* nicht in den offiziellen Repo's, [hier](https://raspberrypi.stackexchange.com/questions/10250/how-do-i-install-libfaac-dev-on-raspi) gibt es eine Anleitung zum selber kompilieren/downloaden.
+ zusätzlich für [V4L2 Codec](https://www.raspberrypi.org/forums/viewtopic.php?t=62364):  **sudo modprobe bcm2835-v4l2**

Grundsätzlich werden alle Skripte mit **./skriptname.py** oder **python3 skriptname.py** gestartet, lediglich *webservice.py* erfordert **sudo**.
