# A quick example of using the ESP32-S2 (Adafruit ESP32-S2 Reverse TFT Feather) as a web client 
# to fetch questions from the Open Trivia Database and display them on the TFT display. 
# The user can press the buttons to answer the question.

# The code is based on the Adafruit CircuitPython WebClient example
# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT

#  To setup Python on the Adafruit ESP32-S2 Reverse TFT Feather, follow the instructions here:
# https://learn.adafruit.com/esp32-s2-reverse-tft-feather/circuitpython

import os
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import digitalio
import time

# URLs to fetch from
TEXT_URL = "http://wifitest.adafruit.com/testwifi/index.html"
JSON_QUOTES_URL = "https://www.adafruit.com/api/quotes.php"
JSON_STARS_URL = "https://api.github.com/repos/adafruit/circuitpython"
JSON_TRIVIA_URL = "https://opentdb.com/api.php?amount=1&category=9&difficulty=easy&type=boolean"

print("ESP32-S2 WebClient Test")
print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

# print("Available WiFi networks:")
# for network in wifi.radio.start_scanning_networks():
#     print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
#                                              network.rssi, network.channel))
# wifi.radio.stop_scanning_networks()

print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
print(f"My IP address: {wifi.radio.ipv4_address}")

# ping_ip = ipaddress.IPv4Address("8.8.8.8")
# ping = wifi.radio.ping(ip=ping_ip)

# # retry once if timed out
# if ping is None:
#     ping = wifi.radio.ping(ip=ping_ip)

# if ping is None:
#     print("Couldn't ping 'google.com' successfully")
# else:
#     # convert s to ms
#     print(f"Pinging 'google.com' took: {ping * 1000} ms")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

button_a = digitalio.DigitalInOut(board.D1)
button_b = digitalio.DigitalInOut(board.D2)


# Define a function to decode HTML entities manually
def decode_html(html_string):
    html_entities = {
        "&quot;": "\"",
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&nbsp;": " ",
        # Add more entities as needed
    }

    for entity, char in html_entities.items():
        html_string = html_string.replace(entity, char)

    return html_string


while True:
    # print(f"Fetching json from {JSON_TRIVIA_URL}")
    response = requests.get(JSON_TRIVIA_URL)
    correct_answer = response.json().get("results")[0].get("correct_answer")
    decoded_response = decode_html(response.json().get("results")[0].get("question"))
    print(" ")
    print("?" * 40)
    print(decoded_response)
    print(" ")
    print("?" * 40)

    # print(f"Correct Answer: {correct_answer}")
    print("Press D1: True  or  D2: False")


    while True:
        if button_a.value:
            if correct_answer == "True":
                print("\n CORRECT! \n")
            else:
                print("\n INCORRECT! \n")
            break

        if button_b.value:
            if correct_answer == "False":
                print("\n CORRECT! \n")
            else:
                print("\n INCORRECT! \n")
            break

    for i in range(5, 0, -1):
        print(f"Next question in {i} seconds")
        time.sleep(1)
    # print("Done")


# button.switch_to_input(pull=digitalio.Pull.UP)

# print(f"Fetching text from {TEXT_URL}")
# response = requests.get(TEXT_URL)
# print("-" * 40)
# print(response.text)
# print("-" * 40)

# print(f"Fetching json from {JSON_QUOTES_URL}")
# response = requests.get(JSON_QUOTES_URL)
# print("-" * 40)
# print(response.json())
# print("-" * 40)

# print()

# print(f"Fetching and parsing json from {JSON_STARS_URL}")
# response = requests.get(JSON_STARS_URL)
# print("-" * 40)
# print(f"CircuitPython GitHub Stars: {response.json()['stargazers_count']}")
# print("-" * 40)
