'''En este ejercicio vamos a implementar un oscilador sinusoidal con una filosofía diferente, generando
la señal por bloques (chunks). Es decir, no generaremos la señal completa sino sucesivos fragmentos
de la misma de tamaño prefijado. El tamaño de los bloques vendrá determinado por una variable
global BUF_SIZE (que podemos inicializar con 1024 por ejemplo).
Para ello implementaremos una clase Osc. El método constructor definirá un atributo con la frecuencia y otro método next devolverá el siguiente chunk (de tamaño BUF_SIZE) con las siguientes
muestras de la señal. Concatenar varios chunks consecutivos y utilizar Matplotlib para verificar que
se obtiene la señal esperada.'''

#%% Fade in and fade out
import numpy as np
import matplotlib.pyplot as plt

#Frecuencia de muestreo
SRATE = 44100
#%%
#Devuelve una señal sinusoidal de frecuencia frec, duracion dur y volumen vol
def osc(frec, dur, vol = 1, phs = 0):
    s = np.arange(int(SRATE * dur))
    return vol * np.sin((frec * 2 * np.pi * s - phs) / SRATE)

#Decrece la intensidad desde el instante t hasta el final
def fadeOut(sample, t):
    return np.array([sample if i < t  else (sample * (sample.size - i)) / (sample.size - t) for i in sample])

#Crece la intensidad desde el inicio hasta el instante t
def fadeIn(sample, t):
    return np.array([sample if i > t  else (sample * i) / t for i in sample])

onda = osc(2, 1, 1)
plt.plot(fadeOut(onda, .2))
onda2 = osc(3, 1, 1, 10000)
plt.plot(fadeOut(onda, .8))


# %%
