''' Implementar un piano polifónico utilizando el modelo de síntesis de Karplus-Strong
visto en clase. Para ello puede implementarse este modelo de síntesis como una clase con un método
para iniciar nota, otro para obtener los sucesivos chunks de sonido, etc. Para conseguir la polifonía
se puede utilizar una lista de objetos de la citada clase. Cada uno de ellos proporciona chunks de
la nota correspondiente, que se mezclarán (suma de arrays) y se enviarán al stream de salida.'''

import numpy as np
import sounddevice as sd
import kbhit    

SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024

keys = "zsxdcvgbhnjmq2w3er5t6y7ui"
frecs = [220 * np.power(2, i/12) for i in range(len(keys))]

class KarplusStrong:
    def __init__(self, frec, dur):
        N = SRATE // int(frec) # la frecuencia determina el tamanio del buffer
        buf = np.random.rand(N) * 2 - 1 # buffer inicial: ruido
        self.nSamples = int(dur * SRATE)
        self.samples = np.empty(self.nSamples, dtype="float32") # salida
        # generamos los nSamples haciendo recorrido circular por el buffer
        for i in range(self.nSamples):
            self.samples[i] = buf[i % N] # recorrido de buffer circular
            buf[i % N] = 0.5 * (buf[i % N] + buf[(1 + i) % N]) # filtrado
        
        self.i = self.nSamples # marcador de posicion, al inicio con la nota "terminada"

    def getChunk(self):
        j = self.i + CHUNK

        if j > self.nSamples:
            return np.zeros(CHUNK) # Silencio si se ha acabado
        
        chunk = self.samples[self.i:j] #Proximos samples del bloque
        self.i = j

        return chunk
    
    def play(self): # comienza la nota
        self.i = 0

DUR = 1.3
wavetable = [KarplusStrong(frecs[i], DUR) for i in range(len(keys))] # Lista de notas de Karplus Strong

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

kb = kbhit.KBHit()
c=''
print("Teclado = zsxdcvgbhnjmq2w3er5t6y7ui      P = quit")
while c != 'p':
    if kb.kbhit():
        c = kb.getch()
        if keys.count(c):
            i = keys.index(c)
            wavetable[i].play()

    buf = np.zeros(CHUNK, dtype = np.float32)
    for i in range(len(keys)):
        buf += wavetable[i].getChunk()

    stream.write(buf) 
        
stream.stop()