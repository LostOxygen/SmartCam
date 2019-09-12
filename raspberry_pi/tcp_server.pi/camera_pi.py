#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Kameramodul für Raspberrypi zum abfangen einzelner Bilder für Livestream etc

import time
import io
import threading
import picamera
from picamera.array import PiRGBArray


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    frame_cv = None
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self): #normales Frame zurück
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    def get_frame_cv(self): #numpy Frame für Verarbeitung
        Camera.last_access = time.time()
        self.initialize()
        return self.frame_cv

    def get_picture(self):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (1920, 1088)
            stream = PiRGBArray(camera, size=(1920, 1088)) #Benutzt ein PiRGBArray
            camera.hflip = True
            camera.vflip = True

            #stream = io.BytesIO()
            for frame in camera.capture_continuous(stream, 'bgr', use_video_port=True):
                self.frame_cv = frame.array #numpy Array für Bildverarbeitung
                # store frame
                stream.seek(0)
                self.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()
                break
            return self.frame_cv

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (1920, 1088)
            stream = PiRGBArray(camera, size=(1920, 1088)) #Benutzt ein PiRGBArray
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            #stream = io.BytesIO()
            for frame in camera.capture_continuous(stream, 'bgr', use_video_port=True):
                cls.frame_cv = frame.array #numpy Array für Bildverarbeitung
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 100:
                    break
        cls.thread = None
