# Readme für RoboSchalt mit OpenCV
### Dependecies:
(bestenfalls in dieser Reihenfolge installieren)
*Es wird zwingend Python3 benötigt!*
+ DirMngr : **sudo apt-get install dirmngr**
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ [NumPy](http://www.numpy.org/): **sudo pip3 install numpy**
+ [OpenCV](http://www.codebind.com/cpp-tutorial/install-opencv-ubuntu-cpp/) (vor dem kompilieren libfaac s.u. installieren!)
+ zusätzlich für [V4L2 Codec](https://www.raspberrypi.org/forums/viewtopic.php?t=62364):  **sudo modprobe bcm2835-v4l2**

Grundsätzlich werden alle Skripte mit **./skriptname.py** oder **python3 skriptname.py** gestartet, lediglich *webservice.py* erfordert **sudo**.

### Libfaac für Debian (Stretch)
Läuft der Raspberrypi unter Debian/Raspbian, so gibt es das Paket Libfaac nicht in den offiziellen Repo's. Deswegen:
+ *sudo nano /etc/apt/sources.list*
+ *deb http://www.deb-multimedia.org/ stretch main non-free* hinzufügen
+ *sudo apt-get install debian-keyring*
+ *gpg --keyserver pgp.mit.edu --recv-keys 1F41B907*
+ *gpg --armor --export 1F41B907 | apt-key add*
+ *sudo apt-get install deb-multimedia-keyring*
+ *sudo apt-get update*
+ *sudo apt-get install libfaac-dev*
