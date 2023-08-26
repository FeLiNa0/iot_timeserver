import time

import adafruit_framebuf
from Pico_ePaper_2in66 import EPD_2in66

PIXEL_FORMAT = adafruit_framebuf.MVLSB

def draw(current_time):
    epd = EPD_2in66()
    image = adafruit_framebuf.FrameBuffer(epd.buffer_Landscape, epd.height, epd.width, PIXEL_FORMAT)
    image.fill(0x00)
    image.text("RPi Pico Zero", 10, 0, 0xFF, font_name='./assets/font5x8.bin')
    image.text("FeLiNa FOREVER", 10, 20, 0xFF, font_name='./assets/font5x8.bin', size=2)
    image.text(current_time, 10, 40, 0xFF, font_name='./assets/font5x8.bin', size=3)
    
    time.sleep(1)
    epd.init(0)
    epd.Clear(0xFF)
    time.sleep(2)
    epd.display_Landscape(epd.buffer_Landscape)
    print("Drawing done. Putting screen to sleep")
    epd.sleep()
