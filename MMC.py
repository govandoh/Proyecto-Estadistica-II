import os
import csv
from math import sqrt
import matplotlib.pyplot as plt

#Algoritmo que calcula la b, a, r y forma la ecuacion de la recta. Retorna el valor de la estimacion
def algoritmo_minimos_cuadrados(n, x, y, z):
    sumaX = 0
    sumaY = 0
    sumaXY = 0
    sumaX2 = 0
    sumaY2 = 0
    print("X \tY \t X*Y \t X^2 \t Y^2")
    for i in range(n):
        sumaX += x[i]  # Guarda la suma de x
        sumaY += y[i]  # Guarda la suma de y
        sumaXY += x[i] * y[i]  # Guarda la suma de la multiplicación de XY
        sumaX2 += x[i]**2  # Guarda la suma de la potencia cuadrada de x
        sumaY2 += y[i]**2 # Guarda la suma de la potencia cuadrada de y
        print(str(x[i]) + "\t" + str(y[i]) + "\t" + str(x[i]*y[i]) + "\t" + str(x[i]**2) + "\t" + str(y[i]**2)) # Muestra cada fila de x, y, x*y, x^2 en pantalla
    print("-"*100)
    print(str(sumaX) + "\t" + str(sumaY) + "\t" + str(sumaXY) + "\t" + str(sumaX2) + "\t" + str(sumaY2)) # Muestra la sumatoria de x, y, x*y, x^2 en pantalla
    b = ((n * sumaXY) - (sumaX * sumaY)) / ((n * sumaX2) - (sumaX**2))  # Calcula b usando las variables en donde se guardaron las sumatorias
    a = (sumaY / n) - b * (sumaX / n)  # Calcula a
    r = ((n * sumaXY) - (sumaX * sumaY)) / sqrt((n * sumaXY - (sumaX**2)) * ((n * sumaY2) - (sumaY**2))) # Calcula r
    print("\nLa ecuación de la recta es Y = {}x + {} \nCoeficiente de correlacion r = {}".format(b, a, r)) # Muestra la ecuacion
    valor_deflexion = b * z + a #Evalua x
    
    #Grafica los puntos y la linea ajustada
    plt.scatter(x, y, label="Datos") # Dibuja los puntos dispersos
    plt.plot(x, [b*i + a for i in x], color='red', label='Ajuste de minimos cuadrados') # Dibuja la linea ajustada usando la ecuacion previamente encontrada
    plt.title("Diagrama de dispersion")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.show()
    return valor_deflexion

# Funcion que permite cargar un archivo CSV 
def insertar_csv():
    # Mientras este en el ciclo While, el programa le pedira al usuario que cargue un archivo CSV.
    # Al final le preguntara si quiere cargar otro archivo CSV. Si en un caso el usuario responde diferente a 's' entonces se saldra del ciclo While
    while True:
        n = 0
        x = []
        y = []
        ruta = input("Copie y pegue la ruta de su archivo: ") # Guardamos la ruta del archivo en la variable 'ruta'
        
        with open(ruta,"r") as archivo: # Abre el archivo CSV que se guardo en la ruta
            lector = csv.reader(archivo) #Obtiene todas las filas del archivo
            next(lector) # Se salta la cabecera del archivo CSV
            for fila in lector: # Lee cada fila en el archivo
                x.append(float(fila[0])) # Por cada fila, agrega el valor de la primer columna al arreglo x
                y.append(float(fila[1])) # Por cada fila, agrega el valor de la segunda columna al arreglo y
            n = lector.line_num - 1 # Obtiene el numero de filas sin contar la cabecera
        archivo.close()
        # Mientras este en el ciclo While, el programa le pedira al usuario que ingrese un valor de x a estimar. 
        # Al final le preguntara si quiere estimar otro valor usando los mismos datos del archivo CSV. 
        #Si en un caso el usuario responde diferente a 's' entonces se saldra del ciclo While
        while True:
            z = float(input("Ingrese el valor de x a estimar: "))
            resultado = algoritmo_minimos_cuadrados(n, x, y, z) #Almacena el valor estimado en la variable resultado
            print("El valor de deflexión aproximado es: ", resultado)

            respuesta = input("Desea estimar un nuevo valor de x usando los mismo datos? (s/n): ")
            if respuesta.lower() != 's':
                break
            print()
        
        respuesta = input("Desea cargar un nuevo archivo? (s/n): ")
        if respuesta.lower() != 's':
            break
        print()
#Funcion que permite el ingreso de los datos de forma manual
def insertar_manual():
    #Mientras este en el ciclo While, el programa le pedira al usuario que ingrese los valores de x, y.
    #Al final le preguntara si quiere ingresar una nueva cantidad de datos. Si en un caso el usuario responde diferente a 's' entonces se saldra del ciclo While
    while True:
        n = int(input("Ingrese la cantidad n de elementos: "))
        x = [0] * n
        y = [0] * n

        for i in range(n):
            x[i] = float(input("Ingrese el valor de x[{}]: ".format(i)))
            y[i] = float(input("Ingrese el valor de y[{}]: ".format(i)))
            print()
        #Mientras este en el ciclo While, el programa le pedira al usuario que ingrese un valor de x a estimar. 
        #Al final le preguntara si quiere estimar otro valor usando los mismos datos. Si en un caso el usuario responde diferente a 's' entonces se saldra del ciclo While
        while True:
            z = float(input("Ingrese el valor de x a estimar: "))
            resultado = algoritmo_minimos_cuadrados(n, x, y, z) #Almacena el valor estimado en la variable resultado
            print("El valor de deflexión aproximado es: ", resultado)
            
            respuesta = input("Desea estimar un nuevo valor de x usando los mismo datos? (s/n): ")
            if respuesta.lower() != 's':
                break
            print()
        
        respuesta = input("Desea ingresar nuevos valores de X y Y? (s/n): ")
        if respuesta.lower() != 's':
            break
        limpiar_pantalla()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("\tMETODO DE MINIMOS CUADRADOS EN SERIES DE TIEMPO")
    #Mientras este en el ciclo While, el programa seguira ejecutandose a menos que el usuario ingrese 0 como opcion.
    while True:
        opcion = int(input("1) INGRESAR DATOS POR MEDIO DE UN ARCHIVO CSV \n2) INGRESAR DATOS DE FORMA MANUAL \n0) Salir del programa\nIngrese el numero de opcion: "))
        if opcion == 0:
            break
        if opcion == 1:
            insertar_csv()
            limpiar_pantalla()
        elif opcion == 2:
            insertar_manual()
            limpiar_pantalla()
        else:
            print("Opcion no valida. Ingrese el valor entero de 1, 2 o 0 si desea finalizar el programa")
    print("FIN")

if __name__=="__main__":
    main()