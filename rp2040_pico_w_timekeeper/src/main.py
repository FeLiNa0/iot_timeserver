import os
import ipaddress
import wifi
import socketpool

from src.draw import draw

def main():
    print("Connecting to WiFi")
    
    #  connect to your SSID
    SSID = os.getenv('CIRCUITPY_WIFI_SSID')
    wifi.radio.connect(SSID, os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    
    print("Connected to WiFi: ", SSID)
    
    pool = socketpool.SocketPool(wifi.radio)
    
    #  prints MAC address to REPL
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])
    
    #  prints IP address to REPL
    print("My IP address is", wifi.radio.ipv4_address)
    
    #  pings Google
    ipv4 = ipaddress.ip_address("8.8.4.4")
    print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))
    
    draw()
