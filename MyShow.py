import cv2
import json
import matplotlib.pyplot as plt
import numpy as np 

class Myplot3d():
    def __init__(self):
        import matplotlib.pyplot as plt 
        from mpl_toolkits import mplot3d 
        self.fig = plt.figure(figsize = (10, 7)) 
        self.ax=mplot3d.Axes3D(self.fig) 
        self.ax.set_xlim3d(-200,200)
        self.ax.set_ylim3d(-200,200)
        self.ax.set_zlim3d(0,300)
        self.ax.set_xlabel("x axis")
        self.ax.set_ylabel("y axis")
        self.ax.set_zlabel("x zxis")
        self.ax.scatter3D(float(0), float(0), float(0), color="red") 
        #plt.gca().set_box_aspect((3, 5, 2))  # 当x、y、z轴范围之比为3:5:2时
        # plt.gca().set_box_aspect((4, 4, 3))

    def scatter(self,point3d,color): 
        self.ax.scatter3D(float(point3d[0]), float(point3d[1]), float(point3d[2]), color = color)  
    def scatters(self,points3d):
        """args:
        points3d is a list of tuples. 
        tuple=(x_coordinate,y_coordinate,z_coordinate)
        """
        for point3d in points3d:
            self.scatter(point3d,"grey")
    def line(self,point3d_1,point3d_2,color):
        line_x=np.array([float(point3d_1[0]),float(point3d_2[0])])
        line_y=np.array([float(point3d_1[1]),float(point3d_2[1])])
        line_z=np.array([float(point3d_1[2]),float(point3d_2[2])])
        self.ax.plot3D(line_x,line_y,line_z,color)
    def lines(self,pointpairs):
        """args:
        pointpairs is a list of tuples. 
        tuples=(point3d_1,point3d_2). point3d is a tuple.
        point3d=(x_coordinate,y_coordinate,z_coordinate)
        """
        for point3d_1,point3d_2 in pointpairs:
            self.line(point3d_1,point3d_2,"grey")
    def show(self,title="3D scatter plot"):
        plt.title(title)  
        plt.show() 
    # TEST
    def test_scatters(self,):
        z = np.random.randint(80, size =(55))  
        x = np.random.randint(60, size =(55))  
        y = np.random.randint(64, size =(55)) 
        points3d=[]
        for i in range(55):
            points3d.append( (x[i],y[i],z[i]) )
        self.scatters(points3d)
    def test_lines(self,):
        pointpair=[]
        pointpair.append( ((0,0,0),(100,100,100)) )
        pointpair.append( ((-100,-100,-100),(0,0,0)) )
        self.lines(pointpair)


class Myshow3d(Myplot3d):
    def __init__(self):
        super().__init__()
        self.panoptic_bones_def = [
            [0, 1], [0, 2],  # trunk
            [0, 3], [3, 4], [4, 5],  # left arm
            [0, 9], [9, 10], [10, 11],  # right arm
            [2, 6], [6, 7], [7, 8],  # left leg
            [2, 12], [12, 13], [13, 14],  # right leg
        ]
    def draw_body(self,point3ds,edges):
        pointpairs=[]
        for edge in edges:
            pointpairs.append( (point3ds[edge[0]],point3ds[edge[1]]) )
        self.lines(pointpairs)
    def draw_bodies(self,poses):
        """输入样例：
        [
        { "id": 0, "joints19": [37.482, -138.047, 62.0985, 0.613953, 34.5987, -151.174, 44.4078, 0.545837, 32.1764, -83.2804, 56.5939, 0.369202, 53.2297, -136.168, 59.5709, 0.43335, 57.562, -111.273, 52.6583, 0.3573, 45.0171, -117.013, 34.9161, 0.354065, 42.6458, -82.3876, 55.5034, 0.33844, 45.5505, -43.8638, 59.3359, 0.404053, 48.2481, -9.87553, 63.4798, 0.519226, 21.2823, -139.089, 64.1216, 0.540466, 12.2628, -114.515, 63.7989, 0.490234, 17.8035, -116.212, 42.491, 0.339417, 21.7071, -84.1731, 57.6844, 0.341003, 18.579, -47.0052, 57.1199, 0.394897, 18.9895, -10.8257, 57.6605, 0.542419, 37.6105, -154.719, 44.3409, 0.408142, 44.6142, -157.091, 51.0789, 0.383728, 32.1702, -155.426, 45.7755, 0.461487, 29.8345, -157.753, 54.7664, 0.486023]},
        { "id": 1,"joints19": [107.41, -134.815, -68.5295, 0.622559, 96.4937, -154.887, -58.1142, 0.617554, 101.938, -80.0638, -64.7326, 0.378113, 96.5186, -135.522, -81.2809, 0.504272, 93.0374, -108.422, -86.0067, 0.350403, 88.4061, -87.5321, -75.1575, 0.279541, 95.7582, -80.3518, -73.3317, 0.357788, 102.644, -43.6313, -79.6496, 0.373901, 103.63, -9.94175, -82.7598, 0.450989, 118.347, -133.794, -56.0669, 0.498962, 120.252, -105.723, -49.6593, 0.419556, 113.181, -81.5887, -44.693, 0.424927, 108.118, -79.7759, -56.1336, 0.368286, 114.908, -43.2314, -57.9979, 0.429321, 114.253, -9.47867, -56.3847, 0.474243, 96.115, -158.823, -62.2445, 0.521912, 100.073, -156.88, -71.7589, 0.375671, 100.658, -158.184, -57.0163, 0.554565, 110.587, -155.426, -59.4075, 0.426575]},
        { "id": 2,"joints19": [-67.0101, -146.56, 2.95995, 0.691467, -50.4429, -164.704, 0.189158, 0.561707, -61.7185, -91.7512, 1.55607, 0.375183, -65.2855, -147.514, 19.9409, 0.521362, -51.4539, -126.456, 35.7198, 0.474121, -26.6777, -132.812, 31.4961, 0.430908, -59.5367, -91.7566, 11.7572, 0.33197, -62.3741, -50.9528, 11.6894, 0.40387, -62.0549, -10.8004, 12.4692, 0.493347, -69.4677, -146.098, -14.1295, 0.552063, -68.9392, -121.396, -32.5725, 0.556824, -46.3788, -131.514, -36.0474, 0.527832, -63.9002, -91.7457, -8.64507, 0.341675, -67.5315, -50.5619, -7.34732, 0.398926, -70.5452, -9.81809, -6.06827, 0.511536, -52.2811, -168.382, 3.79442, 0.47052, -61.7241, -167.041, 9.47161, 0.433777, -53.0538, -168.155, -2.74377, 0.454529, -63.3842, -166.595, -6.41483, 0.495728]}
        ]
        """
        for pose in poses:
            pose=pose["joints19"]
            pose=np.array(pose).reshape((-1,4))
            joints=[]
            for joint in pose:
                joints.append( (joint[0],joint[2],-joint[1]) )
            self.draw_body(joints,self.panoptic_bones_def)
        pass
    def draw_cameras():
        pass
    