
from machine import Pin, SoftI2C, Timer, RTC

import time

# Own modules
import ssd1306


class STATE:
    WAIT = 0
    RUN = 1

WAIT_DURATION = 20
RUN_DURATION = 5
INIT_STATE = STATE.WAIT

# You can choose any other combination of I2C pins
i2c = SoftI2C(scl=Pin(5), sda=Pin(4))

devices = i2c.scan()
oled = ssd1306.SSD1306_I2C(128, 32, i2c)


def seconds_to_timer(s):
    return '{:02}:{:02}:{:02}'.format(s//3600, s%3600//60, s%60)


class ProgressBar:
    def __init__(self, height):
        self.height = height
    
    def show(self):
        self.oled.text("|"*self.counter, 0 , self.height)
        self.oled.text("|"*self.counter, 2 , self.height)
        self.oled.text("|"*self.counter, 4 , self.height)
    

class HeartBeat:
    def __init__(self):
        self.cycle_start = time.time()
        self.state = INIT_STATE

    def beat(self, timer):
        diff = time.time() - self.cycle_start
        
        if self.state == STATE.WAIT:
            if diff < WAIT_DURATION:
                self.show(diff)
            else:
                self.state = STATE.RUN
                self.run()
        else:
            if diff < WAIT_DURATION + RUN_DURATION:
                self.show(diff)
            else:
                machine.reset()

    def show(self, diff):      
        oled.fill(0)
        if self.state == STATE.WAIT:
            time_left = WAIT_DURATION - diff
            oled.text("Status: WAIT", 0, 0)
            oled.text("Time: " + seconds_to_timer(time_left), 0, 10)
        else:
            time_left = (WAIT_DURATION + RUN_DURATION) - diff
            oled.text("Status: RUN", 0, 0)
            oled.text("Time: " + seconds_to_timer(time_left), 0 ,10)

        oled.show()
    
    def run(self):
        # trigger running operation
        pass


timer = Timer()
timer.init(freq=10, mode=Timer.PERIODIC, callback=HeartBeat().beat)
