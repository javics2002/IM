'''Recordemos la partitura de la hoja anterior:
Happy Birthday
Joe Buchanan’s Scottish Tome - Page 551.3
G G A G c B G G A G d c G G g e c B A f f e c d c
Podemos hacer una representación de esta partitura mediante una lista (Python) de pares (nota,duración). Las notas se representan con las letras A B ...G; para subir una octava se utilizan las
minúsculas a b ...g2
. La duración se representa con un número que indica las unidades de tiempo
(la unidad que se puede fijar en el programa). De este modo, la partitura anterior quedaría:
[(G,0.5),(G,0.5),(A,1),(G,1),(c,1),(B,2),. . . ]
Recordemos la tabla de frecuencias (para una octava):
C D E F G a b c d . . . g
523,251 587,33 659,255 698,456 783,991 880 987,767 . . . . . .
Recordemos también que dada la frecuencia de una nota, la de la octava superior se obtiene duplicando dicha frecuencia. La de la octava inferior, dividiendo entre 2. Para reproducir la partitura
puede utilizarse el oscilador osc(nota,volumen,duración) visto en clase.
Puede extenderse la implementación para leer de archivo la partitura en notación ABC (Wikipedia,
entrada "Notación musical ABC").'''

import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs

SRATE = 44100

notes = "C.D.EF.G.a.bc.d.ef.g."
freqs = [523.251*(2**(i/12)) for i in range(24)]

hpday = [("G",0.5),("G",0.5),("a",1),
        ("G",1),("c",1),("b",2),
        ("G",0.5),("G",0.5),("a",1),("G",1),
        ("d",1),("c",2),
        ("G",0.5),("G",0.5),("g",1),("e",1),
        ("c",1),("b",1),("a",1),
        ("f",0.5),("f",0.5),("e",1),("c",1),
        ("d",1),("c",2)]

def getFreqDur(note):
    dur = note[1]
    i = notes.index(note[0])
    freq = freqs[i]
    return freq, dur

# returns a sinusoidal signal with frec, dur, vol
def osc(frec,dur,vol=1):
    # number of samples requiered according to SRATE
    nSamples = int(SRATE*dur)
    return vol * np.sin(2*np.pi*np.arange(nSamples)*frec/SRATE)

data = []
for i in range(len(hpday)):
    freq, dur = getFreqDur(hpday[i])
    data = np.append(data, osc(freq, dur))

# bajamos volumen
data = data * 0.5

# a reproducir!
sd.play(data, SRATE)

# bloqueamos la ejecución hasta que acabe
sd.wait()