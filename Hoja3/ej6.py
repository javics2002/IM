'''Implementar un sampler que permita cargar muestras anotadas con intervalo de
sustain (muestra inicial y final) de modo que pueda alargar las notas el tiempo deseado haciendo
loop sobre dicho intervalo. Este sintetizador comenzará a reproducir una nota con un mensaje
noteon (con una frecuencia dada) y utilizará el sample para producir esa nota, que se mantiene en
el tiempo utilizando reproduciendo en loop la región sustain y termina (sale de dicha región) con
el mensaje noteoff. Para la entrega debe proporcionarse al menos una muestra anotada (wav), para
poder probar el funcionamiento.'''

import numpy as np
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf
import kbhit 

keys = "zsxdcvgbhnjmq2w3er5t6y7ui"

# leemos wav en array numpy (data)
# por defecto lee en formato dtype="float64". No hay problema para reproducción simple (hace conversiones internas)
koto, SRATE = sf.read('koto.wav',dtype="float32")
KOTO_ON = 19372
KOTO_OFF = 25333
CHUNK = 1024
CHANNELS = len(koto.shape)

# info del wav
print("SRATE: {}   Format: {}   Channels: {}    Len: {}".
  format(SRATE,koto.dtype,CHANNELS, koto.shape[0]))

from scipy.interpolate import interp1d

class Sampler:
    def __init__(self, data, noteOn, noteOff):
        self.data = data
        self.nSamples = len(data)
        self.on = noteOn
        self.off = noteOff
        self.loopLen = noteOff - noteOn
        self.i = len(data)
        self.loop = False
    
    def start(self):
        print("noteon")
        self.i = 0
        self.loop = True

    def end(self):
        print("noteoff")
        self.loop = False

    def getChunk(self):
        j = self.i + CHUNK

        if j > self.nSamples:
            return np.zeros((CHUNK, CHANNELS), dtype=np.float32) # Silencio si se ha acabado
        
        chunk = np.zeros((CHUNK, CHANNELS), dtype=np.float32)

        #Proximos samples del bloque
        if self.i < self.on:
            chunk = self.data[self.i:j]
            self.i = j
        elif self.loop:
            for k in range(CHUNK):
                chunk[k] = self.data[self.on + (self.i + k) % self.loopLen]
            self.i = (j - self.on) % self.loopLen + self.on 
        else:
            chunk = self.data[self.i:j]
            self.i = j
        
        return chunk

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=CHANNELS)  
stream.start()

kb = kbhit.KBHit()
sampler = Sampler(koto, KOTO_ON, KOTO_OFF)
c=''
notePlayed = False
print("Cualquier tecla = noteon/noteoff      Q = quit")
while c != 'q':
    if kb.kbhit():
        c = kb.getch()

        if notePlayed:
            sampler.end()
        else:
            sampler.start()
        notePlayed = not notePlayed

    stream.write(sampler.getChunk()) 
        
stream.stop()