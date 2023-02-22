'''
Utilizar el filtro IIR visto en clase para implementar un filtro paso banda (BP)
con frecuencia de corte y ancho de banda configurables. Utilizar dos filtros LP y HP en secuencia,
calculando los valores de α según se ha explicado en clase
'''
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import sys
import kbhit
import numpy as np

CHUNK = 1024

if len(sys.argv) < 2:
    #print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    #sys.exit(-1)
    wav = 'tormenta.wav'
else:
    wav = sys.argv[1]

data, SRATE = sf.read(wav,dtype="float32")

stream = sd.OutputStream(samplerate = SRATE, blocksize = CHUNK, channels = len(data.shape))  
stream.start()

kb = kbhit.KBHit()
frame = 0
c= ' '   

print("[L] frecuencia de corte baja +100")
print("[l] frecuencia de corte baja -100")
print("[H] frecuencia de corte alta +100")
print("[h] frecuencia de corte alta -100")

lowFrec = 1000
highFrec = 3000
prev = 0
filter = "lp"

while c!= 'q': # and not(quit):
    bloque = data[frame*CHUNK : (frame+1)*CHUNK]
        
    lowAlpha = np.exp(-2*np.pi*lowFrec / SRATE)
    highAlpha = np.exp(-2*np.pi*highFrec / SRATE)
    
    # filtro paso bajo y alto
    bloque[0] = highAlpha * prev + (1-highAlpha) * bloque[0] - lowAlpha * prev + (1-lowAlpha) * bloque[0]
    for i in range(1,CHUNK):
        bloque[i] = highAlpha * bloque[i-1] + (1-highAlpha) * bloque[i] - (lowAlpha * bloque[i-1] + (1-lowAlpha) * bloque[i])

    prev = bloque[CHUNK-1]

    stream.write(bloque)    
    if kb.kbhit():
        c = kb.getch()
        print(c)
        if c =='q': break
        elif c=='L': lowFrec += 100
        elif c=='l': lowFrec -= 100
        elif c=='H': highFrec += 100
        elif c=='h': highFrec = max(highFrec - 100, lowFrec)
        lowFrec = min(highFrec, max(0, lowFrec))
        highFrec = min(SRATE/2, max(highFrec, lowFrec))
        print("Frecuencia de corte baja: ", lowFrec,"   Alta: ", highFrec)

    frame += 1

kb.set_normal_term()

        
stream.stop()
stream.close()
