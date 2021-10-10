from bs4 import BeautifulSoup
import requests    
import unicodedata
import math
class motor:
    def __init__(self, N, kV, I, R, W) -> None:
        self.name = N.lstrip().rstrip()
        self.kV = float(kV.strip())
        self.current = float(I.strip())
        self.resistance = float(R.strip())
        self.weight = math.ceil(float(W.strip())*28.3495) 

class battery:
    def __init__(self, N, C, V, W, CR, T) -> None:
        self.name = N.lstrip().rstrip()
        self.voltage = float(V.strip())
        self.capacity = float(C.strip())
        self.c_rating = float(CR.strip())
        self.weight = math.ceil(float(W.strip())*28.3495)
        self.type = T.lstrip().rstrip()
        self.watt_hours = self.capacity*self.voltage
        self.discharge_rating = self.capacity*self.c_rating

motorBase = []
batteryBase = []
#Motor and battery list, source url and destination file name
Msrc1 = "http://www.motocalc.com/data/motor.html"
Msrc2 = "http://www.motocalc.com/data/show.cgi?table=1"
Mdest = "motors_scraped.csv"

Bsrc1 = "http://www.motocalc.com/data/cell.html"
Bsrc2 = "http://www.motocalc.com/data/show.cgi?table=2"
Bdest = "batteries_scraped.csv"


print("This program will proceed to obtain motor and battery information from motocalc\u2122's publicly available, native and user-contributed database.")
print("Sources:")
print(Msrc1)
print(Msrc2)
print(Bsrc1)
print(Bsrc2)
print("")

#COPYRIGHT WARNING!
print(">>>>>Important Notice<<<<<")
print("This compilation of data is protected by copyright law. It may be freely used for personal, non-commercial purposes only. Use of this compilation for any other purpose is expressly forbidden.\n")

print("The files <" + Mdest + "> and <" + Bdest + "> in the current directory will be overwritten.")
input("Press ENTER to confirm the operation, or close the window now.\n")

def motorDisp(i):#list motor specs, for debug
    print ("------------------------")
    print ("Motor number: " + str(i))
    print (motorBase[i].name)
    print (str(motorBase[i].kV) + " kV, " + str(motorBase[i].current) + " A (no-load current), " + str(motorBase[i].resistance) + " Ohm (resistance), " + str(motorBase[i].weight) + " g (weight)")

def fetch(src):#fetch plaintext from website, in the form of a massive list of strings.
    print("Fetching from: " + src + "\nThis may take a while...\n")
    session = requests.session()    
    req = session.get(src)    
    doc = BeautifulSoup(req.content, features="html.parser")   
    docContent = doc.get_text().split('\n')#Linesplit
    docContent = [elem.replace('\xa0',' ') for elem in docContent]#Fix formatting
    docContent = [elem.replace(',','.') for elem in docContent]#there are some typos in the database, idc
    return docContent

def parse(type, docContent, lOffset, rOffset):#Parse plaintext into list. loffset points to starting blankspace index and len-roffset points to ending blankspace index
    rowFlag = False
    for i in range(lOffset,len(docContent)-rOffset):
        if not docContent[i]:
            rowFlag = True
        elif rowFlag == True:
            rowFlag = False
            if type == "nativeMotor" or type == "userMotor" :
                if docContent[i+4].isspace() or not docContent[i+4]:#Skip entries with missing weight
                    continue
                newMotor = motor(docContent[i], docContent[i+1], docContent[i+2], docContent[i+3], docContent[i+4])
                motorBase.append(newMotor)
            elif type == "nativeBattery":
                if docContent[i+5].isspace() or not docContent[i+5] or docContent[i+6].isspace() or not docContent[i+6]:#Skip entries with missing C rating or type
                    continue
                newBattery = battery(docContent[i], docContent[i+1], docContent[i+2], docContent[i+4], docContent[i+6], docContent[i+5])
                batteryBase.append(newBattery)
            elif type == "userBattery":
                if docContent[i+5].isspace() or not docContent[i+5] or docContent[i+6].isspace() or not docContent[i+6]:#Skip entries with missing C rating or type
                    continue
                newBattery = battery(docContent[i], docContent[i+1], docContent[i+2], docContent[i+4], docContent[i+5], docContent[i+6])
                batteryBase.append(newBattery)

try:
    #fetch from motorcalc native motor database, offsets 10,5 as of writing
    docContent = fetch(Msrc1)
    parse("nativeMotor", docContent,10,5)
    #fetch from motorcalc user contributed motor database, offsets 24,21 as of writing
    docContent = fetch(Msrc2)
    parse("userMotor", docContent,24,21)
    #fetch from motorcalc native battery database
    docContent = fetch(Bsrc1)
    parse("nativeBattery", docContent,10,5)
    #fetch from motorcalc user contributed battery database
    docContent = fetch(Bsrc2)
    parse("userBattery", docContent,24,21)
except: 
    print("Exception occurred while attempting to fetch and parse data.")
    input("Press ENTER to continue...")
    Sys.exit()

print("Success!\n")
print("Motors indexed: " + str(len(motorBase)) + "\n")
print("Batteries indexed: " + str(len(batteryBase)) + "\n")
#motorDisp(1000)
#motorDisp(3000)
#motorDisp(4700)
try:
    f = open(Mdest, "w")
except:
    print("Failed to access " + Mdest + ". Please close it if it is open, and try executing script on desktop.")
    input("Press ENTER to continue...")
    Sys.exit()
f.write("Motors scraped off: " + Msrc1 + ",,,\n")
f.write("Motors scraped off: " + Msrc2 + ",,,\n")
f.write("This compilation of data is protected by copyright law. It may be freely used for personal, non-commercial purposes only. Use of this compilation for any other purpose is expressly forbidden.,,,\n")
f.write(",,,\n")
f.write("Name,kV(kV),No_Load_Current(A),Resistance(Ohm),Weight(g)\n")
for i in motorBase:
    f.write(i.name + "," + str(i.kV) + "," + str(i.current) + "," + str(i.resistance) + "," + str(i.weight) + "\n")
f.close()

try:
    f = open(Bdest, "w")
except:
    print("Failed to access " + Bdest + ". Please close it if it is open, and try executing script on desktop.")
    input("Press ENTER to continue...")
    Sys.exit()
f.write("Batteries scraped off: " + Msrc1 + ",,,\n")
f.write("Batteries scraped off: " + Msrc2 + ",,,\n")
f.write("This compilation of data is protected by copyright law. It may be freely used for personal, non-commercial purposes only. Use of this compilation for any other purpose is expressly forbidden.,,,\n")
f.write(",,,\n")
f.write("Name,Capacity(mAh),Voltage(V),Weight(g),C rating,Watt hours,Discharge rating,Type\n")
for i in batteryBase:
    f.write(i.name + "," + str(i.capacity) + "," + str(i.voltage) + "," + str(i.weight) + "," + str(i.c_rating) + "," + str(i.watt_hours) + "," + str(i.discharge_rating) + "," + i.type + "\n")
f.close()

print("Exported motors to " + Mdest + " and batteries to " + Bdest)
input("Press ENTER to continue...")