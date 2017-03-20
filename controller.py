#! /usr/bin/env python
# -*- coding: utf-8 -*-

import Adafruit_BBIO.PWM as PWM
from time import sleep
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.PWM as PWM
import Adafruit_TCS34725
import os
import pprint
import pygame
import smbus
import time
import numpy as np
    
GPIO.setup("P8_8", GPIO.OUT)
GPIO.setup("P8_10", GPIO.OUT)
GPIO.setup("P8_12", GPIO.OUT)
GPIO.setup("P8_14", GPIO.OUT)
GPIO.setup("P8_7", GPIO.OUT)
GPIO.setup("P8_9", GPIO.OUT)
GPIO.setup("P8_11", GPIO.OUT)

PWM.start("P9_14", 100, 50)
PWM.start("P9_16", 100, 50)

ADC.setup()
# Create a TCS34725 instance with default integration time (2.4ms) and gain (4x).

def obstacle_ahead():
    reading = ADC.read("P9_39")
    if reading < 0.70:
        return 1
    else:
        return 0

def lights_on():
    GPIO.output("P8_11", GPIO.HIGH)
    
def lights_off():
    GPIO.output("P8_11", GPIO.LOW)

def read_right_color():
    GPIO.output("P8_9", GPIO.HIGH)
    sleep(0.1)
    tcs = Adafruit_TCS34725.TCS34725()
    r, g, b, c = tcs.get_raw_data()
    for i in range(0,5):
        r_, g_, b_, c_ = tcs.get_raw_data()
        r += r_
        g += g_
        b += b_
        c += c_
    GPIO.output("P8_9", GPIO.LOW)
    print("Right: ", r/5, g/5, b/5)
    return r/5, g/5, b/5, c/5
    
def read_left_color():
    GPIO.output("P8_7", GPIO.HIGH)
    sleep(0.1)
    tcs = Adafruit_TCS34725.TCS34725()
    r, g, b, c = tcs.get_raw_data()
    for i in range(0,5):
        r_, g_, b_, c_ = tcs.get_raw_data()
        r += r_
        g += g_
        b += b_
        c += c_
    GPIO.output("P8_7", GPIO.LOW)
    print("Left: ", r/5, g/5, b/5)
    return r/5, g/5, b/5, c/5

def is_blue(r, g, b):
    if r < 15 and g < 15 and b > 15:
        return 1
    else:
        return 0

def is_black(r, g, b):
    if r < 10 and g < 10 and b < 10:
        return 1
    else:
        return 0

def turn_right():
    print("Turning right")
    go_forward()
    sleep(1)
    GPIO.output("P8_8", GPIO.LOW)
    GPIO.output("P8_10", GPIO.HIGH)
    sleep(1.0)
    go_forward()
    sleep(1)
    kill_motors()
    
def turn_left():
    print("Turning left")
    go_forward()
    sleep(1)
    GPIO.output("P8_12", GPIO.LOW)
    GPIO.output("P8_14", GPIO.HIGH)
    sleep(1)
    go_forward()
    sleep(1)
    kill_motors()
        
def turn_slightly_right():
    print("Turning slightly right")
    GPIO.output("P8_8", GPIO.LOW)
    GPIO.output("P8_10", GPIO.HIGH)
    GPIO.output("P8_12", GPIO.HIGH)
    GPIO.output("P8_14", GPIO.LOW)
    sleep(0.1)
    go_forward()
    
def turn_slightly_left():
    print("Turning slightly left")
    GPIO.output("P8_8", GPIO.HIGH)
    GPIO.output("P8_10", GPIO.LOW)
    GPIO.output("P8_12", GPIO.LOW)
    GPIO.output("P8_14", GPIO.HIGH)
    sleep(0.1)
    go_forward()
    
def go_forward():
    GPIO.output("P8_8", GPIO.HIGH)
    GPIO.output("P8_10", GPIO.LOW)
    GPIO.output("P8_12", GPIO.HIGH)
    GPIO.output("P8_14", GPIO.LOW)
    
