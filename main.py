import pyvisa
from datetime import datetime


rm = pyvisa.ResourceManager()
inst = rm.open_resource('USB0::0x0957::0x2007::MY57013825::0::INSTR')    
inst.timeout=5000      #set a delay
inst.write("*CLS")     #clear 
inst.write("*RST")     #reset 


'''Set Variables'''
scanIntervals = float(input("Enter the delay between measurements [in seconds]: "))      #Delay in secs, between scans
numberScans = int(input("Enter the scan quantity: "))+1         #Number of scan sweeps to measure
channelDelay = 0.1      #Delay, in secs, between relay closure and measurement 
points = 0              #number of data points stored
user = input("User: ")
thermocouples=input("Which thermocuples will be used? Type one by one with coma between them: ")

tc = f"(@{thermocouples})"
scanlist = tc
inst .write(f"CONF:TEMP TC,T,{tc}")  
 
#setup scan list
inst.write("ROUTE:SCAN " + scanlist) 
inst.write("ROUTE:SCAN:SIZE?") 
numberChannels = int(inst.read())+1
#reading format
inst.write("FORMAT:READING:CHAN ON")
inst.write("FORMAT:READING:TIME ON")  
#channel delay
inst.write("ROUT:CHAN:DELAY " + str(channelDelay)+","+scanlist)
#setup when scanning starts and interval rate
inst.write("TRIG:COUNT "+str(numberScans)) 
inst.write("TRIG:SOUR TIMER")
inst.write(("TRIG:TIMER " + str(scanIntervals)))
#start the scan and retrieve the scan time
inst.write("INIT;:SYSTEM:TIME:SCAN?")   
now = datetime.now()
start_time =  now.strftime("%d/%m/%Y %H:%M:%S")
print("Test start time: ", start_time, " | User: ")
#empty line
print()
'''wait until there is a data available'''
points = 0
while (points==0):
    inst.write("DATA:POINTS?")
    points=int(inst.read())

'''
The data points are printed 
data, time, channel
'''

for scan in range (1,numberScans):
    numberScans=numberScans-1
    scansLeft = numberScans-1

    print("Scan no.: ",scan)
    print("Scans remaining: ", scansLeft)
    for chan in range(1,numberChannels):
        try:
            inst.write("DATA:REMOVE? 1")
            values = inst.read()
            v1,v2,v3 = values.split(',')
            
            print("\nChannel: ",int(v3))
            print("Temperature: ",float(v1),"[*C]")
            print("Time: ",float(v2), "[s]\n")
            
            points = 0
            #wait for data
            while (points==0):
                inst.write("DATA:POINTS?")
                points=int(inst.read())
        except KeyboardInterrupt:
            inst.write("*CLS")     #clear 
            inst.write("*RST")     #reset     
            inst.close()
            print ('\nClosing')

       
        
    
# '''Close'''
inst.write("*CLS")     #clear 
inst.write("*RST")     #reset     
inst.close()
print ('\nClosing')