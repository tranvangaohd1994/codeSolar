import urllib.request 
import time 
import serial
import threading
from pi_sht1x import SHT1x
import RPi.GPIO as GPIO

ser = serial.Serial(
	port = '/dev/ttyAMA0',
	baudrate = 19200,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
	timeout = 1
)

print("readUart Init")
#0-HumiOut 1-TempOut 2-HumiIn 3-TempIn 4-ReTotal 5-ReDay 6-Money 7-Pơwer 8-9-10-11-12--Power thanh phan
newData=[0,0,0,0,0,0,0,0,0,0,0,0,0]
oldData=[0,0,0,0,0,0,0,0,0,0,0,0,0]

isRead = True
isAvailbal = True
numSent2Thing = 0

def readTempIn():
    print("read tempIn")
    try:
        with SHT1x(18, 23, gpio_mode=GPIO.BCM) as sensor:
            tempIn = sensor.read_temperature()
            humidityIn = sensor.read_humidity(tempIn)
            newData[2] = (int(tempIn*10))/10
            newData[3] = int(humidityIn)
            if oldData[2] != newData[2] : 
                oldData[2] = newData[2]
            if oldData[3] != newData[3] :
                oldData[3] = newData[3]
    except :
        print("error SHT read temp")
    finally :
        print("done ReadTempIn")

class readUart(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):
        while isRead :
            try :
                #sent to Node
                #\xaaU\x00\x01\x01\x00\x01\x81\x0c\x00\x00\x00\x00\x00\x00\x00\x00\x14\x00\x14\x00\x01\xb7
                #(170, 85, 0, 1, 1, 0, 1, 129, 12, 0, 0, 0, 0,  0, 0,    0, 0, | 179, 5, | 157, 23, | 2, 251)
                # 0    1   2  3  4  5  6  7    8   9  10 11 12  13 14    15 16 | 17   18 | 19   20  | 21 22
                #-----------------header--------   -RE_total-  -Etoday--- P------T         H           checksum      
                isAvailbal=False
                s=ser.read(23)# read du 23 ki tu moi tra ve
                isAvailbal = True
                print(s)
                
                if len(s) == 23 and s[0]==170 and s[1] == 85 :
                    #0-HumiOut 1-TempOut 2-HumiIn 3-TempIn 4-ReToDay 5-ReTotal 6-Money 7-Pơwer 8-9-10-11-12--Power
                    newData[0] = Rhumiout = int((s[19] + (s[20]<< 8))/100)
                    newData[1] = Rtempout = int((s[17] + (s[18]<< 8))/10) / 10
                   
                    newData[4] = RE_today = (s[13] + (s[14]<< 8))/10
                    newData[5] = RE_total = (s[9] + (s[10]<<8) + (s[11]<<16) + (s[12]<<24))/10
                    newData[6] = int(RE_total*2700)
                    newData[7] = Rpower   = (s[15] + (s[16]<< 8))
                    print("readData -- ",oldData)
                    if Rhumiout > 10 and Rhumiout < 100 and newData[0] != oldData[0]:
                        oldData[0] = newData[0]
                    if Rtempout > 3 and Rtempout < 100 and newData[1] != oldData[1] :
                        oldData[1] = newData[1]
                        
                    if RE_today > 0 and RE_today < 65000 and newData[4] != oldData[4] :
                        oldData[4] = newData[4]
                    if RE_total > 0 and RE_total < 65000 and newData[5] != oldData[5] :
                        oldData[5] = newData[5]
                        oldData[6] = newData[6]

                    if Rpower >= 0 and Rpower < 99999 and newData[7] != oldData[7] :
                        oldData[7] = newData[7]
                        i=1
                        powerC = newData[7]
                        while i < 6 :
                            du = powerC % 10
                            oldData[7+i] = du
                            powerC = int(powerC/10)
                            i+=1
                    readTempIn()
                    numSent2Thing+=1
                    if numSent2Thing == 15 :
                        numSent2Thing =0
                        self.sentToThingSpeak()
                        
        
            except KeyboardInterrupt:
                ser.close()
                print("ser.close()")
            except Exception as e:
                print("ERROR SERIAL : ",e.__doc__)
                #print("error")
                #time.sleep(10)
    
    def sentToThingSpeak(self):
        tin,hin  = oldData[2], oldData[3]
        to,ho = oldData[1],oldData[0]
        print ('starting a`senting to thingspeak...')
        myAPI = "5M9J9T2YMZB2DJZY"
        baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
        try :
            with urllib.request.urlopen(baseURL+"&field1=%s&field2=%s&field3=%s&field4=%s" % (tin,hin,to,ho)) as f:
                print (f.read())
                f.close()
        except:
            print ('exiting.')
  
HEADER = [170, 85, 1, 0, 0, 1, 1, 1, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
str1=''.join(str(chr(e)) for e in HEADER)
#strEncode = str1.encode().strip()
strEncode = b'\xaa\x55\x01\x00\x00\x01\x01\x01\x00\x01\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
threadRead = readUart(1,"readUart",1)
threadRead.start()
def sent2Arduino() :
        ser.write(strEncode)
        ser.flush()
        print("sent header",strEncode)
readTempIn()


