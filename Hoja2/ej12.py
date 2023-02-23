'''Implementar un oscilador chirp(frecIni,frecFin,dur) que genere una señal sinusoidal de duración
dur, que comience con una frecuencia frecIni y la incremente gradualmente (de manera lineal) hasta
alcanzar frecFin. Este tipo de osciladores es conocido y utilizado en distintas aplicaciones (https:
//en.wikipedia.org/wiki/Chirp). Para implementarlo se puede partir del oscilador básico visto
en clase y modificarlo para variar el parámetro de frecuencia en el argumento de la función sin.
A continuación mejorar la funcionalidad para que, utilizando la misma muestra, pueda producir la
señal con la frecuencia requerida.'''

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

SRATE = 44100
CHUNK = 1024

def chirp(frecIni,frecFin,dur,vol=1.0):
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*np.linspace(frecIni,frecFin,nSamples)/SRATE)

    # abrimos stream de salida
stream = sd.OutputStream(
    samplerate = SRATE,            # frec muestreo 
    blocksize  = CHUNK,            # tamaño del bloque (muy recomendable unificarlo en todo el programa)
    channels   = 2)  # num de canales

# arrancamos stream
stream.start()

kb = kbhit.KBHit()
c = ' '

# En data tenemos el wav completo, ahora procesamos por bloques (chunks)
numBloque = 0 # contador de bloques/chunks

osc = chirp(440, 880, 2, .1)
sd.play(osc)
sd.wait()

stream.stop()
stream.close()
kb.set_normal_term()
