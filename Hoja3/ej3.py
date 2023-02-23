'''El theremin es un instrumento electrónico basado en osciladores, que consta de dos
antenas metálicas que detectan la posición relativa de las manos del intérprete (thereminista). Esa
posición determina la frecuencia y la amplitud del tono (la frecuencia se controla con una mano y
la amplitud (volumen) con la otra). Puede verse un vídeo en https://www.youtube.com/watch?
v=K6KbEnGnymk
En este ejercicio se implementará un theremin con el modelo de síntesis por wavetable visto en clase
(con este modelo es fácil evitar los pops debidos a los cambios de frecuencia/volumen). Las antenas
se simularán con el ratón: la posición horizontal determina la frecuencia (en un rango prejado,
como [100,10000]) y la vertical, la amplitud en [0,1]. Para el obtener la posición del ratón en una
ventana puede utilizarse la librería pygame. El siguiente código permite obtener la posición del
ratón:
# creacion de una ventana de pygame
import pygame
from pygame.locals import *
WIDTH = 640 # ancho y alto de la ventana de PyGame
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")
...
# obtencion de la posicion del raton
for event in pygame.event.get():
if event.type == pygame.MOUSEMOTION:
mouseX, mouseY = event.pos
pygame.quit()
Pueden utilizarse otros modelos de generación, como la síntesis FM. Deberán evitarse o suavizarse
los pops al cambiar la frecuencia/volumen'''

# theremin

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio

SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 64

class WaveTable:
    def __init__(self):
        self.data = np.sin(2*np.pi*np.arange(SRATE)/SRATE)
        self.n = len(self.data)
        self.i = int(0)

    def nextChunk(self, chunk, frec):
        samples = np.zeros(chunk)
        for k in range(chunk):
            samples[k] = self.data[int(self.i)]
            self.i = int(self.i + frec) % self.n
        return samples

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

# creacion de una ventana de pygame
import pygame
from pygame.locals import *

WIDTH = 640 # ancho y alto de la ventana de PyGame
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Theremin")

mouseX = mouseY = 0

waveTable = WaveTable()

frec = 0
amp = 0

quit = False
while not quit:
    # obtencion de la posicion del raton
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = event.pos
        elif event.type == pygame.QUIT:
            quit = True

    frec = 100 + (2000 - 100) * mouseX / WIDTH
    amp = .1 * mouseY / HEIGHT + amp * .9           #suavizado de volumen
    
    samples = amp * waveTable.nextChunk(CHUNK, frec)   
    stream.write(np.float32(0.9*samples)) 


stream.stop()

pygame.quit()
