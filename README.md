### Usage
```python
usage: sudo server_start.py [-h] [-p PORT] [-a BIND_ADDRESS] [-v | -q] [--logfile LOGFILE]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port on which the server should run

  -a BIND_ADDRESS,      adress on which the server will bind
  --bind_address BIND_ADDRESS

  -wp PORT,             port on which the webservice should run
  --web_port PORT

  -wa BIND_ADDRESS,     adress on which the webservice will bind
  --web_bind_address

  -v, --verbose         Prints info messages
  -q, --quiet           Prints only error messages

  --logfile LOGFILE     Logs will be written to this file
```

### Dependecies:
(install in this order) \
*Python3 is required to run!*
+ DirMngr : **sudo apt-get install dirmngr**
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ [NumPy](http://www.numpy.org/): **sudo pip3 install numpy**
+ [SymPy](http://www.sympy.org/): **sudo pip3 install sympy**
+ [Neopixel](http://learn.adafruit.com/): **sudo pip3 install adafruit-circuitpython-neopixel**
+ [OpenCV](http://www.opencv.org/) **sudo pip3 install opencv-python**

### Particularities with Debian/Raspbian
Not every version of debian/raspbian covers the pre-build opencv package mentioned above. If the installation fails, you have to build opencv manually. To do so, build the paket **libfaac** with the following instructions:
```python
 sudo nano /etc/apt/sources.list
 deb http://www.deb-multimedia.org/ stretch main non-free hinzufügen
 sudo apt-get install debian-keyring
 gpg --keyserver pgp.mit.edu --recv-keys 1F41B907
 gpg --armor --export 1F41B907 | apt-key add
 sudo apt-get update
 sudo apt-get install deb-multimedia-keyring
 sudo apt-get update
 sudo apt-get install libfaac-dev
```
After this you can build OpenCV with this tutorial:
+ [OpenCV](http://www.codebind.com/cpp-tutorial/install-opencv-ubuntu-cpp/)

### Troubleshooting
Überprüfen ob OpenCV richtig installiert wurde:
```python
  import cv2
  cv2.__version__
```
If the module **cv2** can't be found, go to:
```python
  /usr/local/lib/python2.x/dist-packages
```
and copy the directory **cv2** to
```python
  /usr/local/lib/python3.x/dist-packages
```
