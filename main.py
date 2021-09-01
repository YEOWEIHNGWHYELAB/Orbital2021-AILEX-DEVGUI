#-----------------------------------------------------------------------------
import kivy

kivy.require('1.9.0')

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.video import Video
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
import subprocess
import glob
import os
import sys
import threading
import keyboard
import time
import math
import random
import Vehicle_Traversing
import webbrowser
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
screen_manager = Builder.load_file("design.kv")
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
class introVideo(Video):
    def __init__(self,  **kwargs):
        super(introVideo,  self).__init__(**kwargs)
        self.source = "CARLA_Trailer.avi"
        self.state = 'play'
        self.options = {'eos': 'loop'}
        self.bind(on_touch_down = self.on_stop)

    def check(self):
        Logger.info("film position:" + str(self.position))

    def on_stop(self,  *args):
        self.state = 'stop'  # stop the video
        main_window.remove_widget(introVid)
        main_window.current = 'main_Menu'  # switch to the other Screen

class mainMenu(Screen):
    def __init__(self, **kwargs):
        super(mainMenu, self).__init__(**kwargs)

    def exit(self):
        quit()
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
class singlePlayer(Screen):
    def __init__(self, **kwargs):
        super(singlePlayer, self).__init__(**kwargs)

    def popupCARLAexe(self):
        the_popup = CARLASTADNBYPopup()
        the_popup.open()

class CARLASTADNBYPopup(Popup):
    def __init__(self,  **kwargs):
        super(CARLASTADNBYPopup,  self).__init__(**kwargs)

    def exeMainCarla(self):
        subprocess.Popen(["../../CarlaUE4.exe"])

    def exeMainCarla_low(self):
        t1 = threading.Thread(target=lowQualityEnv)
        t1.start()

