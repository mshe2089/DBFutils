from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import keyboard
import math
import time
import sys
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()
#Filename of options and output files.
dest = "test1.csv"
opti = "options.txt"

#Delay between calculation and nabbing results. Crank up if internet is bad and causes erroneous scraped results.
calcDelay = 0.3

#INDEXING DEFINITIONS
motorBrandMax = 100 #Index of the last motor brand from the dropdown menu that will be processed
motorMax = 200 #Index of the last motor (from selected brand) from the dropdown menu that will be processed
batteryMax = 20 #... so on
controllerMax = 11
propellerMax = 1

motorBrandMin = 1 #Index of the last first brand from the dropdown menu that will be processed
motorMin = 1 #Index of the first motor (from selected brand) from the dropdown menu that will be processed
batteryMin = 1 #... so on
controllerMin = 10
propellerMin = 0

#Dictionary of parameters
params = {
  "username" : "placeholder",
  "password" : "placeholder",
  "weight": "placeholder",
  "wingspan": "placeholder",
  "wingarea": "placeholder",
  "diameter": "placeholder",#INCHES
  "pitch": "placeholder",
  "blades": "placeholder",
  "Pconst": "placeholder",
  "Tconst": "placeholder",
  "Pconst": "placeholder",
  "motorBrandCur": 0,
  "motorCur": 0,
  "batteryCur": 0,
  "controllerCur": 0,
  "propellerCur": 0,
  "progress": 0
}

#Saves options from params
def save():
    try:
        o = open(opti, "w")
        keys = list(params)
        for i in range(0, len(keys)):
            o.write(str(params[keys[i]]))
            if i < len(keys) - 1:
                o.write(",")
        o.write("\n Description goes here. lorem ipsum lorem ipsum lorem ipsum lorem ipsumn ")
        o.close()
    except:
        input("Failed to save to options file. Press ENTER to continue.\n")

#Loads options into params
def load():
    try:
        o = open(opti, "r")
        ls = [i for i in o.readline().split(",")]
        keys = list(params)
        for i in range(0, len(keys)):
            if i < len(keys) - 6:
                params[keys[i]] = ls[i]
            else:
                params[keys[i]] = int(ls[i])
        o.close()
        return
    except:
        input("Error while querying options file. Press ENTER to quit now.\n")
        quit()

#Ask for new params
def paramQuery(params):
    print("Please input parameters manually. Be careful not to make any typos.\n")
    s = input("Username: \n")
    params["username"] = s
    s = input("Password: \n")
    params["password"] = s
    s = input("Weight incl. Drive (g): \n")
    params["weight"] = (s)
    s = input("Wingspan (mm): \n")
    params["wingspan"] = (s)
    s = input("Wing area (dm^2): \n")
    params["wingarea"] = (s)
    s = input("Propeller diameter (in): \n")
    params["diameter"] = (s)
    s = input("Propeller pitch (in): \n")
    params["pitch"] = (s)
    s = input("Propeller blade count: \n")
    params["blades"] = (s)
    s = input("Propeller P constant (default = 1): \n")
    params["Pconst"] = (s)
    s = input("Propeller T constant (default = 1): \n")
    params["Tconst"] = (s)
    params["motorBrandCur"] = motorBrandMin
    params["motorCur"] = motorMin
    params["batteryCur"] = batteryMin
    params["controllerCur"] = controllerMin
    params["propellerCur"] = propellerMin
    params["progress"] = 0
    save()

#Query user for options
def optQuery(params):
    choice = input("Load progress from options file? N to create new options file (Default: Y, N to restart from fresh). Y/N\n")
    if choice.upper() == "Y":
        load()
    elif choice.upper() == "N":
        try:
            f = open(dest, "w")
            f.close()
        except:
            pass
        paramQuery(params)
    else:
        optQuery()

#Query user if they want browser window
def headlessQuery():
    choice = input("Do you want this script to run a visible browser window? N to run only console window (Default: N). Y/N\n")
    if choice.upper() == "N":
        return True
    elif choice.upper() == "Y":
        return False
    else:
        headlessQuery()

