import cv2
import numpy as np



#https://github.com/CMU-Perceptual-Computing-Lab/panoptic-toolbox/blob/master/python/panutils.py
def projectPoints(X, K, R, t, Kd):
    """ Projects points X (3xN) using camera intrinsics K (3x3),
    extrinsics (R,t) and distortion parameters Kd=[k1,k2,p1,p2,k3].
    
    Roughly, x = K*(R*X + t) + distortion
    
    See http://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html
    or cv2.projectPoints
    """
    X=np.mat(X)
    R=np.mat(R)
    K=np.mat(K)
    x = np.asarray(R*X + t)
    
    x[0:2,:] = x[0:2,:]/x[2,:]
    
    r = x[0,:]*x[0,:] + x[1,:]*x[1,:]
    
    x[0,:] = x[0,:]*(1 + Kd[0]*r + Kd[1]*r*r + Kd[4]*r*r*r) + 2*Kd[2]*x[0,:]*x[1,:] + Kd[3]*(r + 2*x[0,:]*x[0,:])
    x[1,:] = x[1,:]*(1 + Kd[0]*r + Kd[1]*r*r + Kd[4]*r*r*r) + 2*Kd[3]*x[0,:]*x[1,:] + Kd[2]*(r + 2*x[1,:]*x[1,:])

    x[0,:] = K[0,0]*x[0,:] + K[0,1]*x[1,:] + K[0,2]
    x[1,:] = K[1,0]*x[0,:] + K[1,1]*x[1,:] + K[1,2]
    
    return x

import json

with open("./body3DScene_00001000.json", "r", encoding="utf-8") as poses:
    poses=json.load(poses)
    pose=poses["bodies"][0]["joints19"]

with open("./calibration_160224_haggling1.json", "r", encoding="utf-8") as calibrations:
    calibrations=json.load(calibrations) 
    calibrations=calibrations["cameras"]
    type="hd"
    index=23
    for step,temp in enumerate(calibrations):
        if temp["type"]==type and temp["node"]==index :
            R=temp["R"]
            t=temp["t"]
            K=temp["K"]
            distCoef=temp["distCoef"]
# 将 打印 相机参数 人体姿态 转化为numpy
R=np.array(R)
t=np.array(t)
K=np.array(K)
distCoef=np.array(distCoef)
pose=np.array(pose).reshape(-1,4)[:,0:3]

pose_func=projectPoints(pose.T,K,R,t,distCoef)
pose_cv2,_=cv2.projectPoints(pose.T,R,t,K,distCoef)

# 打印 相机参数 人体姿态 
print("=> 相机外参R:",R)
print("=> 相机外参t:",t)
print("=> 相机内参K:",K)
print("=> 畸变系数d:",distCoef)
print("=> 人体姿态：",pose)

# 打印 转换后的2d坐标
print("=> 自定义函数投影:",pose_func)
print("=> cv2函数投影:",pose_cv2)

# 发现虽然输出的格式不一样，但结果是完全相同的

# 展示 拍摄图片 与 关节点结果
img=cv2.imread("00_23_00001000.jpg")

# 画点
point_size = 1
point_color = (0, 0, 255)  # BGR
thickness = 2
for point in pose_cv2:
    point=point[0]
    point=(int(point[0]),int(point[1]))
    # point = (100, 50)  # 点的坐标。画点实际上就是画半径很小的实心圆。
    cv2.circle(img, point, point_size, point_color, thickness)

cv2.imshow("picture",img)
cv2.waitKey(0)
