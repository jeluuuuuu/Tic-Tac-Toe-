from mlf_api import RobotClient
import time
import cv2

import numpy as np

robot = RobotClient("spike.local")
robot.connectWebRTC()
robot.get_frame()
robot.closeWebRTC()

#robot.move_xyz(cx+275,cy+300,0,[30,0,40])


#COMENTARIO DE PRUEBA 1
#COMENTARIO DE PRUEBA 2
#COMENTARIO DE PRUEBA 3
