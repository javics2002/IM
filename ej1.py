'''Comenzaremos generando un segundo de ruido a 44100 Hz de frecuencia de muestreo. Para ello
creamos un array de NumPy con 44100 componentes v = np.arange(44100) que almacenará la
señal. A continuación, generamos una muestra aleatoria para cada componente, que corresponde a
un instante temporal (a intervalos de 1/44100 segundos). Dibujar la señal con Matplotlib.
NumPy puede generar directamente un array de valores aleatorios. Buscar la función adecuada y
hacerlo de esta manera (mucho más eficiente).'''

#%% 0,1s de ruido
import numpy as np
import matplotlib.pyplot as plt

#Frecuencia de muestreo
SRATE = 44100
#Segundos de ruido
DURATION = .1

noise = np.random.random(int(SRATE * DURATION)) * 2 - 1

plt.plot(noise)

# %%
