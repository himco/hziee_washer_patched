# hziee_washer_patched
Hziee TCL Washer Free With ESP32(Web)

## Q:What's the base?
Just a piece of esp32 with micropython develop enviroment.

## Q:How to Use?
By http request within wifi.
e.g. To start Standard Mode: http://192.168.16.16/?mode=1
e.g. To send myself serial data: http://192.168.16.16/?raw=AA00CC

## Q:What's the extra lib.?
Picoweb(for the web)

## Q:What's the key of it?
Serial data below with baudrate:9600

##### Standard Mode
>A0010203010100000000000000000000000000000
000000000000000000000000000000000000000A8


##### Fast Mode
>A0010202010100000000000000000000000000000
000000000000000000000000000000000000000A7

##### Dewatering Mode
>A0010201010100000000000000000000000000000
000000000000000000000000000000000000000A6

##### Stop Mode
>A0010200010200000000000000000000000000000
000000000000000000000000000000000000000A6



