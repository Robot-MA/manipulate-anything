import numpy as np
import torch
from m2t2.rlbench_utils import gripper_pose_from_rlbench, gripper_pose_to_rlbench, rotation_to_rlbench
from scipy.spatial import KDTree

def retract_action(obs, cfg):
    action = obs['gripper_matrix']
    gripper_open = 0  # Ensure the gripper remains closed
    # Retract the gripper by moving it backwards
    trans = action[:3, 3] - 0.1 * action[:3, 2]
    action[:3, 3] = trans
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def press_action(obs):
    action = obs['gripper_matrix']
    gripper_open = obs['gripper_open']
    message = 'Retract'
    trans = action[:3, 3] + 0.1 * action[:3, 2]
    rot = obs['gripper_pose'][3:]
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def rotate_gripper_y(obs, quaternion_multiply):
    action = obs['gripper_matrix']
    gripper_open = 0  # Ensure the gripper remains closed
    angle_y = np.radians(45)
    rotation_quaternion = [np.cos(angle_y / 2), 0, np.sin(angle_y / 2), 0]
    rot = quaternion_multiply(obs['gripper_pose'][3:], rotation_quaternion)
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def sweep_action(obs, sweep_direction='x', sweep_amount=0.1):
    action = obs['gripper_matrix']
    gripper_open = 0  # Ensure the gripper remains closed
    if sweep_direction == 'x':
        action[0, 3] += sweep_amount
    elif sweep_direction == 'y':
        action[1, 3] += sweep_amount
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def rotate_gripper_z(obs, quaternion_multiply, angle=-60):
    action = obs['gripper_matrix']
    gripper_open = 0  # Ensure the gripper remains closed
    angle_z = np.radians(angle)
    rotation_quaternion = [np.cos(angle_z / 2), 0, 0, np.sin(angle_z / 2)]
    rot = quaternion_multiply(obs['gripper_pose'][3:], rotation_quaternion)
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def rotate_gripper_x(obs, quaternion_multiply, angle=45):
    action = obs['gripper_matrix']
    gripper_open = 0  # Ensure the gripper remains closed
    angle_x = np.radians(angle)
    rotation_quaternion = [np.cos(angle_x / 2), np.sin(angle_x / 2), 0, 0]
    rot = quaternion_multiply(obs['gripper_pose'][3:], rotation_quaternion)
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def drop_action(obs):
    action = obs['gripper_matrix']
    gripper_open = 1  # Open the gripper to drop the object
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def close_gripper_action(obs, quaternion_multiply):
    action = obs['gripper_matrix']
    gripper_open = 1  # Ensure the gripper remains closed
    action[1, 3] += 0.3
    action[2, 3] += 0.1
    angle_x = np.radians(-45)
    rotation_quaternion = [np.cos(angle_x / 2), np.sin(angle_x / 2), 0, 0]
    rot = quaternion_multiply(obs['gripper_pose'][3:], rotation_quaternion)
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred

def open_gripper_action(obs, quaternion_multiply):
    action = obs['gripper_matrix']
    gripper_open = obs['gripper_open']  # Current state of the gripper
    action[1, 3] -= 0.4
    action[2, 3] += 0.3
    angle_x = np.radians(45)
    rotation_quaternion = [np.cos(angle_x / 2), np.sin(angle_x / 2), 0, 0]
    rot = quaternion_multiply(obs['gripper_pose'][3:], rotation_quaternion)
    pred = gripper_pose_from_rlbench(action)
    return action, gripper_open, pred
