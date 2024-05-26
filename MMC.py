import os
import csv
from math import sqrt
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats
import vista

#Algoritmo que calcula la b, a, r y forma la ecuacion de la recta. Retorna el valor de la estimacion
def algoritmo_minimos_cuadrados(n, x, y, z):
    sumaX = 0
    sumaY = 0
    sumaXY = 0
    sumaX2 = 0
    sumaY2 = 0
    valor_deflexion = 0.0

    fecha = datetime.datetime.now() # Obtiene la fecha actual
    formato_fecha = fecha.strftime("%d-%m-%Y %H-%M-%S") # Da formato a la fecha
    file = "Resultados"
    nombre_archivo = f"{file}/regresion_lineal_{formato_fecha}.txt" # Concatena el texto 'regresion lineal' con la fecha
    
    if not os.path.exists(file):
        os.makedirs(file) # Crea la carpeta 'Resultados' si no existe
    
    # Crea un archivo con el nombre de regresion_lineal_DD-MM-AAAA
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("Resultados de la Regresión Lineal Simple:\n\n")
        archivo.write("X \tY \t X*Y \t X^2 \t Y^2\n")
        for i in range(n):
            sumaX += x[i]  # Guarda la suma de x
            sumaY += y[i]  # Guarda la suma de y
            sumaXY += x[i] * y[i]  # Guarda la suma de la multiplicación de XY
            sumaX2 += x[i]**2  # Guarda la suma de la potencia cuadrada de x
            sumaY2 += y[i]**2 # Guarda la suma de la potencia cuadrada de y
            archivo.write(str(x[i]) + "\t" + str(y[i]) + "\t" + str(x[i]*y[i]) + "\t" + str(x[i]**2) + "\t" + str(y[i]**2) + "\n") # Guarda cada fila de x, y, x*y, x^2 en un archivo    
        
        archivo.write("-"*100)
        archivo.write("\n" + str(sumaX) + "\t" + str(sumaY) + "\t" + str(sumaXY) + "\t" + str(sumaX2) + "\t" + str(sumaY2)) # Guarda la sumatoria de x, y, x*y, x^2 en un archivo
        b = ((n * sumaXY) - (sumaX * sumaY)) / ((n * sumaX2) - (sumaX**2))  # Calcula b usando las variables en donde se guardaron las sumatorias
        a = (sumaY / n) - b * (sumaX / n)  # Calcula a
        r = ((n * sumaXY) - (sumaX * sumaY)) / sqrt((n * sumaX2 - (sumaX**2)) * ((n * sumaY2) - (sumaY**2))) # Calcula r
        valor_deflexion = b * z + a # Evalua x
        # Guarda la pendiente, interseccion, coeficiente de relacion y la ecuacion en un archivo
        archivo.write("\n\nPendiente (b): {}".format(b))
        archivo.write("\nIntersección (a): {}".format(a))
        archivo.write("\nCoeficiente de correlacion (R): {}".format(r))
        archivo.write("\nLa ecuación de la recta es Y = {}({}) + {} = {}".format(b, z, a, valor_deflexion)) 
    archivo.close() # Cierra el archivo
    
    
    #Grafica los puntos y la linea ajustada
    plt.scatter(x, y, label="Datos") # Dibuja los puntos dispersos
    plt.plot(x, [b*i + a for i in x], color='red', label='Ajuste de minimos cuadrados') # Dibuja la linea ajustada usando la ecuacion previamente encontrada
    plt.title("Diagrama de dispersion")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.text(3,2,"Y = {}(x) + {} \nr = {}".format(b, a, r)) # Muestra la ecuacion y coeficiente r en la grafica
    plt.legend()
    plt.show()
    print("Los resultados de la regresión lineal simple han sido guardados")

    return valor_deflexion, nombre_archivo

