import os
import socket
import time
from sense_hat import SenseHat


sense = SenseHat()


#Getting temperature from room
#-------------------------------------
#Function to measure cpu temperature, used for correcting fault in sensor temperature
def cpu_temp():
    tmp = os.popen('vcgencmd measure_temp').readline()
    return(float(tmp.replace("temp=","").replace("'C\n","")))

def get_temp():
    sense.clear()

    temp = sense.get_temperature_from_pressure()
    temp += sense.get_temperature_from_humidity()

    avgTemp = temp / 2

    #Divisor calculated from room temperature of 20C
    #correctedTemp = avgTemp - (cpuTemp - avgTemp)/divisor
    tempFactor = (cpu_temp() - avgTemp) / 1.9869
    
    correctedTemp = avgTemp

    #if cpu temp is higher than air temperature, it affects the sensors
    if cpu_temp() > avgTemp:
        correctedTemp -= tempFactor

    return(correctedTemp)

#-------------------------------------

#Getting humidity from room
#-------------------------------------
def get_humidity():
    sense.clear()
    hum = sense.get_humidity()
    return(hum)
#-------------------------------------

#Getting pressure from room
#-------------------------------------
def get_pressure():
    sense.clear()
    pres = sense.get_pressure()
    return(pres)
#-------------------------------------

#Network part, send data to main computer
#-------------------------------------
def send_data(tempData, humData, presData):
    destIP = '192.168.0.11'
    destPort = 1001
    listPort = 1002

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        soc.connect((destIP,destPort))
        soc.sendto(bytes(tempData, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(humData, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(presData, "utf-8"), (destIP, destPort))
        soc.close()
    except:
        pass
    
#-------------------------------------

while True:
    temperature = str(get_temp())[0:8]
    humidity = str(get_humidity())[0:8]
    pressure = str(get_pressure())[0:8]
    
    print(temperature)
    print(humidity)
    print(pressure)
    
    send_data(temperature, humidity, pressure)
    
    #sleep for 60 seconds
    time.sleep(5)
