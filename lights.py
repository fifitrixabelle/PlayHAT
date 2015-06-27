# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time
import sys
import httplib
import urllib2
import socket
import exceptions
socket.setdefaulttimeout(30)
from IPython import embed

from neopixel import *
from beautifulhue.api import Bridge
import RPi.GPIO as GPIO

# LED strip configuration:
LED_COUNT      = 9       # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Button config
GPIO.setmode(GPIO.BCM)
RED_BUTTON_PIN = 4
GREEN_BUTTON_PIN = 17
YELLOW_BUTTON_PIN = 22
BLUE_BUTTON_PIN = 27
RED_BUTTON = GPIO.setup(RED_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GREEN_BUTTON = GPIO.setup(GREEN_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
YELLOW_BUTTON = GPIO.setup(YELLOW_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
BLUE_BUTTON = GPIO.setup(BLUE_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Hue config
USERNAME = 'beautifulhuetest'
BRIDGE = Bridge(device={'ip':'192.168.0.2'}, user={'name':USERNAME})

HUE_COLOURS = {
    'red':0,
    'yellow':12750,
    'blue':46920,
    'green':25500
    }
LED_COLOURS = {
    'red':[255,0,0],
    'yellow':[255,255,0],
    'blue':[0,0,255],
    'green':[0,255,0]
    }

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
  """Wipe color across display a pixel at a time."""
  for i in range(strip.numPixels()):
    strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)

def turnOnAll(colour):
  print colour
  resource = {
      'which':0,
      'data':{
        'action':{
          'on':True,
          'hue':HUE_COLOURS[colour],
          'bri':255
          }
        }
      }
  colorWipe(strip, Color(*LED_COLOURS[colour]))
  BRIDGE.group.update(resource)
  colorWipe(strip, Color(0, 0, 0))

def turnOffAll():
  print "Turning off"
  resource = {
      'which':0,
      'data':{
        'action':{
          'on':False,
          }
        }
      }
  BRIDGE.group.update(resource)
  colorWipe(strip, Color(0, 0, 0))

def cleanUp():
  turnOffAll()
  GPIO.cleanup()
  exit()


if __name__ == '__main__':
  strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
  strip.begin()

  print 'Press Ctrl-C to quit.'
  active = ""
  buttons = {
      RED_BUTTON_PIN:"red",
      YELLOW_BUTTON_PIN:"yellow",
      GREEN_BUTTON_PIN:"green",
      BLUE_BUTTON_PIN:"blue"
      }
  while True:
    try:
      # if button pressed change lights
      for button in buttons.keys():
        if not GPIO.input(button):
          if active == buttons[button]:
            turnOffAll()
            active = ""
            time.sleep(0.5)
          else:
            turnOnAll(buttons[button])
            active = buttons[button]
            time.sleep(0.5)
      time.sleep(0.1)

    except httplib.BadStatusLine: pass

    except exceptions.KeyboardInterrupt:
      cleanUp()

    except:
      print "Unexpected error:", sys.exc_info()[0]
      cleanup()

  cleanUp()
