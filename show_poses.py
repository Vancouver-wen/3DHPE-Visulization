import cv2
import json
import matplotlib.pyplot as plt
import numpy as np  

with open("./body3DScene_00001000.json", "r", encoding="utf-8") as poses:
    poses=json.load(poses)
    poses=poses["bodies"]

from MyShow import Myshow3d
myplot3d=Myshow3d()
myplot3d.draw_bodies(poses=poses)

hd_cameras=[]
with open("./calibration_160224_haggling1.json", "r", encoding="utf-8") as calibrations:
    calibrations=json.load(calibrations) 
    calibrations=calibrations["cameras"]
    type="hd"
    index=int
    for step,temp in enumerate(calibrations):
        if temp["type"]==type:
            position=temp["t"]
            rotation=temp["R"]
            position=np.array(position)
            rotation=np.array(rotation)
            rotation_inv=np.linalg.inv(rotation)
            position= -np.matmul(rotation_inv,position)
            point3d=( float(position[0][0]),float(position[2][0]),-float(position[1][0]), )
            hd_cameras.append(point3d)

myplot3d.scatters(hd_cameras)
myplot3d.show()

