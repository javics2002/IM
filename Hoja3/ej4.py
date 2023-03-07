'''En este ejercicio implementaremos un sintetizador armónico, i.e., un sintetizador que produce acordes 
(combinaciones de notas simultáneas) en vez de notas aisladas como explicaremos más adelante.
Nuestro sintetizador utilizará la escala diatónica (las teclas blancas del piano: c-d-e-f-g-a-b-c) y 
podrá utilizar dos tipos de afinación, justa y temperada, según la siguiente tabla:
A B C D E F G a
Afinación justa 440 495 550 586.67 660 733.33 825 880
Relaciones 1 9/8 5/4 4/3 3/2 5/3 15/8 2
Afinación temperada 440 493.88 554.36 587.33 659.26 739.99 830.61 880
Relaciones 1 2^2/12 2^3/12 2^5/12 2^7/12 2^8/12 2^10/12 2^12/12 = 2
Recordemos que con esta tabla podemos obtener todas las octavas: podemos subir una nota una
octava multiplicando su frecuencia por 2, y bajarla una octava dividiendo entre dos.
Nuestro sintetizador producirá las tríadas (acordes) elementales de la escala diatónica que se forman
a partir de una nota cualquiera, añadiendo otras dos por encima en saltos de 2. Por ejemplo, a partir
de la nota C obtenemos el acorde C con las notas C-E-G, y a partir de la nota A obtenemos el
acorde A con las notas A-C-E. Como es habitual, utilizaremos las teclas zxcvbnm para una octava
(baja) y qwertyu para la superior (alta). Cuando se pulse z sonará el acorde C.
Como generador de sonido podemos utilizar el modelo de síntesis FM combinado con las envolventes
ADSR (ambos vistos en clase).
Discusión: ¿Qué afinación suena mejor, la justa o la temperada?'''

import numpy as np
import sounddevice as sd
import kbhit    

SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024

just = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2]
temperate = [1, np.power(2, 2/12), np.power(2, 3/12), np.power(2, 5/12), np.power(2, 7/12), np.power(2, 8/12), np.power(2, 10/12), 2]

# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
def oscFM(frecs,frame):
    # sin(2πfc+βsin(2πfm))  
    chunk = np.arange(CHUNK)+frame
    samples = np.zeros(CHUNK)+frame
    # recorremos en orden inverso
    
    for i in range(len(frecs)-1,-1,-1):
        samples = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/SRATE + samples, dtype=np.float32)
    return samples

keys = "zxcvbnmqwertyu"

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

armonicos = [0, 0, 0]

def getNote(index, escala):
    if escala:
        frec = 440 * just[index % 7]
    else:
        frec = 440 * temperate[index % 7]
    while index > 6:
        frec *= 2
        index -= 7
    return ((frec, 0.8), (1.5 * frec, 0.5), (2 * frec, 0.2))

armonicos = [0, 2, 4]

class ADSR:
    def __init__(self, attack, decay, sustain, release):
        self.values = np.linspace(0, 1, int(attack * SRATE))
        np.append(self.values, np.linspace(1, .7, int(decay * SRATE)))
        np.append(self.values, np.linspace(.7, .7, int(sustain * SRATE)))
        np.append(self.values, np.linspace(.7, 0, int(release * SRATE)))
        self.start()

    def start(self):
        self.t = 0

    def update(self, dt):
        self.t += dt

    def get(self):
        if(self.t > self.values.size):
            return 0
        else:
            return self.values[self.t]

kb = kbhit.KBHit()
adsr = ADSR(.2, .2, 1, 1.5)
c=''
frame = 0
escala = True
print("Teclado = zxcvbnmqwertyu     O = cambiar de escala justa a temperada")
while c != 'p':
    adsr.update(CHUNK)

    if kb.kbhit():
        c = kb.getch()
        if c == 'o':
            escala = not escala
        elif keys.count(c):
            adsr.start()
            i = keys.index(c)
            armonicos = [i, i + 2, i + 4]

    samples = np.zeros(CHUNK)
    for i in range(1):
        samples += oscFM(getNote(armonicos[i], escala), frame)
    stream.write(np.float32(adsr.get() * samples)) 
    frame += CHUNK
        
stream.stop()