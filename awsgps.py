import serial
import pynmea2
import time
import json
import AWSIoTPythonSDK.MQTTLib as AWSIoTPyMQTT
import time as t

ENDPOINT = "a18pni26jv19lo-ats.iot.eu-central-1.amazonaws.com"
CLIENT_ID = "testDevice"
PATH_TO_CERTIFICATE = "12dc4fe69907fb1b7096e6f34b99ee85d732fba29e1f4679dfe19dd33c6c1833-certificate.pem.crt"
PATH_TO_PRIVATE_KEY = "12dc4fe69907fb1b7096e6f34b99ee85d732fba29e1f4679dfe19dd33c6c1833-private.pem.key"
PATH_TO_AMAZON_ROOT_CA_1 = "AmazonRootCA1.pem"
TOPIC = "test/testing"

myAWSIoTMQTTClient = AWSIoTPyMQTT.AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, 8883)
myAWSIoTMQTTClient.configureCredentials(PATH_TO_AMAZON_ROOT_CA_1, PATH_TO_PRIVATE_KEY, PATH_TO_CERTIFICATE)
myAWSIoTMQTTClient.connect()

jsonlist =[]
ser = serial.Serial('/dev/ttyTHS1',baudrate=9600)
myAWSIoTMQTTClient.connect()
while True:
  line = ser.readline()

  if line.startswith('$GPRMC'):
     rmc = pynmea2.parse(line)
     status = rmc.status
     speed = rmc.spd_over_grnd 
     gps = " Status=" +str(status)  + "   Speed=" +str(speed) 
     print(gps)   
    
  if line.startswith('$GPGGA'):
     rmc2 = pynmea2.parse(line)
     alt =  rmc2.altitude 
     lat = rmc2.latitude 
     lng = rmc2.longitude
     latm = rmc2.latitude_minutes
     lngm = rmc2.longitude_minutes
     lats = rmc2.latitude_seconds
     lngs = rmc2.longitude_seconds
     lngdir= rmc2.lon_dir
     latdir= rmc2.lat_dir
     #time = rmc2.timestamp 
     gps2 ="Altitude="+str(alt) + "     Longitude=" +str(lng) + "    Latitude="+str(lat) +           "LatitudeMinutes="+str(latm) + "     LongitudeMinutes=" +str(lngm) + "    LatitudeSeconds="+str(lats) + "LongitudeSeconds="+str(lngs) + "   Longitude Direction=" + str(lngdir) +    "Latitude Direction=" + str(latdir) #+ "Time="+str(time)
     print(gps2) 


     data = {
    'Latitude' : lat,
    'Longitude':lng,
    'Status':status,
    'Speed':speed,
    'Altitude':alt,
    'LatitudeMinutes':latm,
    'LatitudeSeconds':lats,
    'LongitudeMinutes':lngm,
    'LongitudeSeconds':lngs,
	    }

     print("Published: '" + json.dumps(data) + "' to the topic: " + "'test/testing'")
     myAWSIoTMQTTClient.publish(TOPIC, json.dumps(data),1)
     t.sleep(60)   
     print('Publish End')
     jsonlist.append(data)
     filename = 'data3.json'          
     with open(filename, 'a') as file_object:  
    	json.dump(data,file_object)
myAWSIoTMQTTClient.disconnect()

