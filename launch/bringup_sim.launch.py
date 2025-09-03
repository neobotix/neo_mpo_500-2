# Neobotix GmbH
# Author: Pradheep Padmanabhan
# Contributor: Adarsh Karan K P

import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, LaunchContext
from launch.actions import (
    DeclareLaunchArgument, 
    IncludeLaunchDescription,
    OpaqueFunction
    )
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import os

def execution_stage(context: LaunchContext,
                    robot_namespace,
                    world,
                    arm_type,
                    imu_enable,
                    scanner_type,
                    gripper_type,
                    legacy):    

    launch_actions = []

    robot_type = "mpo_500"
    scanner_typ = str(scanner_type.perform(context))
    world_name = str(world.perform(context))
    use_legacy = str(legacy.perform(context))

    if (use_legacy.lower() == "true" and scanner_typ == "sick_nanoscan3"):
        print("Invalid choice, Legacy mode only supports sick_s300 or sick_microscan3")
        print("Exiting")
        return

    if (use_legacy.lower() == "false"):
        scanner_typ = "sick_nanoscan3"

    # Launch bringup_sim file from mp_bringup package
    bringup_sim_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('mp_bringup'), 'launch', 'bringup_sim.launch.py')
        ),
        launch_arguments={
            'robot_namespace': robot_namespace,
            'robot_type': robot_type,
            'world': world_name,
            'arm_type': arm_type,
            'imu_enable': imu_enable,
            'scanner_type': scanner_typ,
            'gripper_type': gripper_type,
            'use_legacy': legacy
        }.items(),
    )

    # Add the launch command to the launch actions
    launch_actions.append(bringup_sim_launch_cmd)

    return launch_actions

def generate_launch_description():

    declare_namespace_cmd = DeclareLaunchArgument(
            'robot_namespace', default_value='', description='Top-level namespace'
        )

    declare_world_name_arg = DeclareLaunchArgument(
            'world',
            default_value='neo_workshop',
            choices=['', 'neo_workshop'],
            description='Simulation world to load'
        )

    declare_arm_type_cmd = DeclareLaunchArgument(
            'arm_type', default_value='',
            choices=['', 'ur5', 'ur10', 'ur5e', 'ur10e', 'ec66', 'cs66'],
            description='Arm Types\n\t'        
        )

    declare_imu_cmd = DeclareLaunchArgument(
            'imu_enable', default_value='False',
            description='Enable IMU - Options: True/False'
        )

    declare_scanner_type_cmd = DeclareLaunchArgument(
            'scanner_type', default_value='sick_s300',
            choices=['', 'sick_s300', 'sick_microscan3', 'sick_nanoscan3'],
            description='Type of laser scanner to use\n\t'
        )

    declare_gripper_type_cmd = DeclareLaunchArgument(
            'gripper_type', default_value='',
            choices=['', '2f_140', '2f_85'], # epick gripper not supported in simulation yet
            description='Gripper Types\n\t'
        )

    declare_use_legacy_cmd = DeclareLaunchArgument(
            'use_legacy', default_value='False',
            description='Set legacy to True if you are using the old model'
        )

    opq_function = OpaqueFunction(
        function=execution_stage,
        args=[
            LaunchConfiguration('robot_namespace'),
            LaunchConfiguration('world'),
            LaunchConfiguration('arm_type'),
            LaunchConfiguration('imu_enable'),
            LaunchConfiguration('scanner_type'),
            LaunchConfiguration('gripper_type'),
            LaunchConfiguration('use_legacy')
        ])

    return LaunchDescription([
        declare_namespace_cmd,
        declare_world_name_arg,
        declare_arm_type_cmd,
        declare_imu_cmd,
        declare_scanner_type_cmd,
        declare_gripper_type_cmd,
        declare_use_legacy_cmd,
        opq_function
    ])
