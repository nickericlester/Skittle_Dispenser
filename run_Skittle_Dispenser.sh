#!/bin/bash
# --------------------------------------------------------------------------
# <Same documentation / copyright>
# --------------------------------------------------------------------------
cd /var/lib/cloud9/ENGI301/midterm


config-pin P2_1 pwm
config-pin P2_3 pwm
config-pin P2_9 i2c
config-pin P2_11 i2c
config-pin P2_35 in
config-pin P2_2 in

python Skittle_Dispenser.py