###ENTRY
print("Hello.")
print("This program will automatically test ecalc component combinations.")
print("Progress is saved across script executions provided " + opti + " and " + dest + " are retained.")
print("Will require a working set of login credentials and a long (hours to days) time to run.")
print("Please close " + opti + " and " + dest + " if they are open.\n")
print("Preferably, let this script run in the background.\n")
optQuery(params)

#Open dest file
try:
    f = open(dest, "a")
except:
    input("Failed to open destination file. Press ENTER to quit now.\n")
    quit()

#Opening and logging in
try:
    options = Options()
    if headlessQuery():
        options.add_argument('--headless')
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.ecalc.ch/calcmember/login.php?https://www.ecalc.ch/motorcalc.php");    
    print("\nLogging in...")
    driver.find_element_by_id('username').send_keys(params["username"])
    driver.find_element_by_id('password').send_keys(params["password"])
    driver.find_element_by_id('myButton').click()

    time.sleep(3)#MODIFY IF INTERNET SHIT
    alert = driver.switch_to.alert
    alert.accept()
except:
    input("Failed to open window and login. Please run with window open to see exact error. Press ENTER to save and quit now.\n")
    save()
    quit()


#Entry fields (only bare necessities for now)
weightSelect = driver.find_element_by_id('inGWeight')
wingSpanSelect = driver.find_element_by_id('inGWingSpan')
wingAreaSelect = driver.find_element_by_id('inGWingArea')

propellerDiameterIn = driver.find_element_by_id('inPDiameter')
propellerPitchIn = driver.find_element_by_id('inPPitch')
propellerBlades = driver.find_element_by_id('inPBlades')
propellerPConstant = driver.find_element_by_id('inPConst')
propellerTConstant = driver.find_element_by_id('inTConst')

#Dropdown fields
batterySelect = Select(driver.find_element_by_id('inBCell'))
controllerSelect = Select(driver.find_element_by_id('inEType'))
motorBrandSelect = Select(driver.find_element_by_id('inMManufacturer'))
motorSelect = Select(driver.find_element_by_id('inMType'))
propellerSelect = Select(driver.find_element_by_id('inPType'))
calculateButton = driver.find_element_by_name('btnCalculate')

