'''Implementar una función vol(sample,vol) que multiplique una señal dada sample (array de NumPy)
por el volumen vol. Implementar otra función modulaVol(sample,frec) multiplique la señal por un
oscilador de frecuencia frec, que oscile en el intervalo [0,1]. ¾Qué ocurre si dejamos que oscile en el
intervalo [-1,1]? Dibujar los resultados.'''

#%% Cambia volumen
import numpy as np
import matplotlib.pyplot as plt

#Frecuencia de muestreo
SRATE = 44100

#Devuelve una señal sinusoidal de frecuencia frec, duracion dur y volumen vol
def osc(frec, dur, vol = 1, phs = 0):
    s = np.arange(int(SRATE * dur))
    return vol * np.sin((frec * 2 * np.pi * s - phs) / SRATE)

#Multiplica una señal sample por vol
def vol(sample, vol):
    return vol * sample;

onda = osc(1, 1, 1)
plt.plot(onda)
plt.plot(vol(onda, 0.3))

#%% Modula volumen [0, 1]
def modulaVol(sample, frec):
    s = osc(frec, sample.size / SRATE) / 2 + .5
    return sample * s

onda = osc(5, 1, 1)
auxonda = osc(1, 1, 1) / 2 + .5
plt.plot(onda)
plt.plot(auxonda)
plt.plot(modulaVol(onda, 1))

#%% Modula volumen [-1, 1]
def modulaVol(sample, frec):
    s = osc(frec, sample.size / SRATE)
    return sample * s

onda = osc(5, 1, 1)
auxonda = osc(1, 1, 1)
plt.plot(onda)
plt.plot(auxonda)
plt.plot(modulaVol(onda, 1))
# %%
