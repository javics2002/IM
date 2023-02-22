'''Implementar una clase Python para hacer un sencillo efecto de Delay (línea de retardo). Este efecto
recibe una señal de entrada y devuelve la misma señal, pero retardada en el tiempo una cantidad
prefijada de tiempo. Tanto la entrada como la salida, serán chunks de audio e internamente deberá
gestionarse un bufier de datos.
Para probar el funcionamiento, reproducir simultáneamente 2 veces la nota de piano del ejercicio
anterior, una sin retardo y otra retardada una fracción de segundo (debe sonar un eco).'''

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHANNELS = 1
CHUNK = 2048
data, SRATE = sf.read('piano.wav',dtype="float32")

class Delay:
    def __init__(self, delay):
        self.sampleDelay = int(SRATE * delay)
        self.buffer = np.zeros(self.sampleDelay,dtype=np.float32)

    def delay(self, chunk):
        self.buffer = np.append(self.buffer, chunk, axis=0)
        delayedChunk = self.buffer[:CHUNK]
        self.buffer = self.buffer[CHUNK:]
        return delayedChunk

delay = Delay(.1)

# abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = CHANNELS)  # num de canales

# arrancamos stream
stream.start()


# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
# bloque = np.arange(CHUNK,dtype=data.dtype)
numBloque = 0
kb = kbhit.KBHit()
c= ' '

vol = 1.0
nSamples = CHUNK 
print('\n\nProcessing chunks: ',end='')

# termina con 'q' o cuando el último bloque ha quedado incompleto (menos de CHUNK samples)
while c!= 'q' and nSamples==CHUNK: 
    # numero de samples a procesar: CHUNK si quedan sufucientes y si no, los que queden
    nSamples = min(CHUNK,data.shape[0] + delay.sampleDelay * data.size - (numBloque+1)*CHUNK)

    # nuevo bloque
    bloque = data[numBloque*CHUNK : numBloque*CHUNK+nSamples ]
    bloque = bloque + delay.delay(bloque)
    bloque *= vol

    # lo pasamos al stream
    stream.write(bloque) # escribimos al stream

    # modificación de volumen 
    if kb.kbhit():
        c = kb.getch()
        if (c=='v'): vol= max(0,vol-0.05)
        elif (c=='V'): vol= min(1,vol+0.05)
        print("Vol: ",vol)

    numBloque += 1
    print('.',end='')


print('end')
stream.stop()
