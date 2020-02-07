#!/usr/bin/python3
# Based on NeoPixel library and strandtest example by Tony DiCola (tony@tonydicola.com)
# To be used with a 12x1 NeoPixel LED stripe.
# Place the LEDs in a circle an watch the time go by ...
# red = hours
# blue = minutes 1-5
# green = seconds
# (To run the program permanently and with autostart use systemd.)

import time
import sys
from neopixel import *

# LED strip configuration:
LED_COUNT = 16      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
rgb = (0,0,0)

def set_color(r, g, b):
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(
        LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    for i in range(0, strip.numPixels(), 1):
        strip.setPixelColor(i, Color(g, r, b))
        strip.show()

# Main program logic follows:
if __name__ == '__main__':
    rgb = int(sys.argv[1], 16)
    r = int(rgb / 256 / 256)
    rgb = rgb - r * 256*256
    g = int(rgb / 256)
    b = rgb - g * 256
    set_color(r, g, b)

