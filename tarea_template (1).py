from mlf_api import RobotClient
import time
import cv2

import numpy as np

def show(frame):
    cv2.imshow("XD", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_contours(frame, contours):
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    show(frame)

robot = RobotClient("fluttershy.local")
robot.connectWebRTC()

try:
    frame = robot.get_frame()
    show(frame)

    # Guardar imagen para encontrar buen umbral hsv
    # Vean: utils/getHsv.py
    # cv2.imwrite("frame.jpg", frame)

    # Seleccionar los umbrales
    #(hMin = 51 , sMin = 0, vMin = 0), (hMax = 77 , sMax = 255, vMax = 71)
    hMin, sMin, vMin = 51, 0, 0
    hMax, sMax, vMax = 77,255, 71
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    # Crear la imagen HSV y aplicar el umbral
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    show(mask)

    # Encontrar los contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"N° de Contornos: {len(contours)}")

    # Mostrar los contornos crudos
    show_contours(frame.copy(), contours)

    # Filtrar los contornos por área
    min_area = 1200
    contours = [c for c in contours if cv2.contourArea(c) > min_area]

    # Dibujar los contornos filtrados con rectangulos
    show_contours(frame, contours)

    # Extraemos el centroide del más grande
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])
    print(f"Centroide: ({cx}, {cy})")

    # Dibujar el centroide
    cv2.circle(frame, (cx, cy), 5, (255, 0, 0), -1)
    show(frame)

    # Transformar de coordenadas de la imagen a coordenadas del robot
    # TODO: Rellenar esto
    #desde la esquina izq de la imagen 5 espacios a la derecha y 6 hacia abajo 
    # 1 pixel = 1milimetro
    # esta a -300p en x y -275p en y (ahora estamos en el mismo punto)
    # rotar los ejes => 275p,300p en x,y con respecto al robot

    # Mover el robot con cinemática inversa

    # Su código va aqui


    robot.move_xyz(cx+275,cy+300,0,[30,0,40])
    
    # No lo alcanzamos a terminar y esto es lo que alcanzamos a hacer (no nos funciono en ese momento) 
    # y no alcanzamos a saber bien porque fallaba






except Exception as e: 
    print(e)

finally:
    robot.closeWebRTC()


