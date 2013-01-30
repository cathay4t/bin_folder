#!/bin/sh
# uncomment this if you enabled synaptic in BIOS.
#xinput set-int-prop "SynPS/2 Synaptics TouchPad" "Synaptics Off" 8 1
#xinput set-int-prop "SynPS/2 Synaptics TouchPad" "Device Enabled" 8 0
xinput set-int-prop "TPPS/2 IBM TrackPoint" \
    "Evdev Wheel Emulation" 8 1
xinput set-int-prop "TPPS/2 IBM TrackPoint" \
    "Evdev Wheel Emulation Button" 8 2
#xinput set-int-prop "TPPS/2 IBM TrackPoint" \
#    "Evdev Wheel Emulation Timeout" 8 200
xinput set-float-prop "TPPS/2 IBM TrackPoint" \
    "Device Accel Velocity Scaling" 244

# speed up mouse
#xset m 5 1
