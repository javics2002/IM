'''En este ejercicio vamos a implementar un idiotizador3. Para ello utilizaremos un
Stream de entrada/salida. Reenviaremos la señal de entrada a la salida, con un retardo (configurable)
de tiempo. Será útil la línea de retardo del ejercicio anterior'''
# basic/record0.py Grabacion de un archivo de audio 'q' para terminar
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHANNELS = 1
CHUNK = 2048
SRATE = 44100

class Delay:
    def __init__(self, delay):
        self.sampleDelay = int(SRATE * delay)
        self.buffer = np.zeros(self.sampleDelay,dtype=np.float32)

    def delay(self, chunk):
        self.buffer = np.append(self.buffer, chunk, axis=0)
        delayedChunk = self.buffer[:CHUNK]
        self.buffer = self.buffer[CHUNK:]
        return delayedChunk

# buffer para acumular grabación.
# (0,1): con un canal (1), vacio (de tamaño 0)
delay = Delay(.25)
buffer = np.empty((0, 1), dtype="float32")
def callbackInput(indata, outdata, frames, time, status):
    global buffer
    global delay
    global CHUNK
    buffer = np.append(buffer,indata)    # buffer[:] = indata
    delayedChunk = delay.delay(buffer)
    buffer = buffer[CHUNK:]
    outdata[:, 0] = delayedChunk

# stream de entrada con callBack
stream = sd.Stream(
    samplerate=SRATE, dtype="float32",
    channels=CHANNELS,
    blocksize=CHUNK,
    device=(3,5), #Cambiar para tu ordenador
    callback=callbackInput)
stream.start()

#Para ver los dispositivos conectados
#print(sd.query_devices())

kb = kbhit.KBHit()
while not kb.kbhit(): 
    True

kb.set_normal_term()