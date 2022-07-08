#初始化串口
from machine import UART
uart=UART(2,baudrate=9600, rx=16, tx=17, timeout=2)

#初始化beeper
from machine import Pin, PWM
import utime
beeper = PWM(Pin(2,Pin.OUT),freq=0,duty=0)
beeper.duty(0)
#初始化led
from machine import Pin, PWM
import utime
led = Pin(23,Pin.OUT)
led.off()

def beep_work(times=1):
    for i in range(times):
        led.on()
        beeper.freq(1000)
        beeper.duty(500)
        utime.sleep_ms(50)
        beeper.duty(0)
        led.off()
        utime.sleep_ms(50)

#初始化picoweb
import picoweb
app=picoweb.WebApp(__name__)

#提示信息
errmsg=""
sucmsg=""

#字符串hex转字节hex
def str2byte(str_buf="AABBCCDDEE010203FF"):
    global errmsg,sucmsg
    
    str_buf = str_buf.replace(" ", "")
    bytes_buff = []
    if len(str_buf) % 2 == 0:
        sucmsg=""
        for i in range(0, len(str_buf), 2):
            # print(int("0x" + str_buf[i:i + 2]))
            sucmsg+=" " + str_buf[i:i + 2]
            bytes_buff.append(int("0x" + str_buf[i:i + 2]))
        sucmsg="send:"+sucmsg
        beep_work(1)
        return bytes(bytes_buff)
        
    else:
        print("[error]hex字符串非法")
        errmsg="hex字符串非法"
        beep_work(2)
        return bytes(0x00)#错误
    #print(bytes_buff)
    
@app.route("/")
def index(req, resp):
    yield from picoweb.start_response(resp, content_type = "text/html")
    #yield from resp.awrite("Hello world ESP32")
    
    #初始化错误内容
    global errmsg,sucmsg
    errmsg=sucmsg=""
    
    #获取参数
    params = picoweb.parse_qs(req.qs)
    print("===================")
    print(params)
    print("===================")
    
    mode = params.get("mode")#获取模式
    raw = params.get("raw")#获取串口数据

    #按照模式发送数据
    if mode and len(mode)!=0:
        if mode == "1":
            print("标准模式")
            uart.write(str2byte("A0010203010100000000000000000000000000000000000000000000000000000000000000000000A8"))
        if mode == "2":
            print("快速模式")
            uart.write(str2byte("A0010202010100000000000000000000000000000000000000000000000000000000000000000000A7 "))
        if mode == "3":
            print("脱水模式")
            uart.write(str2byte("A0010201010100000000000000000000000000000000000000000000000000000000000000000000A6"))
        if mode == "4":
            print("停止模式")
            uart.write(str2byte("A0010200010200000000000000000000000000000000000000000000000000000000000000000000A6"))
            
    #直接发送数据
    elif raw and len(raw)!=0:
        uart.write(str2byte(raw))

    htmlFile = open('webhtml.html', 'r')
    for line in htmlFile:
        if len(errmsg)!=0:
            line=line.replace("errmsg=\"\"","errmsg=\""+errmsg+"\"")
        if len(sucmsg)!=0:
            line=line.replace("sucmsg=\"\"","sucmsg=\""+sucmsg+"\"")
        yield from resp.awrite(line)


app.run(debug=True, host="0.0.0.0", port=80)