# Funcion que permite cargar un archivo CSV para una regresion lineal simple
def insertar_csv_lineal(ruta,z):
    #Lee el archivo CSV y asigna los valores de X y Y en dos variables. Obtiene el numero n de filas del archivo
    datos = pd.read_csv(ruta, header=0, usecols=['X', 'Y'])
    x = datos['X']
    y = datos['Y']
    n = len(datos)

    #z = float(input("Ingrese el valor de x a estimar: "))
    resultado, nombre_archivo = algoritmo_minimos_cuadrados(n, x, y, z) #Almacena el valor estimado en la variable resultado
    txt = f"El valor de deflexión aproximado es: {resultado}"
    vista.messagebox.showinfo("Resultados",txt)
    
    #verificar si las correlaciones son estadísticamente significativas
    alfa = 0.05

    for i, col in enumerate(datos.columns[0:]):
        res = scipy.stats.linregress(datos[col], datos["Y"])
        print(f"{col}: \t Rechazo hipótesis nula: {res.pvalue < alfa}")

    #las distribuciones bajo la hipótesis nula: linea azul
    #los límites dados por alfa: linea punteada negra (dos colas)
    #El valor del observado para cada una de las variables: linea roja
    fig, ax = plt.subplots(1, 1, figsize=(8, 2), tight_layout=True, sharey=True)
    ax.set_ylabel(datos.columns[1])

    N = datos.shape[0]
    t = np.linspace(-7, 7, num=1000)
    dist = scipy.stats.t(loc=0, scale=1, df=N-2) # dos grados de libertad
    
    res = scipy.stats.linregress(datos['X'], datos["Y"])
    t_data = res.rvalue*np.sqrt(N-2)/np.sqrt(1.-res.rvalue**2)
    ax.plot(t, dist.pdf(t))
    ax.plot([dist.ppf(alfa/2)]*2, [0, np.amax(dist.pdf(t))], 'k--')
    ax.plot([dist.ppf(1-alfa/2)]*2, [0, np.amax(dist.pdf(t))], 'k--')
    ax.plot([t_data]*2, [0, np.amax(dist.pdf(t))], 'r-')
    ax.set_xlabel(datos.columns[0])

    plt.show()
    return nombre_archivo
    
