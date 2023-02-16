'''En este ejercicio vamos a implementar un oscilador sinusoidal con una filosofía diferente, generando
la señal por bloques (chunks). Es decir, no generaremos la señal completa sino sucesivos fragmentos
de la misma de tamaño prefijado. El tamaño de los bloques vendrá determinado por una variable
global CHUNK (que podemos inicializar con 1024 por ejemplo).
Para ello implementaremos una clase Osc. El método constructor definirá un atributo con la frecuencia 
y otro método next devolverá el siguiente chunk (de tamaño CHUNK) con las siguientes
muestras de la señal. Concatenar varios chunks consecutivos y utilizar Matplotlib para verificar que
se obtiene la señal esperada.'''

#%% reproductor con Chunks

import numpy as np         # arrays    
import matplotlib.pyplot as plt

SRATE = 44100
CHUNK = 1024

class Osc:
    def __init__(self, frec):
        self.frec = frec
        self.phs = 0

    def next(self):
        s = np.arange(self.phs, self.phs + CHUNK)
        chunk = np.sin(2 * np.pi * self.frec * s / SRATE)
        self.phs = (self.phs + CHUNK) % SRATE
        return chunk

osc = Osc(440)
signal = np.concatenate([osc.next() for i in range(3)])
plt.plot(signal)
plt.show()

#%%