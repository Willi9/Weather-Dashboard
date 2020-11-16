import grovepi
import math
import time
import json

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
light_sensor = 0

# Connect the Redled to port D2, Blueled to port D3, and Greenled 
# SIG,NC,VCC,GND
Redled = 2
Blueled = 3
Greenled = 4

#We are setting up the light sensors and LED Lights 
grovepi.pinMode(light_sensor,"INPUT")
grovepi.pinMode(Redled,"OUTPUT")
grovepi.pinMode(Blueled,"OUTPUT")
grovepi.pinMode(Greenled,"OUTPUT")

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D7
# This example uses the blue colored sensor.
# SIG,NC,VCC,GND
sensor = 7  # The Sensor goes on digital port 6.

# temp_humidity_sensor_type
# Grove Base Kit comes with the blue sensor.
blue = 0    # The Blue colored sensor.

#I am creating a dictionaary object where I can store all of the details 
data = {}

data['Weather'] = []

#Day threshold represents the minimum light that needs to be outside for the system to start recording data
dayThreshold = 70

#We define what a minute is 
Minute = 60

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
        
        # This example uses the blue colored sensor. 
        # The first parameter is the port, the second parameter is the type of sensor.
        [temp,humidity] = grovepi.dht(sensor,blue)
        
        #I am calculating Fahrenheit by using the equation F = C*(9/5) + 32
        temp = (temp*(9.0/5.0))+32
        
        #If the sensor reads above the daylight threshold for light level we will begin taking measurements
        if (sensor_value > dayThreshold):
            
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                
                
                #I am getting the information and appending my list
                data['Weather'].append ({
                   'temp' : temp,
                   'humidity' : humidity })

            
                #I am going to write the data information to My JSON file thats called Weather Data
                with open('WeatherData.json','w') as outfile:
                    json.dump(data,outfile, indent = 4)
            
                #if the temperature is less than 80 degrees and more than 60 degree and the humidity
                #is less than 80percent we will turn on the green LED
                if (85>temp>60 and humidity<80):
                    grovepi.digitalWrite(Greenled,1)
                    grovepi.digitalWrite(Blueled,0)
                    grovepi.digitalWrite(Redled,0)
                   
                
                
                #If the temperature is below 95 degrees and above 85 degrees and the humidity 
                #is below 80 percent the blue LED will come one
                elif (95>temp>85 and humidity<80):
                    grovepi.digitalWrite(Greenled,0)
                    grovepi.digitalWrite(Blueled,1)
                    grovepi.digitalWrite(Redled,0)
                
                
                #If the temperatuer is above 95 degrees, the red LED will come on
                elif (temp > 95):
                    grovepi.digitalWrite(Greenled,0)
                    grovepi.digitalWrite(Blueled,0)
                    grovepi.digitalWrite(Redled,1)
                
                
                #If the humidity is above 80 percent the blue and green LEDs will come on
                elif (humidity > 80):
                    grovepi.digitalWrite(Greenled,1)
                    grovepi.digitalWrite(Blueled,1)
                    grovepi.digitalWrite(Redled,0)
  
                   
                
                #We slow down and take measurements every 30 minutes
                time.sleep(30*Minute)
             
            #We print out this message if we are not in a time we should be taking measurements   
            else:
                print("The system is currently not in operation. Please wait until daytime")
              
            
    except IOError:
        print ("Error")
