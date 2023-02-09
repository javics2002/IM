'''Implementar una función fadeOut(sample,t) que haga un efecto fadeOut con la señal sample desde
el instante t hasta el final (caída lineal de volumen). Análogo con fadeIn(sample,t) haciendo fadeIn
desde el inicio hasta el instante t.'''

#%% Fade in and fade out
import numpy as np
import matplotlib.pyplot as plt

#Frecuencia de muestreo
SRATE = 44100

#Devuelve una señal sinusoidal de frecuencia frec, duracion dur y volumen vol
def osc(frec, dur, vol = 1, phs = 0):
    s = np.arange(int(SRATE * dur))
    return vol * np.sin((frec * 2 * np.pi * s - phs) / SRATE)

#Decrece la intensidad desde el instante t hasta el final
def fadeOut(sample, t):
    return np.array([sample if i < t  else (sample * (sample.size - i)) / (sample.size - t) for i in sample])

onda = osc(1, 1, 1)
plt.plot(fadeOut(onda, .2))
# %%
