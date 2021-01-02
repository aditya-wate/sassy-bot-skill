from time import sleep
from mycroft.util import LOG
# import threading


try:
    import RPi.GPIO as GPIO
    """
    Setup if GPIO is imported
    """
    is_imported = True
except:
    is_imported = False
    pass


PUL = 17  # Driver pulse
DIR = 27  # Driver direction
ENA = 22  # Driver enable
LED = 18  # Indicator


if is_imported:
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(PUL, GPIO.OUT)
    LOG.info("PUL = GPIO 17")
    GPIO.setup(DIR, GPIO.OUT)
    LOG.info("PUL = GPIO 27")
    GPIO.setup(ENA, GPIO.OUT)
    LOG.info("PUL = GPIO 22")
    GPIO.setup(LED, GPIO.OUT)
    LOG.info("PUL = GPIO 18")


    LOG.info("GPIO Setup Complete.")


durationFwd = 200 # Forward spin duration (full rotation 1600)
durationBwd = 200 # Reverse spin duration
delay = 0.0000002 # Delay between PUL.


def forward():
    sleep(.5) # TODO: needs to be removed
    GPIO.output(DIR, GPIO.LOW)
    LOG.info("DIR set to LOW")

    LOG.info("Rotating CW")
    GPIO.output(LED, GPIO.HIGH)
    for x in range(durationFwd): 
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(LED, GPIO.LOW)
    sleep(.5) # TODO: needs to be removed
    return


def reverse():
    sleep(.5) # TODO: needs to be removed
    GPIO.output(DIR, GPIO.HIGH)
    LOG.info("DIR set to HIGH")

    LOG.info("Rotating CCW")
    GPIO.output(LED, GPIO.HIGH)
    for y in range(durationBwd):
        GPIO.output(PUL, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL, GPIO.LOW)
        sleep(delay)
    GPIO.output(LED, GPIO.LOW)
    sleep(.5) # TODO: needs to be removed
    return

def run():
    # TODO: this loop needs to be killed on stop()
    count = 0
    # while True: # TODO: Original logic to be implemented
    # below will cause rocker state sync issues after loop finishes
    while count <= 10: # can't risk infinite loop yet
        if GPIO.input(ENA):
            reverse()
            forward()
            count += 1
        else:
            break

def start():
    GPIO.output(ENA, GPIO.HIGH)
    LOG.info("Starting stepper...")
    run()
    # TODO: if above doesn't work try threading
    # t1 = threading.Thread(target = run)
    # t1.start()
    
def stop():
    GPIO.output(ENA, GPIO.LOW)
    LOG.info("Stopping stepper...")


def cleanup():
    GPIO.cleanup()
    LOG.info("Cleanup for stepper...")
