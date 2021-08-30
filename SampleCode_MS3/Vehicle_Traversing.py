#!/usr/bin/env python

# Copyright (c) 2019 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import glob
import os
import sys
import keyboard
import time

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

import math
import random

loopTrue = True

def get_transform(vehicle_location, angle, d=6.4):
    a = math.radians(angle)
    location = carla.Location(d * math.cos(a), d * math.sin(a), 2.0) + vehicle_location
    return carla.Transform(location, carla.Rotation(yaw=180 + angle, pitch=-15))

def getVehicleID():
    return str(vehicle.type_id)

def vehicleGal(vehicleID):
    vehicleID = ''
    indexcar = 0
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)
    world = client.load_world('Town01')
    spectator = world.get_spectator()
    vehicle_blueprints = world.get_blueprint_library().filter('vehicle')
    # print(len(vehicle_blueprints))
    terminate = True

    location = random.choice(world.get_map().get_spawn_points()).location

    #for blueprint in vehicle_blueprints:
    while terminate:
        loopTrue = True
        kill = False
        blueprint = vehicle_blueprints[indexcar]
        transform = carla.Transform(location, carla.Rotation(yaw=-45.0))
        global vehicle
        vehicle = world.spawn_actor(blueprint, transform)

        try:
            vehicleID = str(getVehicleID())
            # print(vehicleID)

            angle = 0

            while loopTrue:
                if keyboard.is_pressed('y'):
                    if (indexcar == 26):
                        break
                    else:
                        indexcar += 1
                        break

                if keyboard.is_pressed('t'):
                    if (indexcar == 0):
                        break
                    else :
                        indexcar -= 1
                        break

                if keyboard.is_pressed('r'):
                    kill = True
                    break

                timestamp = world.wait_for_tick().timestamp
                angle += timestamp.delta_seconds * 60.0
                spectator.set_transform(get_transform(vehicle.get_location(), angle - 90))

            time.sleep(0.2)

        finally:
            vehicle.destroy()
            print("All Cleared!")
            if (kill == True):
                terminate = False
                return vehicleID

def main():
    vehicleid = ""
    vehicleGal(vehicleid)
    print(vehicleid)

if __name__ == '__main__':
    main()
