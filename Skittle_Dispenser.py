# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Skittle Dispenser
--------------------------------------------------------------------------
License:   
Copyright 2018 Nicholas Lester

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Use a servo to detect a hand. Then, play a song with a piezo element. Finally,
use a servo to open the door and dispense Skittles.

Also, display the fill percentage of the dispenser by taking a reading with a 
force sensitive resistor and displaying on a HT16K33 Display.

Requirements:
    - Play a song and rotate a servo when the ir beam is broken.
    - Display the fill percentage using measurements from the force sensitive 
      resistor

"""



"""
This sets the path to find the python file ht16k33_i2c_base. This may need to
change depending on where ht16k33_i2c_base is located.
"""
import sys
sys.path.append("/var/lib/cloud9/ENGI301/i2c")

import time
import math
import random

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import ht16k33_i2c_base as HT16K33

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
servo_pin = "P2_1"
piezo_pin = "P2_3"
FSR_pin = "AIN5"
ir_pin = "P2_2"


# ------------------------------------------------------------------------
# Note Library
# ------------------------------------------------------------------------
NOTE_B0  = 31
NOTE_C1  = 33
NOTE_CS1 = 35
NOTE_D1  = 37
NOTE_DS1 = 39
NOTE_E1  = 41
NOTE_F1  = 44
NOTE_FS1 = 46
NOTE_G1  = 49
NOTE_GS1 = 52
NOTE_A1  = 55
NOTE_AS1 = 58
NOTE_B1  = 62
NOTE_C2  = 65
NOTE_CS2 = 69
NOTE_D2  = 73
NOTE_DS2 = 78
NOTE_E2  = 82
NOTE_F2  = 87
NOTE_FS2 = 93
NOTE_G2  = 98
NOTE_GS2 = 104
NOTE_A2  = 110
NOTE_AS2 = 117
NOTE_B2  = 123
NOTE_C3  = 131
NOTE_CS3 = 139
NOTE_D3  = 147
NOTE_DS3 = 156
NOTE_E3  = 165
NOTE_F3  = 175
NOTE_FS3 = 185
NOTE_G3  = 196
NOTE_GS3 = 208
NOTE_A3  = 220
NOTE_AS3 = 233
NOTE_B3  = 247
NOTE_C4  = 262
NOTE_CS4 = 277
NOTE_D4  = 294
NOTE_DS4 = 311
NOTE_E4  = 330
NOTE_F4  = 349
NOTE_FS4 = 370
NOTE_G4  = 392
NOTE_GS4 = 415
NOTE_A4  = 440
NOTE_AS4 = 466
NOTE_B4  = 494
NOTE_C5  = 523
NOTE_CS5 = 554
NOTE_D5  = 587
NOTE_DS5 = 622
NOTE_E5  = 659
NOTE_F5  = 698
NOTE_FS5 = 740
NOTE_G5  = 784
NOTE_GS5 = 831
NOTE_A5  = 880
NOTE_AS5 = 932
NOTE_B5  = 988
NOTE_C6  = 1047
NOTE_CS6 = 1109
NOTE_D6  = 1175
NOTE_DS6 = 1245
NOTE_E6  = 1319
NOTE_F6  = 1397
NOTE_FS6 = 1480
NOTE_G6  = 1568
NOTE_GS6 = 1661
NOTE_A6  = 1760
NOTE_AS6 = 1865
NOTE_B6  = 1976
NOTE_C7  = 2093
NOTE_CS7 = 2217
NOTE_D7  = 2349
NOTE_DS7 = 2489
NOTE_E7  = 2637
NOTE_F7  = 2794
NOTE_FS7 = 2960
NOTE_G7  = 3136
NOTE_GS7 = 3322
NOTE_A7  = 3520
NOTE_AS7 = 3729
NOTE_B7  = 3951
NOTE_C8  = 4186
NOTE_CS8 = 4435
NOTE_D8  = 4699
NOTE_DS8 = 4978

# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

def setup():
    """Sets up the hardware components."""
    ADC.setup()
    GPIO.setup(ir_pin, GPIO.IN)
    HT16K33.display_setup()
    HT16K33.display_clear()
    
# end def

def play_note(Note, Length):
    """Plays a given note for a given length."""
    PWM.start(piezo_pin, 50, Note)
    time.sleep(Length)
    
# end def

def open_door():
    """Makes the servo open the dispensing door and close it again."""
    PWM.start(servo_pin, (100), 20.0)
    PWM.set_duty_cycle(servo_pin, 1.5)
    
    time.sleep(2.0)
    
    PWM.start(servo_pin, (100), 20.0)
    PWM.set_duty_cycle(servo_pin, 3.5)
    
    time.sleep(1.0)
    
    PWM.stop(servo_pin)
    PWM.cleanup()
    
# end def

    
def play_zelda_secret():
    """Plays the Uncover Secret song from The Legend of Zelda."""
    play_note(NOTE_G5, 0.15)
    play_note(NOTE_FS5, 0.15)
    play_note(NOTE_DS5, 0.15)
    play_note(NOTE_A4, 0.15)
    play_note(NOTE_GS4, 0.15)
    play_note(NOTE_E5, 0.15)
    play_note(NOTE_GS5, 0.15)
    play_note(NOTE_C6, 0.15)
    PWM.stop(piezo_pin)
    PWM.cleanup()
    
# end def

def play_zelda_Song_of_Time():
    """Plays the Song of Time from The Legend of Zelda."""
    play_note(NOTE_A4, 0.5)
    play_note(NOTE_D4, 1.0)
    play_note(NOTE_F4, 0.5)
    play_note(NOTE_A4, 0.5)
    play_note(NOTE_D4, 1.0)
    play_note(NOTE_F4, 0.5)
    play_note(NOTE_A4, 0.25)
    play_note(NOTE_C5, 0.25)
    play_note(NOTE_B4, 0.5)
    play_note(NOTE_G4, 0.5)
    play_note(NOTE_F4, 0.25)
    play_note(NOTE_G4, 0.25)
    play_note(NOTE_A4, 0.5)
    play_note(NOTE_D4, 0.5)
    play_note(NOTE_C4, 0.25)
    play_note(NOTE_E4, 0.25)
    play_note(NOTE_D4, 1.5)
    PWM.stop(piezo_pin)
    PWM.cleanup()
    
# end def

def play_zelda_Saria_song():
    """Plays Saria's Song from The Legend of Zelda."""
    play_note(NOTE_F4, 0.15)
    play_note(NOTE_A4, 0.15)
    play_note(NOTE_B4, 0.3)
    play_note(NOTE_F4, 0.15)
    play_note(NOTE_A4, 0.15)
    play_note(NOTE_B4, 0.3)
    play_note(NOTE_F4, 0.15)
    play_note(NOTE_A4, 0.15)
    play_note(NOTE_B4, 0.15)
    play_note(NOTE_E4, 0.15)
    play_note(NOTE_D5, 0.3)
    play_note(NOTE_B4, 0.15)
    play_note(NOTE_C5, 0.15)
    play_note(NOTE_B4, 0.15)
    play_note(NOTE_G4, 0.15)
    play_note(NOTE_E4, 0.6)
    PWM.stop(piezo_pin)
    PWM.cleanup()

# end def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    setup()
    
    while True:
        fill_percent = int(math.floor(ADC.read("AIN5") * 200))
        HT16K33.update_display(fill_percent)
        if GPIO.input("P2_2") == 0:
            song_number = random.randint(1, 3)
            if song_number == 1:
                play_zelda_secret()
            elif song_number == 2:
                play_zelda_Song_of_Time()
            elif song_number == 3:
                play_zelda_Saria_song()
            else:
                pass
            open_door()
            time.sleep(5)
        else:
            pass
        time.sleep(1)
        

        
