'''Implementar un piano simple utilizando el sample proporcionado piano.wav. Utilizaremos KBHit para 
mapear las teclas zxc. . . a una octava del piano y qwe. . . a la octava superior.
A partir de muestra de una nota, por ejemplo un C, el resto de notas pueden obtenerse variando la
velocidad de reproducción de esa muestra de acuerdo a estas proporciones:
Nota C D E F G A B c d . . . a
Frec. 1 9/8 5/4 4/3 3/2 5/3 15/8 2 . . .
Es decir, para obtener un D (re) podemos reproducir a 1.12 de velocidad. Esto altera el pitch de la
muestra en la proporción justa para tener el D. Una forma sencilla de alterar el pitch de la nota es
modificar la frecuencia de muestreo en el stream de salida, haciendo los cálculos pertinentes.
Para hacerlo de forma más sofisticada observemos que dado un array de NumPy, si generamos otro
que contenga solo los samples en posición par (de la mitad de tamaño), obtenemos un sonido una
octava por arriba. Y al contrario, si generamos un array del doble de tamaño añadiendo muestras
intermedias (como media de la anterior y la superior de una dada) obtenemos una octava menos.
Esta idea de interpolación puede generalizarse para obtener cualquier nota, utitilizando la tabla de
pitch dados.'''

import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf
import kbhit 

# leemos wav en array numpy (data)
# por defecto lee en formato dtype="float64". No hay problema para reproducción simple (hace conversiones internas)
data, SRATE = sf.read('piano.wav',dtype="float32")

keys = "zxcvbnmasdfghj"
rate = [1,9/8,5/4,4/3,3/2,5/3,15/8,2,18/8,10/4,8/3,6/2,10/3,30/8]

kb = kbhit.KBHit()
c=''
while c != 'q':
    if kb.kbhit():
        c = kb.getch()
        if(keys.count(c)):
            sd.play(data, SRATE * rate[keys.index(c)])
        
sd.wait()