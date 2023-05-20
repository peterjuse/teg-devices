
import cv2
import numpy as np
import os
import math
#from matplotlib import pyplot as plt
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep

class DetectorDeRostros(object):
    def __init__(self,xml_path):
        self.clasificador = cv2.CascadeClassifier(xml_path)

    def detectar(self, imagen, solo_grande=True):
        factor_escalado = 1.2
        min_vecinos = 5
        tam_minimo = (30,30)
        solo_grande = True
        banderas = cv2.CASCADE_FIND_BIGGEST_OBJECT | \
                    cv2.CASCADE_DO_ROUGH_SEARCH if solo_grande else \
                    cv2.CASCADE_SCALE_IMAGE
        coordenadas_rostros = self.clasificador.detectMultiScale(imagen,
                            scaleFactor=factor_escalado,
                            minNeighbors=min_vecinos,
                            minSize=tam_minimo,
                            flags=banderas)
        return coordenadas_rostros


def cortarRostros(imagen,coordenadas_rostros):
    rostros = []
    for (x,y,w,h) in coordenadas_rostros:
        w_rm = int(0.2 * w  / 2)
        rostros.append(imagen[y:y+h,x+w_rm:x+w-w_rm])
    return rostros

def normalizarIntensidad(imagenes):
    imagenes_normalizadas = []
    for imagen in imagenes:
        a_color = len(imagen.shape) == 3
        if a_color:
            imagen = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
        imagenes_normalizadas.append(cv2.equalizeHist(imagen))
    return imagenes_normalizadas

def redimensionar(imagenes,tam=(100,100)):
    imagenes_normalizadas = []
    for imagen in imagenes:
        if imagen.shape < tam:
            imagen_normalizada = cv2.resize(imagen,tam, 
                                            interpolation = cv2.INTER_AREA)
        else:
            imagen_normalizada = cv2.resize(imagen,tam, 
                                            interpolation = cv2.INTER_CUBIC)
        imagenes_normalizadas.append(imagen_normalizada)
    return imagenes_normalizadas

def normalizarRostros(cuadro,coordenadas_rostros):
    rostros = cortarRostros(cuadro,coordenadas_rostros)
    rostros = normalizarIntensidad(rostros)
    rostros = redimensionar(rostros)
    return rostros

def dibujarRectangulo(imagen,coordenadas):
    for(x,y,w,h) in coordenadas:
        w_rm = int(0.2 * w / 2)
        cv2.rectangle(imagen,(x + w_rm, y),(x + w - w_rm, y+h),(150,150,0),8)


camara = PiCamera(resolution=(1280,720),led_pin=13)
try:
    camara.vflip = True
    camara.hflip = True
    camara.led = True
    rawCapture = PiRGBArray(camara, size=(1280, 720))
    sleep(1)
    detector = DetectorDeRostros("/home/pi/opencv-3.4.1/data/haarcascades/"
        "haarcascade_frontalface_default.xml")
    carpeta = "/home/pi/Pictures/Detector_Rostros_IA/Personas" \
            +input("Ingrese el nombre de la persona: ").lower()
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    contador = 1
    timer = 0
    cv2.namedWindow("Detector de rostros",cv2.WINDOW_AUTOSIZE)
    for cuadro in camara.capture_continuous(rawCapture, 
        format="bgr", 
        use_video_port=True):
        cuadro = cuadro.array
        coordenadas_rostros = detector.detectar(cuadro)
        if len(coordenadas_rostros) and timer % 700 == 50:
            rostros = normalizarRostros(cuadro,coordenadas_rostros)
            cv2.imwrite(carpeta + '/' +str(contador)+'.jpeg',rostros[0])
            contador += 1
        dibujarRectangulo(cuadro,coordenadas_rostros)
        cv2.imshow('Detector de rostros',cuadro)
        cv2.waitKey(50)
        timer += 50
        rawCapture.truncate(0)
        if contador == 60:
            break
    cv2.destroyAllWindows()
    pass
finally:
    camara.led = False
    camara.close()