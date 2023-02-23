'''Implementar una función para remuestrear un audio dado con un frame rate a otro especificado,
sin alterar el pitch. Esta función servirá para cambiar la frecuencia de muestreo (sample rate).
Investigar formas de interpolación para hacerlo.'''

import numpy as np
import sounddevice as sd   # modulo de conexión con portAudio
import soundfile as sf
import kbhit 

# leemos wav en array numpy (data)
# por defecto lee en formato dtype="float64". No hay problema para reproducción simple (hace conversiones internas)
data, SRATE = sf.read('piano.wav',dtype="float32")

# info del wav
print("SRATE: {}   Format: {}   Channels: {}    Len: {}".
  format(SRATE,data.dtype,len(data.shape), data.shape[0]))

# def resample(data, targetRate):
#     nSamples = int(data.shape[0] * targetRate/SRATE)
#     resampledData = np.array(nSamples, dtype=data.dtype)
#     for i in range(0, nSamples):
#         sample = np.array()
#     return resampledData

from scipy.interpolate import interp1d

def resample_audio(audio, original_rate, target_rate):
    # calcular el tiempo correspondiente a cada muestra del audio original
    original_time = np.arange(0, len(audio)) / original_rate
    
    # calcular el tiempo correspondiente a cada muestra del audio remuestreado
    target_time = np.arange(0, len(audio)) / target_rate
    
    # crear una función spline que interpole los datos originales
    spline_func = interp1d(original_time, audio, kind='cubic')
    
    # evaluar la función spline en los tiempos correspondientes al audio remuestreado
    resampled_audio = spline_func(target_time)
    
    return resampled_audio

sd.play(data, SRATE)
sd.wait()

rate = SRATE / 2
sd.play(resample_audio(data, SRATE, rate), rate)
sd.wait()

rate = SRATE * 2
sd.play(resample_audio(data, SRATE, rate), rate)
sd.wait()