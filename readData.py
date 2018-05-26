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
        bytesize = serial.EIGHTBITS
        ,timeout = 1
)
#ser.open()
print("readUart Init")
#0-HumiOut 1-TempOut 2-HumiIn 3-TempIn 4-ReTotal 5-ReDay 6-Money 7-Pơwer 8-9-10-11-12--Power thanh phan
newData=[0,0,0,0,0,0,'0',0,0,0,0,0,0,0]
oldData=[0,0,0,0,0,0,'0',0,0,0,0,0,0,0]
isRead = True
isAvailbal = True


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
                
                ##cho write xong moi read()
                while isWriteSerial :
                    pass
                ser.flushInput()
                ser.flushOutput()
                time.sleep(.1)
                isAvailbal=False
                s=ser.read(23)
                isAvailbal =True
                print(s)
                
                if len(s) == 23 and s[0]==170 and s[1] == 85 :
                    #0-HumiOut 1-TempOut 2-HumiIn 3-TempIn 4-ReToDay 5-ReTotal 6-Money 7-Pơwer 8-9-10-11-12--Power
                    newData[0] = Rhumiout = int((s[19] + (s[20]<< 8))/100)
                    newData[1] = Rtempout = int((s[17] + (s[18]<< 8))/10) / 10
                   
                    newData[4] = RE_today = (s[13] + (s[14]<< 8))/100
                    newData[5] = RE_total = (s[9] + (s[10]<<8) + (s[11]<<16) + (s[12]<<24))/100
                    newData[13] = int(RE_total*2700)
                    newData[7] = Rpower   = (s[15] + (s[16]<< 8))
                    print("readData -- ",oldData)
                    if Rhumiout >= 0 and Rhumiout < 100 and newData[0] != oldData[0]:
                        oldData[0] = newData[0]
                    if Rtempout >= 0 and Rtempout < 100 and newData[1] != oldData[1] :
                        oldData[1] = newData[1]
                        
                    if RE_today >= 0 and RE_today < 65000 and newData[4] != oldData[4] :
                        oldData[4] = newData[4]
                    if RE_total > 0 and RE_total < 65000 and newData[5] != oldData[5] :
                        oldData[5] = newData[5]
                        oldData[13] = newData[13]
                        mon=oldData[13]
                        imon = 0
                        smon=""
                        while mon!=0 :
                            imon+=1
                            nmon=mon%10
                            smon=str(nmon)+smon
                            mon=int(mon/10)
                            if imon%3 == 0:
                                smon=","+smon
                        if imon%3 == 0 and imon > 0:
                            oldData[6]=smon[1:len(smon)]
                        elif imon==0:
                            oldData[6]='0'
                        else :
                            oldData[6]=smon
                    if Rpower >= 0 and Rpower < 99999 and newData[7] != oldData[7] :
                        oldData[7] = newData[7]
                        i=1
                        powerC = newData[7]
                        while i < 6 :
                            du = powerC % 10
                            oldData[7+i] = du
                            powerC = int(powerC/10)
                            i+=1
                    #readTempIn()
            except KeyboardInterrupt:
                ser.close()
                print("ser.close()")
            except Exception as e:
                print("ERROR SERIAL : ",e.__doc__)
                #print("error")
                #time.sleep(10)
        
    #0-HumiOut 1-TempOut 2-HumiIn 3-TempIn 4-ReToDay 5-ReTotal 6-Money 7-Pơwer 8-9-10-11-12--Power
def sent2Server():
        dataString = "ID_Device=133&Tempin="+str(oldData[2])+"&Humiin="+str(oldData[3])+"&Tempout="+str(oldData[1])+"&Humiout="+str(oldData[0])+"&Power="+str(oldData[7])+"&Enery="+str(oldData[5]);        
        baseURL = "http://solarville.vn/SolarVilleService.asmx/UploadData?"
        print(dataString)
        try :
            with urllib.request.urlopen(baseURL+dataString) as f:
                print (f.read())
                f.close()
        except:
            print ('exiting.')
def sentToThingSpeak():
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
strEncode = b'\xaa\x55\x01\x00\x00\x01\x01\x01\x00\x01\x03'
threadRead = readUart(1,"readUart",1)
threadRead.start()


global numSent2Thing , timeSent2Server
numSent2Thing = 0
timeSent2Server = 0
timeReadTempIn = 0
isWriteSerial = False
numNotReceived = 0

def sent2Arduino() :
        global numSent2Thing , timeSent2Server,timeReadTempIn,isWriteSerial
        isWriteSerial =True
        ser.write(strEncode)
        ser.flush()
        isWriteSerial =False
        print("sent header",strEncode)
        numSent2Thing+=1
        if numSent2Thing == 100 :
            numSent2Thing = 0
            #sentToThingSpeak()
            
        timeSent2Server +=1
        if timeSent2Server == 30:
            timeSent2Server = 0
            sent2Server()
            
        timeReadTempIn+=1
        if timeReadTempIn == 2:
            readTempIn()
            timeReadTempIn = 0
readTempIn()

#b'\xaaU\x00\x01\x01\x00\x01\x81\x0c\x00\x00\x00\x00\x00\x00\x94\x13_\nC \x03\x02

#b'\x01\x01\x00\x01\x81\x0c\x00\x00\x00\x00\xc2\x08\x90\x13_\n'
#b'\xaaU\x00C \x03\xc8'




