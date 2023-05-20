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
        for imagen in os.listdir("/home/pi/Pictures/Detector_Rostros_IA/"
            "Personas/" + persona):
            imagenes.append(cv2.imread("/home/pi/Pictures/Detector_Rostros_IA/"
                                        "Personas/" + persona +'/' +imagen,0))
            etiquetas.append(i)
    return (imagenes,np.array(etiquetas),dicc_etiquetas)

def mostrarEtiqueta(imagen, texto, coordenadas, confianza, umbral):
    if confianza < umbral:
        cv2.putText(imagen, texto.capitalize(),
                    coordenadas,
                    cv2.FONT_HERSHEY_PLAIN, 3, (66, 53, 243), 2)
    else:
        cv2.putText(imagen, "Desconocido",
                    coordenadas,
                    cv2.FONT_HERSHEY_PLAIN, 3, (66, 53, 243), 2)


cv2.namedWindow("Detector de rostros", cv2.WINDOW_AUTOSIZE)
#cv2.setWindowProperty("Detector de rostros", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
imagenes, etiquetas, dicc_etiquetas = recolectarConjunto()
modelo_lbph = cv2.face.LBPHFaceRecognizer_create()
modelo_lbph.train(imagenes, etiquetas)
print("Modelos entrenados")
camara = PiCamera(resolution=(640,480),led_pin=13)
try:
    camara.vflip = True
    camara.hflip = True
    camara.led = True
    rawCapture = PiRGBArray(camara, size=(640, 480))
    sleep(1)
    detector = DetectorDeRostros("/home/pi/opencv-3.4.1/data/haarcascades/"
                                    "haarcascade_frontalface_default.xml")
    cv2.namedWindow("Detector de rostros",cv2.WINDOW_AUTOSIZE)
    for cuadro in camara.capture_continuous(rawCapture, 
        format="bgr", 
        use_video_port=True):
        cuadro = cuadro.array
        coordenadas_rostros = detector.detectar(cuadro)
        if len(coordenadas_rostros):
            rostros = normalizarRostros(cuadro,coordenadas_rostros)
            for i, rostro in enumerate(rostros): 
                colector = cv2.face.StandardCollector_create()
                modelo_lbph.predict_collect(rostro, colector)
                confianza = colector.getMinDist()
                prediccion = colector.getMinLabel()
                print("Prediccion: " \
                    + dicc_etiquetas[prediccion].capitalize() \
                    +"  Confianza: " + str(round(confianza)))
            dibujarRectangulo(cuadro,coordenadas_rostros)
            mostrarEtiqueta(cuadro,dicc_etiquetas[prediccion],
                (coordenadas_rostros[i][0],coordenadas_rostros[i][1]-10),
                confianza,140) # Ultimo elemento es el UMBRAL
            cv2.putText(cuadro, "ESC para salir", (5, cuadro.shape[0] - 5),
                                cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2, 
                                cv2.LINE_AA)
            cv2.putText(cuadro, "Raspberry Pi Camara", 
                        (cuadro.shape[1] - 100, 30),
                        cv2.FONT_HERSHEY_PLAIN, 1.3, 
                        (66, 53, 243), 2, cv2.LINE_AA)
        cv2.imshow('Detector de rostros',cuadro)
        rawCapture.truncate(0)
        if cv2.waitKey(25) & 0xFF == 27:
            break
finally:
    camara.led = False
    pass