# Funcion que permite cargar un archivo CSV para una regresion lineal multiple
def insertar_csv_multiple(ruta, x1, x2):
    
    #ruta = input("Copie y pegue la ruta de su archivo: ") # Guardamos la ruta del archivo en la variable 'ruta'
    # Carga los datos desde el archivo CSV
    datos = pd.read_csv(ruta, header=0, usecols=['Y', 'X1', 'X2'])
    # Variables predictoras (x1 y x2) y variable de respuesta (y)
    x = datos[['X1', 'X2']]
    x = sm.add_constant(x)  # Añade columna de unos para el intercepto
    y = datos['Y']
    
    #x1 = float(input("Ingrese el valor de x1 a estimar: "))
    #x2 = float(input("Ingrese el valor de x2 a estimar: "))
   
    # Ajusta el modelo de regresión lineal múltiple
    modelo = sm.OLS(y, x).fit()
    resultado = modelo.params['const'] + modelo.params['X1'] * x1 + modelo.params['X2'] * x2
    
    # Resumen del modelo ajustado
    resumen = modelo.summary()

    fecha = datetime.datetime.now() # Obtiene la fecha actual
    formato_fecha = fecha.strftime("%d-%m-%Y %H-%M-%S") # Da formato a la fecha
    file = "Resultados"
    
    if not os.path.exists(file):
        os.makedirs(file) # Crea la carpeta 'Resultados' si no existe

    nombre_archivo = f"{file}/regresion_multiple_{formato_fecha}.txt" # Concatena el texto 'regresion multiple' con la fecha
    # Crea un archivo con el nombre de regresion_multiple_DD-MM-AAAA
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("Resultados de la Regresión Lineal Multiple:\n\n")
        archivo.write(resumen.as_text()) # Convierte en texto el resumen del modelo ajustado y lo guarda en un archivo de texto
        archivo.write("\n\nLa ecuacion es: Y = {} + {} * {} + {} * {} = {}".format(modelo.params['const'], modelo.params['X1'], x1, modelo.params['X2'], x2, resultado)) # Guarda la ecuacion en el archivo

    archivo.close() # Cierra el archivo
    # Grafica los datos y la línea de regresión
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d') # Agrega ejes a la figura
    ax.scatter(datos['X1'], datos['X2'], datos['Y'], c='blue', marker='o', alpha=0.5) # Diagrama de dispersion de y frente a x
    #Etiquetas para los ejes x, y, z
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel('y')

    # Superponer la línea de regresión
    x1_surf, x2_surf = np.meshgrid(np.linspace(datos['X1'].min(), datos['X1'].max(), 100),
                                np.linspace(datos['X2'].min(), datos['X2'].max(), 100)) # Devuelve una lista de matrices de coordenadas a partir de vectores de coordenadas.
    X_surf = pd.core.frame.DataFrame({'const': np.ones(10000), 'X1': x1_surf.ravel(), 'X2': x2_surf.ravel()}) # Crea un DataFrame de pandas con tres columnas: una columna llamada 'const' llena de unos, y dos columnas ('X1' y 'X2')
    ax.plot_surface(x1_surf, x2_surf, modelo.predict(X_surf).values.reshape(100, 100), color='None', alpha=0.5) # Traza una superficie tridimensional en un gráfico
    plt.show()

    #verificar si las correlaciones son estadísticamente significativas
    alfa = 0.05

    for i, col in enumerate(datos.columns[1:]):
        res = scipy.stats.linregress(datos[col], datos["Y"])
        print(f"{col}: \t Rechazo hipótesis nula: {res.pvalue < alfa}")

    #las distribuciones bajo la hipótesis nula: linea azul
    #los límites dados por alfa: linea punteada negra (dos colas)
    #El valor del observado para cada una de las variables: linea roja
    fig, ax = plt.subplots(1, 2, figsize=(8, 2), tight_layout=True, sharey=True)
    ax[0].set_ylabel(datos.columns[0])

    N = datos.shape[0]
    t = np.linspace(-7, 7, num=1000)
    dist = scipy.stats.t(loc=0, scale=1, df=N-2) # dos grados de libertad


    for i, col in enumerate(datos.columns[1:]):
        res = scipy.stats.linregress(datos[col], datos["Y"])
        t_data = res.rvalue*np.sqrt(N-2)/np.sqrt(1.-res.rvalue**2)
        ax[i].plot(t, dist.pdf(t))
        ax[i].plot([dist.ppf(alfa/2)]*2, [0, np.amax(dist.pdf(t))], 'k--')
        ax[i].plot([dist.ppf(1-alfa/2)]*2, [0, np.amax(dist.pdf(t))], 'k--')
        ax[i].plot([t_data]*2, [0, np.amax(dist.pdf(t))], 'r-')
        ax[i].set_xlabel(col)

    plt.show()
    return nombre_archivo

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# def main():
#     print("\tMETODO DE MINIMOS CUADRADOS EN SERIES DE TIEMPO")
#     #Mientras este en el ciclo While, el programa seguira ejecutandose a menos que el usuario ingrese 0 como opcion.
#     while True:
#         opcion = int(input("1) REGRESION LINEAL SIMPLE \n2) REGRESION LINEAL MULTIPLE \n0) Salir del programa\nIngrese el numero de opcion: "))
#         if opcion == 0:
#             break
#         if opcion == 1:
#             insertar_csv_lineal()
#             limpiar_pantalla()
#         elif opcion == 2:
#             insertar_csv_multiple()
#             limpiar_pantalla()
#         else:
#             print("Opcion no valida. Debe ingresar el valor entero de 1, 2 o 0 si desea finalizar el programa")
#             limpiar_pantalla()
#     print("FIN")

# if __name__=="__main__":
#     #main()
