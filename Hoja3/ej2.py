'''Extender el sintetizador FM del ejercicio anterior para permitir otros tipos de onda: cuadrada,
diente de sierra, etc.'''

# sintesis fm con osciladores variables

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit
import os
from enum import Enum
from scipy import signal


SRATE = 44100       # sampling rate, Hz, must be integer
CHUNK = 1024

class Waveform(Enum):
    SINE = 1
    SQUARE = 2
    SAWTOOTH = 3

type = Waveform.SINE

# [(fc,vol),(fm1,beta1),(fm2,beta2),...]
def oscFM(frecs,frame):
    # sin(2πfc+βsin(2πfm))  
    chunk = np.arange(CHUNK)+frame
    samples = np.zeros(CHUNK)+frame
    # recorremos en orden inverso
    
    for i in range(len(frecs)-1,-1,-1):
        if(type == Waveform.SINE):
            samples = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/SRATE + samples)
        elif(type == Waveform.SQUARE):
            samples = frecs[i][1] * signal.square(2 * np.pi * frecs[i][0] * chunk / SRATE + samples)
        elif(type == Waveform.SAWTOOTH):
            samples = frecs[i][1] * signal.sawtooth(2 * np.pi * frecs[i][0] * chunk / SRATE + samples)
    return samples

    '''
    mod = frecs[i][1] * np.sin(2*np.pi*frecs[i][0]*chunk/RATE)
    res = np.sin(2*np.pi*fc*interval/RATE + mod)
    return (vol*res).astype(np.float32)
    '''

stream = sd.OutputStream(samplerate=SRATE,blocksize=CHUNK,channels=1)  
stream.start()

kb = kbhit.KBHit()
c = ' '
last = 0

fc, fm = 220, 220
frecs = [[fc,0.8],[fc+fm,0.5],[fc+2*fm,0.3],[fc+3*fm,0.2]]

frame = 0

while True:
    samples = oscFM(frecs,frame)   
    stream.write(np.float32(0.9*samples)) 

    frame += CHUNK

    if kb.kbhit():
        os.system("cls")
        c = kb.getch()
        
        if c =='z': break
        elif (c=='1'):
            frecs[last][0] -= 5
        elif (c=='2'):
            frecs[last][0] += 5
        elif (c=='3'):
            type = Waveform.SINE
        elif (c=='4'):
            type = Waveform.SQUARE
        elif (c=='5'):
            type = Waveform.SAWTOOTH
        elif (c>='a' and c<='x'):
            last = v = ord(c)-ord('a')
            if v<len(frecs): frecs[v][1] = max(0,frecs[v][1]-0.01)
        elif (c>='A' and c<='X'):
            last = v = ord(c)-ord('A')
            if v<len(frecs): frecs[v][1] = min(3,frecs[v][1]+0.01) 
        print("Use 1 and 2 to lower and rise last modulator's frecuency")
        print("3: sine")
        print("4: square")
        print("5: sawtooth")
        for i in range(len(frecs)): 
            print("["+str(chr(ord('A')+i))+"/"+str(chr(ord('a')+i))+"] ", " Frec " , frecs[i][0],"  beta: ",frecs[i][1])
        print("z quit")

stream.stop()
