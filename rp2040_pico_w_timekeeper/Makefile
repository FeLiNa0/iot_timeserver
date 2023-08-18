SERIAL_DEVICE=/dev/ttyACM0
ADAFRUIT_CIRCUITPY_VERSION := 8.2.2
UF2_DIR := ./deps/uf2/
UF2_FILE := ./deps/uf2/adafruit-circuitpython-pico_w-en_US-$(ADAFRUIT_CIRCUITPY_VERSION).uf2
RESET_UF2_FILE := ./deps/uf2/flash_reset.uf2

BASE_DEST:=/run/media/$(shell whoami)
BOOTLOADER=${BASE_DEST}/RPI-RP2
DEST:=${BASE_DEST}/CIRCUITPY

get-deps:
	git clone git@github.com:FeLiNa0/adafruit_micropython_compat.git ./deps/adafruit_micropython_compat
	git clone git@github.com:waveshareteam/Pico_ePaper_Code.git ./deps/Pico_ePaper_Code

flash-circuitpython: clean prep-to-flash wait-for-bootloader
	mkdir -p $(UF2_DIR)
	wget -O $(UF2_FILE) \
		https://downloads.circuitpython.org/bin/raspberry_pi_pico_w/en_US/adafruit-circuitpython-raspberry_pi_pico_w-en_US-$(ADAFRUIT_CIRCUITPY_VERSION).uf2
	cp $(UF2_FILE) $(BOOTLOADER)

install-libraries:
	# --compile 
	cp -r deps/adafruit_micropython_compat/src/* $(DEST)/lib
	cp ./deps/Pico_ePaper_Code/python/Pico_ePaper-2.66.py $(DEST)/lib/Pico_ePaper_2in66.py
	pipkin --mount $(DEST) install -r requirements.txt

wait-for-dest:
	@echo Will loop until $(DEST) is mounted
	while [ ! -d $(DEST) ] ; do sleep 1 ; done

wait-for-bootloader:
	@echo Will loop until $(BOOTLOADER) is mounted
	while [ ! -d $(BOOTLOADER) ] ; do sleep 1 ; done

cp:
	# Use cp if you do not have rsync installed
	# rsync will minimize unnecessary copying and speed up this operation
	rsync -rhP settings.toml code.py src assets $(DEST)/

diff:
	diff ${DEST}/code.py code.py
	diff ${DEST}/settings.toml settings.toml
	diff -r ${DEST}/src src/
	diff -r ${DEST}/assets assets/
	echo "No changes"

dev: wait-for-dest
	@echo Your code should only re-run when you make changes to it
	watch -n1 'make diff || make cp'

open-serial-console:
	# Pico W CircuitPython baud rate is 115200, or 11520 characters per second
	# https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-linux
	@[ -c ${SERIAL_DEVICE} ] || ( echo "Serial device not found ${SERIAL_DEVICE}" ; exit 1 )
	@echo Try running this as root user or with sudo
	screen ${SERIAL_DEVICE} 115200

prep-to-flash:
	@echo While holding the BOOTSEL button on the Pico, plug in the USB cable to your computer.
	mkdir -p $(UF2_DIR)

reset-rpi-pico-2: clean prep-to-flash wait-for-bootloader
	wget -O $(RESET_UF2_FILE) https://datasheets.raspberrypi.com/soft/flash_nuke.uf2
	cp $(RESET_UF2_FILE) $(BOOTLOADER)

clean:
	rm -rf ./deps/uf2

clean-all:
	rm -rf ./deps/
