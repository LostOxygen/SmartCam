# SmartCam Github Repository
### Usage
```python
usage: sudo python3 server_start.py [-h] [-p PORT] [-a BIND_ADDRESS] [-v | -q] [--logfile LOGFILE]
test client: python3 testClient.py [ip address]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port on which the server should run

  -a BIND_ADDRESS, --bind_address BIND_ADDRESS     adress on which the server will bind

  -v, --verbose         Prints info messages
  -q, --quiet           Prints only error messages

  --logfile LOGFILE     Logs will be written to this file
```

### Commands

| Identifier | Command                   | Description                                                                      |
|------------|---------------------------|----------------------------------------------------------------------------------|
| GOO        | [get_circle_offset](#get_circle_offset)   | returns the (X, Y) offset the gripper has to move to reach the nearest detected circle  |
| GRP        | [grab_point](#grab_point) | returns the coordinates to grab the detected part and a rotation offset for the gripper |
| GCO        | [get_cable_offset](#get_cable_offset) | returns the offset between the cable and it's vertical baseline  |
| IMG|  [image](#image) | creates and saves an image without any other stuff
| MGR| [move_gripper](#move_gripper)| moves the selected gripper gripper into specified direction -> (X, Y) offset
| OGR| [open_gripper](#open_gripper)| opens the selected gripper
| CGR| [close_gripper](#close_gripper)| closes the selected gripper
| SFX| [lights](#lights)| sets the LEDs to specified HEX values
| CLB| [calibrate](#calibrate)| calls the calibration to generate an empty config.ini and calibrates the scaling between pixels and millimeters
| EXT| [exit](#exit)| exits the server and sends EX to the client

### Errors

| Bezeichner | Fehler          | Beschreibung                                    |
|------------|-----------------|-------------------------------------------------|
| eunc       | unknown command | command doesn't exist  |
| einc       | invalid command | didn't understand specific command usage (maybe wrong parameters?) |
| eint       | internal error  | an error occured while processing the command |


### Dependecies:
(install in this order) \
*Python3 is required to run!*
+ DirMngr : **sudo apt-get install dirmngr** \
install pip packages manually or with **sudo pip3 -r requirements.txt** :
+ [Pillow](https://pillow.readthedocs.io/en/stable/): **sudo pip3 install Pillow**
+ [Flask](http://flask.pocoo.org/): **sudo pip3 install Flask**
+ [NumPy](http://www.numpy.org/): **sudo pip3 install numpy**
+ [SymPy](http://www.sympy.org/): **sudo pip3 install sympy**
+ [Neopixel](http://learn.adafruit.com/): **sudo pip3 install adafruit-circuitpython-neopixel**
+ [OpenCV](http://www.opencv.org/) **sudo pip3 install opencv-python**

### Particularities with Debian/Raspbian
Not every version of debian/raspbian covers the pre-build OpenCV package mentioned above. If the installation fails, you have to build OpenCV manually. To do so, first install the paket **libfaac** with the following instructions:
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
Check of OpenCV is installed correctly:
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
