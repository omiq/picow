import sys
import os
import ipaddress
import wifi
import socketpool
import time
import board
from digitalio import DigitalInOut, Direction

# This needs to be in the lib directory on the board
from adafruit_httpserver import Server, Request, Response, POST, GET


#  onboard LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

# This checks the details are loaded successfully
try:
    ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    password = os.getenv("CIRCUITPY_WIFI_PASSWORD")
    print("Connecting to WIFI: " + ssid, end = ' ... ')
except:
    print("Ensure your settings.toml has the required info")
    sys.exit()


#  connect to your SSID
for retries in range(5):
    try:
        # Wait before attempting
        time.sleep(1)
        wifi.radio.connect(ssid, password)
    except:
        print("Could not connect to WiFi. Check your settings.toml file?")


# Success ...
print("Connected!")
pool = socketpool.SocketPool(wifi.radio)

#  prints MAC address to REPL
print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

#  prints IP address to REPL
server_ip = wifi.radio.ipv4_address
print(f"My IP address is {server_ip}")

# HTTP server init:
server = Server(pool, "/public_html", debug=True)

# Output html consistantly
def html(body, title="PICO W"):

    # Templates
    header = f"""<html>
        <head><title>{title}</title>
        <style>
        body {{font-family: sans-serif;}}
        </style>
        </head>
        <body>
        <h1>Pico W Web Server</h1>"""

    end_html = "</body></html>"

    return header + body + end_html

# Root route:
@server.route("/")
def base(request: Request):

    text = f"""
    <h2>Now responding on IP: {server_ip}</h2>
    """

    #  serve the HTML with content type text/html
    return Response(request, html(text), content_type='text/html')


# LED
@server.route("/led/<value>", GET)
def base(request: Request, value):

    # Convert to numeric
    led.value = int(value)

    text = f"""
    <h2>LED: {led.value}</h2>
    """

    #  serve the HTML with content type text/html
    return Response(request, html(text), content_type='text/html')



print("starting server..")
# startup the server
try:
    server.start(str(wifi.radio.ipv4_address), port=80)
    print("Listening on http://%s" % wifi.radio.ipv4_address)
#  if the server fails to begin, restart the pico w
except OSError:
    time.sleep(5)
    print("restarting..")
    microcontroller.reset()

while True:
    #  poll the server for incoming/outgoing requests
    server.poll()
    time.sleep(0.1)

