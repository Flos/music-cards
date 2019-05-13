#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import alsaaudio

#print alsaaudio.cards()
#print alsaaudio.mixers()

m = alsaaudio.Mixer('PCM')
vol = m.getvolume()[0]
is_mute = m.getmute()[0]
print vol

GPIO.setmode(GPIO.BCM)

def toggle_mute():
    global is_mute
    m.setmute(1 - is_mute)
    is_mute = m.getmute()[0]
    if is_mute:
        print('Muted')
    else:
        print('Un-muted')

#pin number on pi (BCM!)
vol_up_pin = 22
vol_dn_pin = 27

#Max and min volume
min_vol = 60
max_vol = 96

GPIO.setup(vol_up_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(vol_dn_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    vu = GPIO.input(vol_up_pin)
    vd = GPIO.input(vol_dn_pin)
    if vu and not vd:
        if is_mute:
            toggle_mute()
        if vol < max_vol:
            vol += 1
            if vol <= max_vol:
                m.setvolume(vol)
            vol = m.getvolume()[0]
        print 'Volume up Pressed', vol
    elif vd and not vu:
        if is_mute:
            toggle_mute()
        if vol > min_vol:
            vol -= 1
            if vol >= min_vol:
                m.setvolume(vol)
            vol = m.getvolume()[0]
        print 'Volume down Pressed', vol
    elif vd and vu:
        toggle_mute()
        time.sleep(0.3)

    time.sleep(0.1)