class envTweaks(Screen):
    def __init__(self, **kwargs):
        super(envTweaks, self).__init__(**kwargs)
        self.numVehicle = 0
        self.numWalker = 0
        self.isSafe = False
        self.lightOn = False
        # Save Game Parameters.
        #----------------------------------------------------------
        self.streetLite = ""
        self.tiIam = ""
        self.whether = ""

        self.Sun_Altitude_Input = 0.0
        self.Sun_Azimuth_Input = 0.0
        self.Clouds_Input = 0.0
        self.Rain_Input = 0.0
        self.Wind_Input = 0.0

        self.Puddles_Input = 0.0
        self.Fog_Input = 0.0
        self.FogDist_Input = 99.0
        self.FogFallOff_Input = 0.0
        self.Wetness_Input = 0.0
        # ----------------------------------------------------------

    def descriptionPopup(self):
        the_popup = popupDescription()
        the_popup.open()

    def descriptionPopup1(self):
        the_popup = popupDescription1()
        the_popup.open()

    def switchSafeOnOff(self, instance, value):
        if value is True:
            self.isSafe = True
        else:
            self.isSafe = False

    def switchLightOnOff(self, instance, value):
        if value is True:
            self.lightOn = True
        else:
            self.lightOn = False

    # Save Files & Execute Files.
    #----------------------------------------------------------
    def saveFile(self, idName):
        filename = "save" + str(idName) + ".txt"
        filename1 = "saveZ" + str(idName) + ".txt"

        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --altitude '
        commandStr += str(self.Sun_Altitude_Input)
        commandStr += " "
        commandStr += "--azimuth "
        commandStr += str(self.Sun_Azimuth_Input)
        commandStr += " "
        commandStr += "--clouds "
        commandStr += str(self.Clouds_Input)
        commandStr += " "
        commandStr += "--rain "
        commandStr += str(self.Rain_Input)
        commandStr += " "
        commandStr += "--wind "
        commandStr += str(self.Wind_Input)
        commandStr += " "
        commandStr += "--puddles "
        commandStr += str(self.Puddles_Input)
        commandStr += " "
        commandStr += "--fog "
        commandStr += str(self.Fog_Input)
        commandStr += " "
        commandStr += "--fogdist "
        commandStr += str(self.FogDist_Input)
        commandStr += " "
        commandStr += "--fogfalloff "
        commandStr += str(self.FogFallOff_Input)
        commandStr += " "
        commandStr += "--wetness "
        commandStr += str(self.Wetness_Input)
        print(commandStr)

        commandStr1 = '--weather ' + str(self.whether) + "\n"
        commandStr2 = '--sun ' + str(self.tiIam) + "\n"
        commandStr3 = '--lights ' + str(self.streetLite)

        file1 = open(filename, "w")
        file1.write(commandStr)
        file1.close()

        file2 = open(filename1, "w")
        file2.write(commandStr1)
        file2.write(commandStr2)
        file2.write(commandStr3)
        file2.close()

    def writeFile(self, executionID):
        filename = "save" + str(executionID) + ".txt"
        with open(filename, 'r') as file:
            data = file.read()

        # print(data)

        # os.system(str(data))

        filename1 = "saveZ" + str(executionID) + ".txt"
        text_file = open(filename1, "r")
        lines = text_file.read().split('\n')

        commandStr1 = 'cmd /c "activate CarlaCompat && python environmentBoi.py ' + lines[0]
        commandStr2 = 'cmd /c "activate CarlaCompat && python environmentBoi.py ' + lines[1]
        commandStr3 = 'cmd /c "activate CarlaCompat && python environmentBoi.py ' + lines[2]

        print(commandStr1)
        print(commandStr2)
        print(commandStr3)

        os.system(commandStr1)
        os.system(commandStr2)
        os.system(commandStr3)

    def writeFileZ(self, executionID):
        filename = "save" + str(executionID) + ".txt"
        with open(filename, 'r') as file:
            data = file.read()

        print(data)

        os.system(str(data))
    # ----------------------------------------------------------

    def spinnerTimeClicked(self, value):
        # print(value)
        if (value == "sunset"):
            self.weatherBoiSun(0)

        elif(value == "day"):
            self.weatherBoiSun(1)

        else:
            self.weatherBoiSun(2)

    def spinnerWeatherClicked(self, value):
        if (value == "clear"):
            self.weatherBoiWeather(0)

        elif(value == "overcast"):
            self.weatherBoiWeather(1)

        else:
            self.weatherBoiWeather(2)

    def spinnerStreetLightClicked(self, value):
        if (value == "on"):
            self.weatherBoiLights(True)

        else:
            self.weatherBoiLights(False)

    # -----------------------------------------------------------------------------
    # Weather Boi Function
    def weatherBoiSun(self, state):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --sun '

        # sunset
        if (state == 0):
            commandStr += "sunset"

        # day
        elif (state == 1):
            commandStr += "day"

        # night
        else:
            commandStr += "night"

        print(commandStr)

        os.system(commandStr)

    def weatherBoiWeather(self, state):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --weather '

        # clear
        if (state == 0):
            commandStr += "clear"

        # overcast
        elif (state == 1):
            commandStr += "overcast"

        # rain
        else:
            commandStr += "rain"

        os.system(commandStr)

    def weatherBoiSunAltitude(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --altitude '
        commandStr += str(stateFloat)
        print(commandStr)
        os.system(commandStr)

    def weatherBoiAzimuth(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --azimuth '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiClouds(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --clouds '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiRains(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --rain '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiPuddles(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --puddles '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiWind(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --wind '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiFog(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --fog '
        commandStr += str(stateFloat)

        # print(commandStr)

        os.system(commandStr)

    def weatherBoiFogdist(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --fogdist '
        commandStr += str(stateFloat)
        os.system(commandStr)
        # print(commandStr)

    def weatherBoiFogfalloff(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --fogfalloff '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiWetness(self, stateFloat):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --wetness '
        commandStr += str(stateFloat)
        os.system(commandStr)

    def weatherBoiLights(self, state):
        commandStr = 'cmd /c "activate CarlaCompat && python environmentBoi.py --lights '

        if (state):
            commandStr += "on"
        else:
            commandStr += "off"

        os.system(commandStr)
    # -----------------------------------------------------------------------------

class popupDescription(Popup):
    def __init__(self, **kwargs):
        super(popupDescription, self).__init__(**kwargs)

class popupDescription1(Popup):
    def __init__(self, **kwargs):
        super(popupDescription1, self).__init__(**kwargs)

class vehicleSelect(Screen):
    def __init__(self, **kwargs):
        super(vehicleSelect, self).__init__(**kwargs)

class manualCon(Screen):
    def __init__(self, **kwargs):
        super(manualCon, self).__init__(**kwargs)

class additionalMode(Screen):
    def __init__(self, **kwargs):
        super(additionalMode, self).__init__(**kwargs)

class laneExplore(Screen):
    def __init__(self, **kwargs):
        super(laneExplore, self).__init__(**kwargs)

class noRender(Screen):
    def __init__(self, **kwargs):
        super(noRender, self).__init__(**kwargs)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
class multiPlayer(Screen):
    def __init__(self, **kwargs):
        super(multiPlayer, self).__init__(**kwargs)

    def openAILEXWeb(self):
        webbrowser.open('https://ailex-auth.web.app/', new=2)

    def openCARLADOCWeb(self):
        webbrowser.open('https://carla.org/', new=2)

class lanBasedPlay(Screen):
    def __init__(self, **kwargs):
        super(lanBasedPlay, self).__init__(**kwargs)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
class deMO(Screen):
    def __init__(self, **kwargs):
        super(deMO, self).__init__(**kwargs)

    # -----------------------------------------------------------------------------
    def wasdControlSamplePopup(self):
        the_popup_1 = wasdControlSamplePopup()
        the_popup_1.open()

    def wasdControlSampleFunc(self, type):
        commandStr = 'cmd /c "activate CarlaCompat && python WASDManualControl.py'

        if (type == True):
            commandStr += " --filter=walker"

        os.system(commandStr)

    def XBOXControlSampleFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python XBOXManualControl.py'

        os.system(commandStr)

    def XBOXControlSample(self):
        t1 = threading.Thread(target=self.XBOXControlSampleFunc)
        t1.start()

    def wasdControlSample(self, type):
        t1 = threading.Thread(target=self.wasdControlSampleFunc, args=[type])
        t1.start()
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    def SimpleDriveInitializationPopup(self):
        the_popup_2 = SimpleDriveInitializationPopup()
        the_popup_2.open()

    def SimpleDriveInitializationFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python Simple_Drive_Forward.py'
        os.system(commandStr)

    def SimpleDriveInitialization(self):
        t1 = threading.Thread(target=self.SimpleDriveInitializationFunc)
        t1.start()
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    def SimpleLidarPopup(self):
        the_popup_2 = SimpleDriveInitializationPopup()
        the_popup_2.open()

    def SimpleLaneDetectFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python Lane_Detection_window.py'
        os.system(commandStr)

    def SimpleLaneDetect(self):
        t1 = threading.Thread(target=self.SimpleLaneDetectFunc)
        t1.start()

    def SimpleLidarFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python Simple_Lidar.py'
        os.system(commandStr)

    def SimpleLidar(self):
        t1 = threading.Thread(target=self.SimpleLidarFunc)
        t1.start()
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    def rayCastFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python raycast_sensor_testing.py'
        os.system(commandStr)

    def rayCast(self):
        t1 = threading.Thread(target=self.rayCastFunc)
        t1.start()

    # -----------------------------------------------------------------------------
    def clientBoundFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python client_bounding_boxes.py'
        os.system(commandStr)

    def clientBound(self):
        t1 = threading.Thread(target=self.clientBoundFunc)
        t1.start()
    # -----------------------------------------------------------------------------

    # -----------------------------------------------------------------------------
    def BangCarPopup(self):
        the_popup_2 = SimpleDriveInitializationPopup()
        the_popup_2.open()

    def BangCarFunc(self):
        commandStr = 'cmd /c "activate CarlaCompat && python vehicle_Bang.py'
        os.system(commandStr)

    def BangCar(self):
        t1 = threading.Thread(target=self.BangCarFunc)
        t1.start()
    # -----------------------------------------------------------------------------

class wasdControlSamplePopup(Popup):
    def __init__(self, **kwargs):
        super(wasdControlSamplePopup, self).__init__(**kwargs)

class SimpleDriveInitializationPopup(Popup):
    def __init__(self, **kwargs):
        super(SimpleDriveInitializationPopup, self).__init__(**kwargs)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
class autoControl(Screen):
    def __init__(self, **kwargs):
        super(autoControl, self).__init__(**kwargs)
        self.behaviour = "normal "
        self.loop = False
        self.agent = "Behavior "

    def autoControl(self):
        t1 = threading.Thread(target=self.autoControlFunc)
        t1.start()

    def autoControlFunc(self):
        commandStr = "cmd /c activate CarlaCompat && python automatic_control.py -b "
        commandStr += self.behaviour
        commandStr += "-a "
        commandStr += self.agent

        if (self.loop):
            commandStr += "--loop"

        print(commandStr)

        os.system(commandStr)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Initialize multiscreen
main_window = ScreenManager()

# Introduction Video Screen
introVid = Screen(name = 'Intro_Video')
introVid.add_widget(introVideo())
main_window.add_widget(introVid)

# Main Menu Screen
main_window.add_widget(mainMenu(name = "main_Menu"))

# Single Player Screen
main_window.add_widget(singlePlayer(name = "single_Player"))
main_window.add_widget(envTweaks(name = "env_tweaks"))
main_window.add_widget(vehicleSelect(name = "vehicle_tweaks"))
main_window.add_widget(manualCon(name = "manual_Con"))
main_window.add_widget(additionalMode(name = "additonal_Mode"))
main_window.add_widget(noRender(name = "no_render"))
main_window.add_widget(laneExplore(name = "lane_explore"))

# Multiplayer Screen
main_window.add_widget(multiPlayer(name = "multi_Player"))
main_window.add_widget(lanBasedPlay(name = "lanBased_Play"))

# DEMO Screen
main_window.add_widget(deMO(name = "Demo"))
main_window.add_widget(autoControl(name = "auto_Control"))
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Shared Functions
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# NPC Function
def npcSpawn(numVehicle, numWalker, isSafe, lightUp):
    commandStr = 'cmd /c "activate CarlaCompat && python npcSpawn.py -n' + str(" ") + str(numVehicle) + str(" -w ") + str(numWalker)

    if (isSafe):
        commandStr += " --safe"

    if (lightUp):
        commandStr += " --car-lights-on"

    os.system(commandStr)

# Dynamic Weather Boi Function
def dynamicWeatherBoi1(speed):
    commandStr = "cmd /c activate CarlaCompat && python dynamicWeatherBoi.py -s "
    commandStr += str(speed)
    os.system(commandStr)

# Open Notepad++
def openNotePadPP():
    os.system('cmd /c "C:\\Program Files (x86)\\Notepad++\\notepad++.exe"')

# Run Vehicle Gallery
def vehicleGallery():
    os.system('cmd /c "activate CarlaCompat && python Vehicle_Traversing.py')

# Launch Low Quality Carla Environment!
def lowQualityEnv():
    os.system('cmd /c "..\\..\\CarlaUE4.exe -quality-level=Low')

def sumoSync(townNum):
    commandStr1 = 'cmd /c "activate CarlaCompat && python config.py --map Town0'
    commandStr1 += str(townNum)
    os.system(commandStr1)

    commandStr2 = 'cmd /c "activate CarlaCompat && cd ..\\..\\Co-Simulation\\Sumo && python run_synchronization.py examples/Town0'
    commandStr2 += str(townNum)
    commandStr2 += ".sumocfg --tls-manager sumo --sumo-gui"
    # print(commandStr2)
    os.system(commandStr2)

def noRenderActivate(render, triggerBox, connection, spawnPoint):
    commandStr = 'cmd /c "activate CarlaCompat && python no_rendering_mode.py '

    # print(render)
    # print(triggerBox)
    # print(connection)
    # print(spawnPoint)

    if (not render):
        commandStr += "--no-rendering "

    if (triggerBox):
        commandStr += "--show-triggers "

    if (connection):
        commandStr += "--show-connections "

    if (spawnPoint):
        commandStr += "--show-spawn-points "

    os.system(commandStr)

def laneExplorer(x, y, z):
    commandStr = 'cmd /c "activate CarlaCompat && python lane_explorer.py '

    commandStr += "-x " + str(x) + " "
    commandStr += "-y " + str(y) + " "
    commandStr += "-z " + str(z) + " "

    # print(commandStr)

    os.system(commandStr)

def multiPed(ip, port):
    commandStr = 'cmd /c "activate CarlaCompat && python WASDManualControl.py --filter=walker --host '
    commandStr += ip
    commandStr += " --port "
    commandStr += port

    print(commandStr)

    os.system(commandStr)

def multiVeh(ip, port, xbox):
    if (xbox):
        commandStr = 'cmd /c "activate CarlaCompat && python XBOXManualControl.py --host '
        commandStr += ip
        commandStr += " --port "
        commandStr += port

        print(commandStr)

        os.system(commandStr)

    else:
        commandStr = 'cmd /c "activate CarlaCompat && python WASDManualControl.py --host '
        commandStr += ip
        commandStr += " --port "
        commandStr += port

        print(commandStr)

        os.system(commandStr)

def ideJoke():
    commandStr = 'cmd /c "activate CarlaCompat && python SimpleIDE.py'
    os.system(commandStr)

def manualCon(mode):
    if (mode == 0):
        commandStr = 'cmd /c "activate CarlaCompat && python WASDManualControl.py'
        os.system(commandStr)

    elif (mode == 1):
        commandStr = 'cmd /c "activate CarlaCompat && python XBOXManualControl.py'
        os.system(commandStr)

    else:
        commandStr = 'cmd /c "activate CarlaCompat && python WASDManualControl.py --filter=walker'
        os.system(commandStr)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Main App
class AILEX2021App(App):
    def __init__(self, **kwargs):
        super(AILEX2021App, self).__init__(**kwargs)
        self.vehicleName = ""
        self.render = False
        self.triggerBox = False
        self.connection = False
        self.spawnPoint = False
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def build(self):
        return main_window

    def toggleRender(self, instance, value):
        if value is True:
            self.render = True
        else:
            self.render = False

    def mapSelect(self, num):
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)
        if (num == 10):
            world = client.load_world('Town10HD')

        else:
            index = str(num)
            world = client.load_world('Town0' + index)

    def npcSpawn(self, numVehicle, numWalker, isSafe, lightUp):
        t1 = threading.Thread(target = npcSpawn, args=(numVehicle, numWalker, isSafe, lightUp))
        t1.start()

    def dynamicWeatherBoi(self, speed):
        t1 = threading.Thread(target = dynamicWeatherBoi1, args=[speed])
        t1.start()

    def notepadpp(self):
        t1 = threading.Thread(target=openNotePadPP)
        t1.start()

    def openVehicleGallery(self):
        self.vehicleName = str(Vehicle_Traversing.vehicleGal(self.vehicleName))

    def sumoSync(self, townNum):
        t1 = threading.Thread(target=sumoSync, args=[townNum])
        t1.start()

    def noRenderActivate(self, render, triggerBox, connection, spawnPoint):
        t1 = threading.Thread(target=noRenderActivate, args=(render, triggerBox, connection, spawnPoint))
        t1.start()

    def laneExplorer(self, x, y, z):
        t1 = threading.Thread(target=laneExplorer, args=(x, y, z))
        t1.start()

    def multiPed(self, ip, port):
        t1 = threading.Thread(target=multiPed, args=(ip, port))
        t1.start()

    def multiVeh(self, ip, port, xbox):
        t1 = threading.Thread(target=multiVeh, args=(ip, port, xbox))
        t1.start()

    def ideJoke(self):
        t1 = threading.Thread(target=ideJoke)
        t1.start()

    def manualCon(self, mode):
        t1 = threading.Thread(target=manualCon, args=[mode])
        t1.start()

mainGUI = AILEX2021App()
mainGUI.run()
#-----------------------------------------------------------------------------