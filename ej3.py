'''Ahora generalizaremos aun más el ejercicio anterior. Definir una variable global con la frecuencia
de muestreo del proyecto SRATE=44100. Implementar una función osc(f,d) que devuelva una señal
sinusoidal con frecuencia f y duración d segs. Por ejemplo, para f=1, d=1 debe devolver un array
NumPy de 44100 muestras con un ciclo de la función sin. Utilizar Matplotlib para dibujar la señal y
probar con distintas frecuencias y duraciones. Probar también con diferentes valores para SRATE.
Análogamente, implementar funciones saw, square, triangle que obtengan señales con las formas 
indicadas (véase https://en.wikipedia.org/wiki/Waveform) y utilizar Matplotlib para dibujarlas'''

#%% Distintas sinusoidales
import numpy as np
import matplotlib.pyplot as plt

#Frecuencia de muestreo
SRATE = 44100

#Devuelve una señal sinusoidal de frecuencia frec, duracion dur y volumen vol
def osc(frec, dur, vol, phs):
    s = np.arange(int(SRATE * dur))
    return vol * np.sin(frec * 2 * np.pi * s / SRATE)

plt.plot(osc(1, 1, 1))
plt.plot(osc(4, 1, .4))
plt.plot(osc(3, .5, .8))
#%% Saw
def saw(frec, dur, vol):
    s = np.arange(int(SRATE * dur))
    return 2 * vol / np.pi * np.arctan(np.tan(frec * np.pi * s / SRATE))

plt.plot(saw(1, 1, 1))
plt.plot(saw(4, 1, .4))
plt.plot(saw(3, .5, .8))
#%% Square
def sqr(frec, dur, vol):
    s = np.arange(int(SRATE * dur))
    return 2 * vol / np.pi * np.arctan(np.tan(frec * np.pi * s / SRATE))

plt.plot(sqr(1, 1, 1))
plt.plot(sqr(4, 1, .4))
plt.plot(sqr(3, .5, .8))
#%% Triangle
def tri(frec, dur, vol):
    s = np.arange(int(SRATE * dur))
    return 2 * vol / np.pi * np.arctan(np.tan(frec * np.pi * s / SRATE))

plt.plot(tri(1, 1, 1))
plt.plot(tri(4, 1, .4))
plt.plot(tri(3, .5, .8))
