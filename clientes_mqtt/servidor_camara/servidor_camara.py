import cv2
import os
import errno
import numpy as np
import paho.mqtt.client as mqtt
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
from datetime import datetime
from flask import Flask, render_template, Response



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


class Camara():
    def __init__(self):
        self.cam = PiCamera(resolution=(640,480),led_pin=13)
        self.cam.vflip = True
        self.cam.hflip = True
        self.cam.led = True
        
        sleep(1)

        self.imagenes, self.etiquetas, self.dicc_etiquetas =recolectarConjunto()
        self.modelo_lbph = cv2.face.LBPHFaceRecognizer_create()
        self.modelo_lbph.train(self.imagenes, self.etiquetas)
        print("Modelos entrenados")

        self.detector = DetectorDeRostros("/home/pi/opencv-3.4.1/data/"
            "haarcascades/haarcascade_frontalface_default.xml")

    def get_frame(self):
        rawCapture = PiRGBArray(self.cam, size=(640, 480))
        for cuadro in self.cam.capture_continuous(rawCapture, 
        format="bgr", 
        use_video_port=True):
            cuadro = cuadro.array
            coordenadas_rostros = self.detector.detectar(cuadro)
            if len(coordenadas_rostros):
                rostros = normalizarRostros(cuadro,coordenadas_rostros)
                for i, rostro in enumerate(rostros): 
                    colector = cv2.face.StandardCollector_create()
                    self.modelo_lbph.predict_collect(rostro, colector)
                    confianza = colector.getMinDist()
                    prediccion = colector.getMinLabel()
                    dibujarRectangulo(cuadro,coordenadas_rostros)
                    etiqueta = mostrarEtiqueta(cuadro,
                        self.dicc_etiquetas[prediccion],
                        (coordenadas_rostros[i][0],
                        coordenadas_rostros[i][1]-10),
                        confianza,110) # Ultimo elemento es el UMBRAL
                    cliente.publish('Seguridad/Camara',
                        'RASPICAM: Persona detectada = ' + str(etiqueta) \
                        +  " - Hora: " + str(datetime.now()),1)
                    directorio = '/home/pi/Pictures/Seguridad/rostro_' \
                                 + etiqueta 
                    try:
                        os.makedirs(directorio)
                    except OSError as e:
                        if e.errno != errno.EEXIST:
                            raise
                    cv2.imwrite(directorio + '/' + etiqueta \
                        +'_'+str(datetime.now()) + '.jpeg',cuadro)
            cv2.putText(cuadro, "Camara de Raspberry Pi",
                        (cuadro.shape[1] - 100, 30), cv2.FONT_HERSHEY_PLAIN, 
                        0.5, (66, 53, 243), 1, cv2.LINE_AA)
            return cuadro


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
        cv2.rectangle(imagen,(x + w_rm, y),(x + w - w_rm, y+h),(150,150,0),3)

def recolectarConjunto():
    imagenes = []
    etiquetas = []
    dicc_etiquetas = {}
    gente = [persona for persona in os.listdir('/home/pi/Pictures/'
        'Detector_Rostros_IA/Personas/')]
    for i,persona in enumerate(gente):
        dicc_etiquetas[i] = persona
        for imagen in os.listdir('/home/pi/Pictures/'
            'Detector_Rostros_IA/Personas/' + persona):
            imagenes.append(cv2.imread('/home/pi/Pictures/'
                'Detector_Rostros_IA/Personas/' + persona +'/' +imagen,0))
            etiquetas.append(i)
    return (imagenes,np.array(etiquetas),dicc_etiquetas)

def mostrarEtiqueta(imagen, texto, coordenadas, confianza, umbral):
    if confianza < umbral:
        etiqueta = texto.capitalize()
    else:
        etiqueta = 'Desconocido'
    cv2.putText(imagen, etiqueta,coordenadas,cv2.FONT_HERSHEY_PLAIN, 1.5, 
        (66, 53, 243), 2)
    return etiqueta


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def micuadro(camara):
    while True:
        frame = camara.get_frame()
        cv2.imwrite('pic.jpg', frame) 
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + \
                open('pic.jpg', 'rb').read() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(micuadro(Camara()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    broker = "127.0.0.1"
    idCliente = "RPi3Peter_Camara"
    cliente = mqtt.Client(idCliente) 
    cliente.connect(broker)
    cliente.loop_start()
    app.run(host='0.0.0.0',threaded=True)
    cliente.loop_stop()
    cliente.disconnect()