import cv2
import numpy as np
import os
import math
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

def recolectarConjunto():
    imagenes = []
    etiquetas = []
    dicc_etiquetas = {}
    gente = [persona for persona in os.listdir("/home/pi/Pictures/"
                                            "Detector_Rostros_IA/Personas/")]
    for i,persona in enumerate(gente):
        dicc_etiquetas[i] = persona
        for imagen in os.listdir("/home/pi/Pictures/"
            "Detector_Rostros_IA/Personas/" + persona):
            imagenes.append(cv2.imread("/home/pi/Pictures/Detector_Rostros_IA/"
                "Personas/" + persona +'/' +imagen,0))
            etiquetas.append(i)
    return (imagenes,np.array(etiquetas),dicc_etiquetas)


imagenes, etiquetas, dicc_etiquetas = recolectarConjunto()
#modelo_eig = cv2.face.createEigenFaceRecognizer()
modelo_eig = cv2.face.EigenFaceRecognizer_create()
modelo_eig.train(imagenes, etiquetas)
modelo_fisher = cv2.face.FisherFaceRecognizer_create()
modelo_fisher.train(imagenes, etiquetas)
modelo_lbph = cv2.face.LBPHFaceRecognizer_create()
modelo_lbph.train(imagenes, etiquetas)
print("Modelos entrenados")
camara = PiCamera(resolution=(1280,720),led_pin=13)
try:
    camara.vflip = True
    camara.hflip = True
    camara.led = True
    rawCapture = PiRGBArray(camara, size=(1280, 720))
    sleep(1)
    detector = DetectorDeRostros("/home/pi/opencv-3.4.1/data/haarcascades/"
        "haarcascade_frontalface_default.xml")
    camara.capture(rawCapture,format='bgr')
    cuadro = rawCapture.array
    coordenadas_rostros = detector.detectar(cuadro)
    rostros = normalizarRostros(cuadro,coordenadas_rostros)
    rostro = rostros[0]
    colector = cv2.face.StandardCollector_create()

    modelo_eig.predict_collect(rostro, colector)
    conf = colector.getMinDist()
    pred = colector.getMinLabel()
    print("Eigen -> Prediccion: " + dicc_etiquetas[pred].capitalize() +\
    "  Confianza: " + str(round(conf)))

    modelo_fisher.predict_collect(rostro, colector)
    conf = colector.getMinDist()
    pred = colector.getMinLabel()
    print("Fisher -> Prediccion: " +\
    dicc_etiquetas[pred].capitalize() + "  Confianza: " + str(round(conf)))

    modelo_lbph.predict_collect(rostro, colector)
    conf = colector.getMinDist()
    pred = colector.getMinLabel()
    print("LBPH  -> Prediccion: " + dicc_etiquetas[pred].capitalize() +\
    "  Confianza: " + str(round(conf)))

finally:
    camara.led = False
    pass

