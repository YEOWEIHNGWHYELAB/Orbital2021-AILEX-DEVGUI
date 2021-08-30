#-----------------------------------------------------------------------
import glob
import os
import sys
import random
import time
import numpy as np
import cv2
import keyboard

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
#-----------------------------------------------------------------------

IM_WIDTH = 640
IM_HEIGHT = 480

actor_list = []
terminate = False

def process_img(image):
    # Changing the data format...
    i = np.array(image.raw_data) # raw_data is just a flatten array...
    i2 = i.reshape((IM_HEIGHT, IM_WIDTH, 4)) # It is RGBA, don't forget the last parameter!
    i3 = i2[:, :, :3] # We take everything of i2 but exclude the Alpha value of the RGBA.

    # Shows visual of the camera.
    cv2.imshow("", i3) # Title is "" which is nothing,
    cv2.waitKey(1) # 1ms

    # Normalize it to between 0 and 1 since in Deep-Learning the data taken in is usually just between 0 and 1.
    return i3 / 255.0

if __name__ == "__main__":
    # Try connect to server.
    try:
        # Server Connect.
        client = carla.Client("localhost", 2000)
        client.set_timeout(5.0)
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        # Select Car.
        AgentCarModel = blueprint_library.filter("model3")[0]
        print(AgentCarModel)

        # Available Spawn Points.
        spawn_point = random.choice(world.get_map().get_spawn_points())

        # Agent Car Initialization.
        agentCar = world.spawn_actor(AgentCarModel, spawn_point)
        agentCar.set_autopilot(False)
        agentCar.apply_control(carla.VehicleControl(throttle = 0.0, steer = 0.0))
        actor_list.append(agentCar)

        # ------------------------------------------------------------------------------------
        # Setup Front RGB camera.
        cam_bp = blueprint_library.find("sensor.camera.rgb")
        cam_bp.set_attribute("image_size_x", f"{IM_WIDTH}")
        cam_bp.set_attribute("image_size_y", f"{IM_HEIGHT}")
        cam_bp.set_attribute("fov", "110") # Set field of view.
        # ------------------------------------------------------------------------------------

        #------------------------------------------------------------------------------------
        # Attach Front RGB camera to the Agent.
        spawn_point = carla.Transform(carla.Location(x = 2.5, z = 0.7))
        centerRGBCam = world.spawn_actor(cam_bp, spawn_point, attach_to = agentCar)
        actor_list.append(centerRGBCam)
        # ------------------------------------------------------------------------------------

        # Get data from sensor and displaying it.
        centerRGBCam.listen(lambda data: process_img(data))

        # Main loop.
        while not terminate:
            if keyboard.is_pressed('z'):
                terminate = True

            agentCar.apply_control(carla.VehicleControl(throttle = 0.5, steer = 0.0))

    # Clean up
    finally:
        for actor in actor_list:
            actor.destroy()
        print("All cleaned up!")