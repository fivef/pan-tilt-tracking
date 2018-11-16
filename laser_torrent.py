from __future__ import division
import BlynkLib
import time
import pigpio

BLYNK_AUTH = '4f6b78ff330d428fae84c2defcae8347'

PAN_PIN = 19
TILT_PIN = 18

PAN_MIN_ANGLE_DEG = -90
PAN_MAX_ANGLE_DEG = 90

TILT_MIN_ANGLE_DEG = -20
TILT_MAX_ANGLE_DEG = 30

PAN_NEUTRAL_MS = 1340
TILT_NEUTRAL_MS = 680

MS_PER_DEGREE = 840/90


# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

gpio = pigpio.pi()  
gpio.set_mode(TILT_PIN, pigpio.OUTPUT)
gpio.set_mode(PAN_PIN, pigpio.OUTPUT)

'''convert degree to servo ms timing 
   returns ms '''
def angle_to_ms(angle, neutral_ms, ms_per_degree):
    return int(neutral_ms + float(angle) * ms_per_degree)

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print('Current V1 value: {}'.format(value))
    ms_value = angle_to_ms(value, PAN_NEUTRAL_MS, -MS_PER_DEGREE)
    print('pan ms: {}'.format(ms_value))

    try:
        gpio.set_servo_pulsewidth(PAN_PIN, ms_value)
    except pigpio.error as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Error")


@blynk.VIRTUAL_WRITE(2)
def my_write_handler2(value):
    print('Current V2 value: {}'.format(value))
    ms_value = angle_to_ms(value, TILT_NEUTRAL_MS, MS_PER_DEGREE)
    print('tilt ms: {}'.format(ms_value))

    try:
        gpio.set_servo_pulsewidth(TILT_PIN, ms_value)
    except pigpio.error as e:
        print("Error: {}".format(e))
    except Exception as e:
        print("Error")

@blynk.VIRTUAL_READ(9)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(9, time.ticks_ms() // 1000)

# Start Blynk (this call should never return)
blynk.run()