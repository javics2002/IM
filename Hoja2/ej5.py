'''Utilizar la versión con callback del grabador de archivos .wav visto en clase 
para permitir grabar y reproducir audio simultáneamente. Se puede tomar un wav 
de entrada para la reproducción y a la vez grabar otro.'''

# basic/record0.py Grabacion de un archivo de audio 'q' para terminar
import numpy as np         # arrays    
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf     # para lectura/escritura de wavs
import kbhit               # para lectura de teclas no bloqueante

CHUNK = 1024
CHANNELS = 2
SRATE = 44100

# leemos wav en array numpy (data)
# por defecto lee float64, pero podemos hacer directamente la conversion a float32
data, SRATE = sf.read('music.wav')

# para arvhivos mono, devuelve un array de la forma data.shape = (n,)
# se necesita hacer explícito en número de canales, i.e., convertir a data.shape = (n,1) 
if (len(data.shape)==1): data = np.reshape(data,(data.shape[0],1))

# info del wav
print("SRATE: {}   Format: {}   Channels: {}    Len: {}".
  format(SRATE,data.dtype,len(data.shape), data.shape[0]))

# buffer para acumular grabación.
# contador de frames
current_frame = 0
# (0,1): con un canal (1), vacio (de tamaño 0)
buffer = np.empty((0, 1), dtype="float32")
def callback(indata, outdata, frames, time, status):
    global buffer
    buffer = np.append(buffer,indata)
    global current_frame       # para actualizarlo en cada callBack
    #if status: print(status)
    #print("Bloque: ",current_frame//CHUNK, outdata.shape, len(outdata))  # num bloque
    #print(data.shape)

    # vemos si podemos coger un CHUNK entero, si no lo que quede
    chunksize = min(len(data) - current_frame, frames)  
    
    # escribimos en outdata los samples correspondientes
    outdata[:chunksize] = data[current_frame:current_frame + chunksize]    
    # es una forma compacta y eficiente de hacer:
    # for i in range(chunksize): outdata[i] = data[current_frame+i]

    # NO funcionaría hacer outdata = data[current_frame:current_frame + chunksize]
    # porque asignaría (compartiría) referencias (objetos array de numpy)
    # outdata tiene que ser un nuevo array para enviar al stream y que no se reescriba
    
    if chunksize < frames: # ha terminado?
        outdata[chunksize:] = 0
        raise sd.CallbackStop()

    # actualizamos current_frame con los frames procesados    
    current_frame += chunksize



# stream de entrada con callBack
stream = sd.Stream(
    samplerate=SRATE, dtype="float32",
    channels=CHANNELS,
    blocksize=CHUNK, 
    callback=callback)


# arrancamos stream
stream.start()


print("* grabando")
print("* pulsa q para termninar")

# bucle para grabacion 
kb = kbhit.KBHit()
c = ' '
while c != 'q': 
    if kb.kbhit(): 
        c = kb.getch()
        print(c)


stream.stop() 
stream.close()
print("* grabacion terminada")

print('Quieres reproducir [S/n]? ',end='')
# bloqueamos ejecucion para recoger respuesta
while not kb.kbhit(): 
    True

# reproducción del buffer adquirido
c = kb.getch()
if c!='n':
    sd.play(buffer, SRATE)
    sd.wait()

# volcado a un archivo wav, utilizando la librería soundfile 
sf.write("rec.wav", buffer, SRATE)

stream.stop()

kb.set_normal_term()