#Fetch function
def fetchAll():
    batteryLoad = driver.find_element_by_id('outBLoad')
    batteryVoltage = driver.find_element_by_id('outBVoltage')
    batteryRatedVoltage = driver.find_element_by_id('outBRatedVoltage')
    batteryEnergy = driver.find_element_by_id('outBEnergy')
    batteryCapacity = driver.find_element_by_id('outBCapacity')
    batteryUsedCapacity = driver.find_element_by_id('outBCapacityUsed')
    batteryFlightTime = driver.find_element_by_id('outBFlightTime')
    batteryMixedFlightTime = driver.find_element_by_id('outBMixedFlightTime')
    batteryWeight = driver.find_element_by_id('outBWeight')

    motorOptCurrent = driver.find_element_by_id('outOptI')
    motorOptVoltage = driver.find_element_by_id('outOptV')
    motorOptRpm = driver.find_element_by_id('outOptRpm')
    motorOptElectricalPower = driver.find_element_by_id('outOptWin')
    motorOptMechanicalPower = driver.find_element_by_id('outOptWout')
    motorOptEfficiency = driver.find_element_by_id('outOptEfficiency')

    motorMaxCurrent = driver.find_element_by_id('outMaxI')
    motorMaxVoltage = driver.find_element_by_id('outMaxV')
    motorMaxRpm = driver.find_element_by_id('outMaxRpm')
    motorMaxElectricalPower = driver.find_element_by_id('outMaxWin')
    motorMaxMechanicalPower = driver.find_element_by_id('outMaxWout')
    motorMaxEfficiency = driver.find_element_by_id('outMaxEfficiency')
    motorMaxTemperature = driver.find_element_by_id('outMaxTemp')

    wattmeterCurrent = driver.find_element_by_id('outLoggerI')
    wattmeterVoltage = driver.find_element_by_id('outLoggerV')
    wattmeterPower = driver.find_element_by_id('outLoggerP')

    propellerStaticThrust = driver.find_element_by_id('outPThrust')
    propellerRevolutions = driver.find_element_by_id('outPRpm')
    propellerStallThrust = driver.find_element_by_id('outPStallThrust')
    propeller0Thrust = driver.find_element_by_id('outPFlightThrust')
    propellerPitchSpeed = driver.find_element_by_id('outPPitchSpeed')
    propellerTipSpeed = driver.find_element_by_id('outPTipSpeed')
    propellerSpecThrust = driver.find_element_by_id('outPEfficiency')

    totalDriveWeight = driver.find_element_by_id('outTotDriveWeight')
    totalPowerWeight = driver.find_element_by_id('outTotPowerWeight')
    totalThrustWeight = driver.find_element_by_id('outTotThrustWeight')
    totalMaxCurrent= driver.find_element_by_id('outTotI')
    totalMaxPin = driver.find_element_by_id('outTotPin')
    totalMaxPout = driver.find_element_by_id('outTotPout')
    totalMaxEfficiency = driver.find_element_by_id('outTotEfficiency')
    totalTorque = driver.find_element_by_id('outTotTorque')

    allUpWeight = driver.find_element_by_id('outTotAUW')
    wingLoad = driver.find_element_by_id('outMWLoad')
    cubicWingLoad = driver.find_element_by_id('outMW3Load')
    stallSpeed = driver.find_element_by_id('outMStallSpeed')
    levelSpeed = driver.find_element_by_id('outMLevelSpeed')
    verticalSpeed = driver.find_element_by_id('outMVclimbSpeed')
    rateOfClimb = driver.find_element_by_id('outMRoc')

    return [
        (batteryLoad.text), # 0
        (batteryVoltage.text),
        (batteryRatedVoltage.text),
        (batteryEnergy.text),
        (batteryCapacity.text),
        (batteryUsedCapacity.text),
        (batteryFlightTime.text),
        (batteryMixedFlightTime.text),
        (batteryWeight.text),
        (motorOptCurrent.text), # 9
        (motorOptVoltage.text),
        (motorOptRpm.text),
        (motorOptElectricalPower.text),
        (motorOptMechanicalPower.text),
        (motorOptEfficiency.text),
        (motorMaxCurrent.text), # 15
        (motorMaxVoltage.text),
        (motorMaxRpm.text),
        (motorMaxElectricalPower.text),
        (motorMaxMechanicalPower.text),
        (motorMaxEfficiency.text),
        (motorMaxTemperature.text),
        (wattmeterCurrent.text), # 22
        (wattmeterVoltage.text),
        (wattmeterPower.text),
        (propellerStaticThrust.text), # 25
        (propellerRevolutions.text),
        (propellerStallThrust.text),
        (propeller0Thrust.text),
        (propellerPitchSpeed.text),
        (propellerTipSpeed.text),
        (propellerSpecThrust.text),
        (totalDriveWeight.text), # 32
        (totalPowerWeight.text),
        (totalThrustWeight.text),
        (totalMaxCurrent.text),
        (totalMaxPin.text),
        (totalMaxPout.text),
        (totalMaxEfficiency.text),
        (totalTorque.text),
        (allUpWeight.text), # 40
        (wingLoad.text),
        (cubicWingLoad.text),
        (stallSpeed.text),
        (levelSpeed.text),
        (verticalSpeed.text),
        (rateOfClimb.text)
        ]

