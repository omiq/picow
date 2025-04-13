# picow
HTTP Server example

You need to edit the `settings.toml` file

```
CIRCUITPY_WIFI_SSID = "SSID_HERE"
CIRCUITPY_WIFI_PASSWORD = "**********"
CIRCUITPY_WEB_API_PORT = 5000
```

## How it Works

This example code (`code.py`) performs the following actions:

1.  **Connects to Wi-Fi:** Reads the SSID and password from your `settings.toml` file to connect the Pico W to your local network.
2.  **Initializes Network Services:** Sets up the necessary network components, including a socket pool and an SSL context for secure connections using `adafruit_connection_manager`.
3.  **Starts a Web Server:** Uses `adafruit_httpserver` to create an HTTP server listening on port 80.
4.  **Defines Routes:**
    *   `/`: The root path displays a welcome message and the Pico W's IP address.
    *   `/time/`: Fetches the current time for London from `timeapi.io` using `adafruit_requests` and displays the day, date, year, and time.
    *   `/led/<value>`: Allows controlling the onboard LED by visiting `/led/1` (to turn on) or `/led/0` (to turn off).
5.  **Listens for Requests:** Enters a loop to continuously poll the server for incoming client requests.

## Adafruit Libraries Used

This project relies on the following Adafruit libraries located in the `./lib` directory:

*   **`adafruit_httpserver`**: Provides the core functionality for running the HTTP web server on the Pico W.
*   **`adafruit_requests.mpy`**: A library similar to Python's `requests`, used here to fetch data from the external time API.
*   **`adafruit_connection_manager.mpy`**: Helps manage Wi-Fi connections and SSL contexts for secure communication.
