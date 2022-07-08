# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)


#network
import network
_wlan = network.WLAN(network.STA_IF)
_wlan.active(True)
_wlan.connect('Isaacnet','123456789')


import gc
import webrepl
webrepl.start()
gc.collect()

try:
    exec(open('webserver.py').read())
except:
    print('open \'webserver.py\' error.')