#initial param entry function (enters weight, wingspan etc etc)
def initParams():
    weightSelect.send_keys(Keys.CONTROL, 'a')
    weightSelect.send_keys(Keys.BACKSPACE)
    weightSelect.send_keys(params["weight"])
    wingSpanSelect.send_keys(Keys.CONTROL, 'a')
    wingSpanSelect.send_keys(Keys.BACKSPACE)
    wingSpanSelect.send_keys(params["wingspan"])
    wingAreaSelect.send_keys(Keys.CONTROL, 'a')
    wingAreaSelect.send_keys(Keys.BACKSPACE)
    wingAreaSelect.send_keys(params["wingarea"])
    propellerDiameterIn.send_keys(Keys.CONTROL, 'a')
    propellerDiameterIn.send_keys(Keys.BACKSPACE)
    propellerDiameterIn.send_keys(params["diameter"])
    propellerPitchIn.send_keys(Keys.CONTROL, 'a')
    propellerPitchIn.send_keys(Keys.BACKSPACE)
    propellerPitchIn.send_keys(params["pitch"])
    propellerBlades.send_keys(Keys.CONTROL, 'a')
    propellerBlades.send_keys(Keys.BACKSPACE)
    propellerBlades.send_keys(params["blades"])
    propellerPConstant.send_keys(Keys.CONTROL, 'a')
    propellerPConstant.send_keys(Keys.BACKSPACE)
    propellerPConstant.send_keys(params["Pconst"])
    propellerTConstant.send_keys(Keys.CONTROL, 'a')
    propellerTConstant.send_keys(Keys.BACKSPACE)
    propellerTConstant.send_keys(params["Tconst"])

#Fetch function: input selections based on indices and scrapes results
def testParams(i,j,k,l,m):
    try:
        try:
            motorBrandSelect.select_by_index(i)
            motorSelect.select_by_index(j)
            batterySelect.select_by_index(k)
            controllerSelect.select_by_index(l)
            propellerSelect.select_by_index(m)
        except:
            return
        time.sleep(calcDelay)
        calculateButton.click()
        time.sleep(calcDelay)

        results = fetchAll()
        f.write((motorBrandSelect.first_selected_option.text) + "," + (motorSelect.first_selected_option.text) + "," + (batterySelect.first_selected_option.text) + "," + (controllerSelect.first_selected_option.text) + "," + (propellerSelect.first_selected_option.text) + ",")
        for i in range(len(results)):
            f.write(results[i])
            if i < len(results) - 1:
                f.write(",")
            else:
                f.write("\n")
    except:
        pass

#Exit function
def die():
    params["motorBrandCur"] = motorBrandTemp
    params["motorCur"] = motorTemp
    params["batteryCur"] = batteryTemp
    params["controllerCur"] = controllerTemp
    params["propellerCur"] = propellerTemp
    save()
    f.close()
    print('')
    print('Script killed. Feel free to close the console window.')
    sys.exit()
        
#MAIN SCRAPE LOOP
initParams()
print("Scraping...")
print("Press and hold tilde (`) to stop and save progress.\n Do not close window manually or all progress since last save will be lost.\n")
progressMax = (motorBrandMax - motorBrandMin)*\
    (motorMax - motorMin)*\
    (controllerMax - controllerMin)*\
    (batteryMax - batteryMin)*\
    (propellerMax - propellerMin)

motorBrandTemp = motorBrandMin
motorTemp = motorMin
batteryTemp = batteryMin
controllerTemp = controllerMin
propellerTemp = propellerMin

i = params["motorBrandCur"]
j = params["motorCur"]
k = params["batteryCur"]
l = params["controllerCur"]
m = params["propellerCur"]
while i <(motorBrandMax):
    motorBrandTemp = i
    while j <(motorMax):
        motorTemp = j
        while k <(batteryMax):
            batteryTemp = k
            while l <(controllerMax):
                controllerTemp = l
                while m <(propellerMax):
                    if keyboard.is_pressed('`'):
                        die()
                    propellerTemp = m
                    print (" Combination attempt " + str(params["progress"]) + " out of " + str(progressMax) + " possible combinations.", end = "\r")#percentage
                    testParams(i,j,k,l,m)#Mot manufacturer, Mot, Bat, Control, Prop
                    params["progress"] += 1
                    m += 1
                m = propellerMin
                l += 1
            l = controllerMin
            k += 1
        k = batteryMin
        j += 1
    j = motorMin
    i += 1

die()