def kill_motors():
    # print("Stopping")
    GPIO.output("P8_8", GPIO.LOW)
    GPIO.output("P8_10", GPIO.LOW)
    GPIO.output("P8_12", GPIO.LOW)
    GPIO.output("P8_14", GPIO.LOW)

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""
        
        print("initializing:")
        pygame.init()
        pygame.joystick.init()
        print("joystick initialized")
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        print("initialized:", bool(self.controller))
        print(self.controller.get_name())

    def listen(self):
        """Listen for events to happen"""
        headlights_on = 0
        auto_mode = 0
        at_intersection = 0
        intersection_no = 0
        while True:
            if auto_mode == 0:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        if event.button == 5:
                            print("Right motor forward")
                            GPIO.output("P8_8", GPIO.HIGH)
                            GPIO.output("P8_10", GPIO.LOW)
                        elif event.button == 7:
                            print("Right motor backward")
                            GPIO.output("P8_8", GPIO.LOW)
                            GPIO.output("P8_10", GPIO.HIGH)
                        elif event.button == 4:
                            print("Left motor forward")
                            GPIO.output("P8_12", GPIO.HIGH)
                            GPIO.output("P8_14", GPIO.LOW)
                        elif event.button == 6:
                            print("Left motor backward")
                            GPIO.output("P8_12", GPIO.LOW)
                            GPIO.output("P8_14", GPIO.HIGH)
                        elif event.button == 0:
                            auto_mode = 1
                            lights_on()
                            print("Auto mode on!")
                        elif event.button == 2:
                            print("Turning right test")
                            turn_right()
                            kill_motors()
                        elif event.button == 3:
                            if headlights_on == 0:
                                headlights_on = 1
                                lights_on()
                            else:
                                headlights_on = 0
                                lights_off()
                        # print(event.button)
                    elif event.type == pygame.JOYBUTTONUP:
                        GPIO.output("P8_8", GPIO.LOW)
                        GPIO.output("P8_10", GPIO.LOW)
                        GPIO.output("P8_12", GPIO.LOW)
                        GPIO.output("P8_14", GPIO.LOW)
            elif auto_mode == 1:
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                         if (event.button == 0):
                            auto_mode = 0
                            lights_off()
                            print("Auto mode off!")
                while obstacle_ahead() == 1:
                    print("Obstacle Ahead!")
                    sleep(1)
                left_color_r, left_color_g, left_color_b, c = read_left_color()
                right_color_r, right_color_g, right_color_b, c = read_right_color()
                if is_black(left_color_r, left_color_g, left_color_b) == 1:
                    turn_slightly_right()
                if is_black(right_color_r, right_color_g, right_color_b) == 1:
                    turn_slightly_left()
                if is_blue(left_color_r, left_color_g, left_color_b) == 1 or is_blue(right_color_r, right_color_g, right_color_b) == 1:
                    at_intersection = 1
                    print("Came to intersection")
                if at_intersection == 1 and is_blue(left_color_r, left_color_g, left_color_b) == 0 and is_blue(right_color_r, right_color_g, right_color_b) == 0:
                    intersection_no += 1
                    at_intersection = 0
                    print("At intersection no: ", intersection_no);
                if intersection_no == 1:
                    print("Going forward on the first intersection")
                elif intersection_no == 2:
                    print("Exiting the first intersection")
                elif intersection_no == 3:
                    print("Arrived on the second intersection")
                    kill_motors()
                    print("Stopping at the stop sign")
                    sleep(5)
                    go_forward()
                elif intersection_no == 4:
                    print("Exiting the second intersection")
                elif intersection_no == 5:
                    print("Turning right on the third intersection")
                    turn_right()
                    intersection_no += 1
                elif intersection_no == 6:
                    print("Going forward on the fourth intersection")
                elif intersection_no == 7:
                    print("Exiting the fourth intersection")
                elif intersection_no == 8:
                    print("Turning left on the fifth intersection")
                    turn_left()
                    intersection_no += 1
                go_forward()
                sleep(0.1)
                kill_motors()


if __name__ == "__main__":
    print("Starting main")
    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
    GPIO.cleanup()
    PWM.stop("P9_14")
    PWM.stop("P9_16")
    PWM.cleanup()
