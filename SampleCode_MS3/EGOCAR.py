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

        # --------------
        # Spawn ego vehicle
        # --------------
        ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
        ego_bp.set_attribute('role_name', 'ego')
        print('\nEgo role_name is set')
        ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
        ego_bp.set_attribute('color', ego_color)
        print('\nEgo color is set')

        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)

        if 0 < number_of_spawn_points:
            random.shuffle(spawn_points)
            ego_transform = spawn_points[0]
            ego_vehicle = world.spawn_actor(ego_bp, ego_transform)
            print('\nEgo is spawned')
        else:
            logging.warning('Could not found any spawn points')

        # --------------
        # Spectator on ego position
        # --------------
        spectator = world.get_spectator()
        world_snapshot = world.wait_for_tick()
        spectator.set_transform(ego_vehicle.get_transform())

        # --------------
        # Spawn attached RGB camera
        # --------------
        cam_bp = None
        cam_bp = world.get_blueprint_library().find('sensor.camera.rgb')
        cam_bp.set_attribute("image_size_x", str(1920))
        cam_bp.set_attribute("image_size_y", str(1080))
        cam_bp.set_attribute("fov", str(105))
        cam_location = carla.Location(2, 0, 1)
        cam_rotation = carla.Rotation(0, 180, 0)
        cam_transform = carla.Transform(cam_location, cam_rotation)
        ego_cam = world.spawn_actor(cam_bp, cam_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)
        ego_cam.listen(lambda image: image.save_to_disk('tutorial/output/%.6d.jpg' % image.frame))

        # --------------
        # Add collision sensor to ego vehicle.
        # --------------

        col_bp = world.get_blueprint_library().find('sensor.other.collision')
        col_location = carla.Location(0, 0, 0)
        col_rotation = carla.Rotation(0, 0, 0)
        col_transform = carla.Transform(col_location, col_rotation)
        ego_col = world.spawn_actor(col_bp, col_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)


        def col_callback(colli):
            print("Collision detected:\n" + str(colli) + '\n')


        ego_col.listen(lambda colli: col_callback(colli))

        # --------------
        # Add Lane invasion sensor to ego vehicle.
        # --------------

        lane_bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
        lane_location = carla.Location(0, 0, 0)
        lane_rotation = carla.Rotation(0, 0, 0)
        lane_transform = carla.Transform(lane_location, lane_rotation)
        ego_lane = world.spawn_actor(lane_bp, lane_transform, attach_to=ego_vehicle,
                                     attachment_type=carla.AttachmentType.Rigid)


        def lane_callback(lane):
            print("Lane invasion detected:\n" + str(lane) + '\n')


        ego_lane.listen(lambda lane: lane_callback(lane))

        # --------------
        # Add Obstacle sensor to ego vehicle.
        # --------------

        obs_bp = world.get_blueprint_library().find('sensor.other.obstacle')
        obs_bp.set_attribute("only_dynamics", str(True))
        obs_location = carla.Location(0, 0, 0)
        obs_rotation = carla.Rotation(0, 0, 0)
        obs_transform = carla.Transform(obs_location, obs_rotation)
        ego_obs = world.spawn_actor(obs_bp, obs_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)


        def obs_callback(obs):
            print("Obstacle detected:\n" + str(obs) + '\n')


        ego_obs.listen(lambda obs: obs_callback(obs))

        # --------------
        # Add GNSS sensor to ego vehicle.
        # --------------

        gnss_bp = world.get_blueprint_library().find('sensor.other.gnss')
        gnss_location = carla.Location(0, 0, 0)
        gnss_rotation = carla.Rotation(0, 0, 0)
        gnss_transform = carla.Transform(gnss_location, gnss_rotation)
        gnss_bp.set_attribute("sensor_tick", str(3.0))
        ego_gnss = world.spawn_actor(gnss_bp, gnss_transform, attach_to=ego_vehicle,
                                     attachment_type=carla.AttachmentType.Rigid)


        def gnss_callback(gnss):
            print("GNSS measure:\n" + str(gnss) + '\n')


        ego_gnss.listen(lambda gnss: gnss_callback(gnss))

        # --------------
        # Add IMU sensor to ego vehicle.
        # --------------

        imu_bp = world.get_blueprint_library().find('sensor.other.imu')
        imu_location = carla.Location(0, 0, 0)
        imu_rotation = carla.Rotation(0, 0, 0)
        imu_transform = carla.Transform(imu_location, imu_rotation)
        imu_bp.set_attribute("sensor_tick", str(3.0))
        ego_imu = world.spawn_actor(imu_bp, imu_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)


        def imu_callback(imu):
            print("IMU measure:\n" + str(imu) + '\n')


        ego_imu.listen(lambda imu: imu_callback(imu))

        # --------------
        # Add a Depth camera to ego vehicle.
        # --------------
        depth_cam = None
        depth_bp = world.get_blueprint_library().find('sensor.camera.depth')
        depth_location = carla.Location(2, 0, 1)
        depth_rotation = carla.Rotation(0, 180, 0)
        depth_transform = carla.Transform(depth_location, depth_rotation)
        depth_cam = world.spawn_actor(depth_bp, depth_transform, attach_to=ego_vehicle,
                                      attachment_type=carla.AttachmentType.Rigid)
        # This time, a color converter is applied to the image, to get the semantic segmentation view
        depth_cam.listen(lambda image: image.save_to_disk('tutorial/new_depth_output/%.6d.jpg' % image.frame,
                                                          carla.ColorConverter.LogarithmicDepth))

        # --------------
        # Add a new semantic segmentation camera to my ego
        # --------------
        sem_cam = None
        sem_bp = world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
        sem_bp.set_attribute("image_size_x", str(1920))
        sem_bp.set_attribute("image_size_y", str(1080))
        sem_bp.set_attribute("fov", str(105))
        sem_location = carla.Location(2, 0, 1)
        sem_rotation = carla.Rotation(0, 180, 0)
        sem_transform = carla.Transform(sem_location, sem_rotation)
        sem_cam = world.spawn_actor(sem_bp, sem_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)
        # This time, a color converter is applied to the image, to get the semantic segmentation view
        sem_cam.listen(lambda image: image.save_to_disk('tutorial/new_sem_output/%.6d.jpg' % image.frame,
                                                        carla.ColorConverter.CityScapesPalette))

        # --------------
        # Add a new LIDAR sensor to my ego
        # --------------
        lidar_cam = None
        lidar_bp = world.get_blueprint_library().find('sensor.lidar.ray_cast')
        lidar_bp.set_attribute('channels', str(32))
        lidar_bp.set_attribute('points_per_second', str(90000))
        lidar_bp.set_attribute('rotation_frequency', str(40))
        lidar_bp.set_attribute('range', str(20))
        lidar_location = carla.Location(0, 0, 2)
        lidar_rotation = carla.Rotation(0, 0, 0)
        lidar_transform = carla.Transform(lidar_location, lidar_rotation)
        lidar_sen = world.spawn_actor(lidar_bp, lidar_transform, attach_to=ego_vehicle)
        lidar_sen.listen(
            lambda point_cloud: point_cloud.save_to_disk('tutorial/new_lidar_output/%.6d.ply' % point_cloud.frame))

        # --------------
        # Add a new radar sensor to my ego
        # --------------
        rad_cam = None
        rad_bp = world.get_blueprint_library().find('sensor.other.radar')
        rad_bp.set_attribute('horizontal_fov', str(35))
        rad_bp.set_attribute('vertical_fov', str(20))
        rad_bp.set_attribute('range', str(20))
        rad_location = carla.Location(x=2.0, z=1.0)
        rad_rotation = carla.Rotation(pitch=5)
        rad_transform = carla.Transform(rad_location, rad_rotation)
        rad_ego = world.spawn_actor(rad_bp, rad_transform, attach_to=ego_vehicle,
                                    attachment_type=carla.AttachmentType.Rigid)


        def rad_callback(radar_data):
            velocity_range = 7.5  # m/s
            current_rot = radar_data.transform.rotation
            for detect in radar_data:
                azi = math.degrees(detect.azimuth)
                alt = math.degrees(detect.altitude)
                # The 0.25 adjusts a bit the distance so the dots can
                # be properly seen
                fw_vec = carla.Vector3D(x=detect.depth - 0.25)
                carla.Transform(
                    carla.Location(),
                    carla.Rotation(
                        pitch=current_rot.pitch + alt,
                        yaw=current_rot.yaw + azi,
                        roll=current_rot.roll)).transform(fw_vec)

                def clamp(min_v, max_v, value):
                    return max(min_v, min(value, max_v))

                norm_velocity = detect.velocity / velocity_range  # range [-1, 1]
                r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
                g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
                b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
                world.debug.draw_point(
                    radar_data.transform.location + fw_vec,
                    size=0.075,
                    life_time=0.06,
                    persistent_lines=False,
                    color=carla.Color(r, g, b))


        rad_ego.listen(lambda radar_data: rad_callback(radar_data))

    # Clean up
    finally:
        for actor in actor_list:
            actor.destroy()
        print("All cleaned up!")