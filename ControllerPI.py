from sense_hat import SenseHat
import socket


sense = SenseHat()

def send_data(accX, accY, accZ, pitch, roll, yaw):
        soc.sendto(bytes(accX, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(accY, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(accZ, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(pitch, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(roll, "utf-8"), (destIP, destPort))
        soc.sendto(bytes(yaw, "utf-8"), (destIP, destPort))
        print("pitch {0}".format(pitch))



destIP = '192.168.0.11'
destPort = 1001
listPort = 1002

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

while True:
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.connect((destIP,destPort))
    except:
        #print("Trying to connect")
        pass
    else:
        #print("Connected")
        connected = True

    

    while connected:
        sense.clear()
        
        acc = sense.get_accelerometer_raw()
        x = acc['x']
        y = acc['y']
        z = acc['z']

        ori = sense.get_orientation()
        pitch = ori["pitch"]
        roll = ori["roll"]
        yaw = ori["yaw"]

        
        
        
        try:
            send_data(str(x)[0:8], str(y)[0:8], str(z)[0:8],
                      str(pitch)[0:8], str(roll)[0:8], str(yaw)[0:8])
        except socket.error:
            #print("Disconnected")
            connected = False
            soc.close()
            
        #print(x)

