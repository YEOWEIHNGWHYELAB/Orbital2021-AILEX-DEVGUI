#!/usr/bin/env python

# Copyright (c) 2020 Computer Vision Center (CVC) at the Universitat Autonoma de
# Barcelona (UAB).
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Vehicle physics example for CARLA
Small example that shows the effect of different impulse and force aplication
methods to a vehicle.
"""

import glob
import os
import sys
import argparse

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
import keyboard

def print_step_info(world, vehicle):
    snapshot = world.get_snapshot()
    print("%d %06.03f %+8.03f %+8.03f %+8.03f %+8.03f %+8.03f %+8.03f %+8.03f %+8.03f %+8.03f" %
            (snapshot.frame, snapshot.timestamp.elapsed_seconds, \
            vehicle.get_acceleration().x, vehicle.get_acceleration().y, vehicle.get_acceleration().z, \
            vehicle.get_velocity().x, vehicle.get_velocity().y, vehicle.get_velocity().z, \
            vehicle.get_location().x, vehicle.get_location().y, vehicle.get_location().z))

def wait(world, frames=100):
    for i in range(0, frames):
        world.tick()

def main(arg):
    """Main function of the script"""
    client = carla.Client(arg.host, arg.port)
    client.set_timeout(5.0)
    world = client.get_world()

    tur = True
    first = True

    while tur:

        try:
            # Setting the world and the spawn properties
            original_settings = world.get_settings()
            settings = world.get_settings()

            delta = 0.1
            settings.fixed_delta_seconds = delta
            settings.synchronous_mode = True
            world.apply_settings(settings)

            blueprint_library = world.get_blueprint_library()
            vehicle_bp = blueprint_library.filter(arg.filter)[0]

            vehicle_transform0 = world.get_map().get_spawn_points()[0]
            vehicle_transform0.location.z += 3
            vehicle0 = world.spawn_actor(vehicle_bp, vehicle_transform0)

            physics_vehicle0 = vehicle0.get_physics_control()
            car_mass0 = physics_vehicle0.mass

            if (first == True):
                spectator_transform = carla.Transform(vehicle_transform0.location, vehicle_transform0.rotation)
                spectator_transform.location += vehicle_transform0.get_forward_vector() * 20
                spectator_transform.rotation.yaw += 180
                spectator = world.get_spectator()
                spectator.set_transform(spectator_transform)
                first = False
            #------------------------------------------------------------------------------------------------
            vehicle_transform1 = world.get_map().get_spawn_points()[0]
            vehicle_transform1.location.z += 3
            vehicle_transform1.location.x += 3
            vehicle1 = world.spawn_actor(vehicle_bp, vehicle_transform1)

            physics_vehicle1 = vehicle1.get_physics_control()
            car_mass1 = physics_vehicle1.mass
            # ------------------------------------------------------------------------------------------------

            # ------------------------------------------------------------------------------------------------
            vehicle_transform2 = world.get_map().get_spawn_points()[0]
            vehicle_transform2.location.z += 3
            vehicle_transform2.location.x += 6
            vehicle2 = world.spawn_actor(vehicle_bp, vehicle_transform2)

            physics_vehicle2 = vehicle2.get_physics_control()
            car_mass2 = physics_vehicle2.mass
            # ------------------------------------------------------------------------------------------------

            # ------------------------------------------------------------------------------------------------
            vehicle_transform3 = world.get_map().get_spawn_points()[0]
            vehicle_transform3.location.z += 3
            vehicle_transform3.location.x += 9
            vehicle3 = world.spawn_actor(vehicle_bp, vehicle_transform3)

            physics_vehicle3 = vehicle3.get_physics_control()
            car_mass3 = physics_vehicle3.mass
            # ------------------------------------------------------------------------------------------------

            # We let the vehicle stabilize and save the transform to reset it after each test.
            wait(world)

            impulse = 10 * car_mass0

            vehicle0.set_target_velocity(carla.Vector3D(0, 0, 0))
            vehicle1.set_target_velocity(carla.Vector3D(0, 0, 0))
            vehicle2.set_target_velocity(carla.Vector3D(0, 0, 0))
            vehicle3.set_target_velocity(carla.Vector3D(0, 0, 0))

            vehicle0.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle1.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle2.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle3.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            wait(world)

            vehicle0.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle1.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle2.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle3.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            wait(world)

            vehicle0.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle1.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle2.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle3.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            wait(world)

            vehicle0.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle1.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle2.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle3.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            wait(world)

            vehicle0.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle1.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle2.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            vehicle3.add_impulse(carla.Vector3D(1 * impulse, 0, 0))
            wait(world)

            vehicle0.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle1.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle2.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            vehicle3.add_impulse(carla.Vector3D(-1 * impulse, 0, 0))
            wait(world)

            wait(world)

            vehicle0.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))
            vehicle1.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))
            vehicle2.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))
            vehicle3.apply_control(carla.VehicleControl(throttle=0.2, steer=0.0))

            # Impulse/Force at the center of mass of the object
            impulse = 10 * car_mass0

            print("# Adding an Impulse of %f N s" % impulse)
            wait(world)

            vehicle0.add_impulse(carla.Vector3D(0, 10 * impulse, 0))
            vehicle1.add_impulse(carla.Vector3D(0, 10 * impulse, 0))
            vehicle2.add_impulse(carla.Vector3D(0, 10 * impulse, 0))
            vehicle3.add_impulse(carla.Vector3D(0, 10 * impulse, 0))

            wait(world)


        finally:
            world.apply_settings(original_settings)
            vehicle0.destroy()
            vehicle1.destroy()
            vehicle2.destroy()
            vehicle3.destroy()

if __name__ == "__main__":

    argparser = argparse.ArgumentParser(
        description=__doc__)
    argparser.add_argument(
        '--host',
        metavar='H',
        default='localhost',
        help='IP of the host CARLA Simulator (default: localhost)')
    argparser.add_argument(
        '-p', '--port',
        metavar='P',
        default=2000,
        type=int,
        help='TCP port of CARLA Simulator (default: 2000)')
    argparser.add_argument(
        '--filter',
        metavar='PATTERN',
        default='model3',
        help='actor filter (default: "vehicle.*")')
    args = argparser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print(' - Exited by user.')