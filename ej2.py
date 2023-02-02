'''. Ahora vamos a generar una onda sinusoidal de 1 Hz y 1 segundo de duración, con la misma frecuencia
de muestreo, i.e., un ciclo de un segundo de esta forma:
Como antes, crearemos un array de NumPy para almacenar las muestras. Utilizaremos la función
np.sin para obtener esa señal teniendo en cuenta que el instante t = 1 seg. corresponde al argumento
2π para la función np.sin. Dibujar la señal con Matplotlib.
A continuación, modificaremos el programa para obtener una señal de 2 Hz y 1 segundo de duración
y luego para obtener una señal de 3 Hz y 2 segundos de duración. Dibujar los resultados.'''

#%% 1s a 1Hz
import numpy as np
import matplotlib.pyplot as plt

#Frecuencia de muestreo
SRATE = 44100
#Segundos de ruido
DURATION = 1
#Hercios
HZ = 1
#Volumen
VOL = 1

#Sample
s = np.arange(int(SRATE * DURATION), dtype=float)
#Seno
sin = VOL * np.sin(HZ * 2 * np.pi * s / SRATE)

plt.plot(sin)
#%% 1s a 2Hz
HZ = 2

s = np.arange(int(SRATE * DURATION), dtype=float)
sin = VOL * np.sin(HZ * 2 * np.pi * s / SRATE)

plt.plot(sin)
# %% 2s a 3Hz
DURATION = 2
HZ = 3

s = np.arange(int(SRATE * DURATION), dtype=float)
sin = VOL * np.sin(HZ * 2 * np.pi * s / SRATE)

plt.plot(sin)
# %%
