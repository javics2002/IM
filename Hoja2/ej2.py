'''Implementar osciladores similares al anterior, pero de onda cuadrada, 
diente de sierra y triangular.
Estas formas pueden generarse de manera manual o utilizar predefinidas de SciPy'''

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import kbhit               # para lectura de teclas no bloqueante
from scipy import signal
from enum import Enum

SRATE = 44100
CHUNK = 1024

class Waveform(Enum):
    SINE = 1
    SQUARE = 2
    SAWTOOTH = 3

class Osc:
    def __init__(self, frec):
        self.frec = frec
        self.phs = 0
        self.type = Waveform.SINE

    def next(self):
        s = np.arange(CHUNK, dtype=np.float32)
        chunk = np.zeros(CHUNK)
        if(self.type == Waveform.SINE):
            chunk = np.sin(2 * np.pi * self.frec * (s + self.phs) / SRATE)
        elif(self.type == Waveform.SQUARE):
            chunk = signal.square(2 * np.pi * self.frec * (s + self.phs) / SRATE)
        elif(self.type == Waveform.SAWTOOTH):
            chunk = signal.sawtooth(2 * np.pi * self.frec * (s + self.phs) / SRATE)
        self.phs += CHUNK
        return chunk.astype(np.float32)

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 1)  # num de canales

# arrancamos stream
stream.start()

kb = kbhit.KBHit()
c = ' '

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
numBloque = 0 # contador de bloques/chunks

osc = Osc(440)
vol = 1.0

while c != 'q': 
    # nuevo bloque. Si tiene menos de CHUNK samples coge los que quedan
    bloque = osc.next()
    bloque *= vol
    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        # Hay pops flojos al cambiar el volumen
        if (c =='v'): vol = max(0,vol-0.05)
        elif (c =='V'): vol = min(1,vol+0.05)
        # Hay pops fuertes al cambiar la frecuencia
        elif (c =='f'): osc.frec -= 5 
        elif (c =='F'): osc.frec += 5
        elif (c == '1'): osc.type = Waveform.SINE
        elif (c == '2'): osc.type = Waveform.SQUARE
        elif (c == '3'): osc.type = Waveform.SAWTOOTH
        print("Vol: ",vol, " Frec: ", osc.frec)

    numBloque += 1

print('end')

stream.stop()
stream.close()
kb.set_normal_term()
