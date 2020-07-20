#!/usr/bin/python3

import time
import sys
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 16      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
rgb = (0,0,0)

class ledStrip():
    def __init__(self):
        pass

    def set_color(self, color):
        rgb = int(color, 16)
        r = int(rgb / 256 / 256)
        rgb = rgb - r * 256*256
        g = int(rgb / 256)
        b = rgb - g * 256
        # Create NeoPixel object with appropriate configuration.
        strip = PixelStrip(
            LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        strip.begin()

        for i in range(0, strip.numPixels(), 1):
            strip.setPixelColor(i, Color(g, r, b))
            strip.show()
