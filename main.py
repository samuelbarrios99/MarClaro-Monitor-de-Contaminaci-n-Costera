NUM_DIAS = 7
SIN_DATO = -1      # este valor indica "ese día no se midió"



# Clase Zona: una zona costera con sus mediciones por día
class Zona:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mediciones = []
        for i in range(NUM_DIAS):
            self.mediciones.append(SIN_DATO)

    def registrar(self, dia, valor):
        self.mediciones[dia] = valor

    def promedio(self):
        suma = 0
        cantidad = 0
        for valor in self.mediciones:
            if valor != SIN_DATO:
                suma = suma + valor
                cantidad = cantidad + 1
        if cantidad == 0:
            return SIN_DATO
        return suma / cantidad



# Clase Alerta: avisa que una zona superó el umbral un día

class Alerta:
    def __init__(self, nombre_zona, dia, valor, umbral):
        self.nombre_zona = nombre_zona
        self.dia = dia
        self.valor = valor
        self.umbral = umbral

    def mostrar(self):
        exceso = self.valor - self.umbral
        print("ALERTA:", self.nombre_zona, "- Día", self.dia + 1,
              "- Índice", self.valor, "(supera el umbral en " + str(exceso) + ")")



# Clase Monitor: administra las zonas, la matriz y los reportes

class Monitor:
    def __init__(self, umbral):
        self.umbral = umbral
        self.zonas = []      # lista de objetos Zona
        self.matriz = []     # matriz: cada fila es la lista de mediciones
                             # de una zona (es la misma lista de la Zona)

    def agregar_zona(self, nombre, valores):
        zona = Zona(nombre)
        for dia in range(len(valores)):
            zona.registrar(dia, valores[dia])
        self.zonas.append(zona)
        self.matriz.append(zona.mediciones)

    def registrar_medicion(self, indice_zona, dia, valor):
        self.zonas[indice_zona].registrar(dia, valor)

    def mostrar_matriz(self):
        print()
        print("Zona".ljust(20), end="")
        for dia in range(NUM_DIAS):
            print(("Día " + str(dia + 1)).rjust(8), end="")
        print()
        for i in range(len(self.matriz)):
            print(self.zonas[i].nombre.ljust(20), end="")
            for j in range(NUM_DIAS):
                if self.matriz[i][j] == SIN_DATO:
                    print("-".rjust(8), end="")
                else:
                    print(str(self.matriz[i][j]).rjust(8), end="")
            print()

    # Promedio por zona (se recorre cada fila) 
    def promedios_por_zona(self):
        promedios = []
        for i in range(len(self.matriz)):
            suma = 0
            cantidad = 0
            for j in range(NUM_DIAS):
                if self.matriz[i][j] != SIN_DATO:
                    suma = suma + self.matriz[i][j]
                    cantidad = cantidad + 1
            if cantidad == 0:
                promedios.append(SIN_DATO)
            else:
                promedios.append(suma / cantidad)
        return promedios

    #Promedio por día (se recorre cada columna)
    def promedios_por_dia(self):
        promedios = []
        for j in range(NUM_DIAS):
            suma = 0
            cantidad = 0
            for i in range(len(self.matriz)):
                if self.matriz[i][j] != SIN_DATO:
                    suma = suma + self.matriz[i][j]
                    cantidad = cantidad + 1
            if cantidad == 0:
                promedios.append(SIN_DATO)
            else:
                promedios.append(suma / cantidad)
        return promedios

    # Zona más contaminada (mayor promedio) 
    def zona_mas_contaminada(self):
        promedios = self.promedios_por_zona()
        posicion = 0
        for i in range(1, len(promedios)):
            if promedios[i] > promedios[posicion]:
                posicion = i
        return posicion

    # - Ranking: ordenamiento burbuja sobre una matriz de 2 columnas 
    def ranking(self):
        promedios = self.promedios_por_zona()
        tabla = []                       # cada fila: [nombre, promedio]
        for i in range(len(self.zonas)):
            tabla.append([self.zonas[i].nombre, promedios[i]])

        n = len(tabla)
        for i in range(n - 1):
            for j in range(n - 1 - i):
                if tabla[j][1] < tabla[j + 1][1]:
                    auxiliar = tabla[j]
                    tabla[j] = tabla[j + 1]
                    tabla[j + 1] = auxiliar
        return tabla

    #  Alertas: mediciones que superan el umbral 
    def generar_alertas(self):
        alertas = []
        for i in range(len(self.matriz)):
            for j in range(NUM_DIAS):
                valor = self.matriz[i][j]
                if valor != SIN_DATO and valor > self.umbral:
                    alertas.append(Alerta(self.zonas[i].nombre, j, valor, self.umbral))
        return alertas

    # Tendencia: compara el inicio con el final de la semana 
    def tendencia(self, indice_zona):
        fila = self.matriz[indice_zona]
        suma_inicio = 0
        cant_inicio = 0
        suma_final = 0
        cant_final = 0
        for j in range(3):                       # días 1, 2 y 3
            if fila[j] != SIN_DATO:
                suma_inicio = suma_inicio + fila[j]
                cant_inicio = cant_inicio + 1
        for j in range(NUM_DIAS - 3, NUM_DIAS):  # últimos 3 días
            if fila[j] != SIN_DATO:
                suma_final = suma_final + fila[j]
                cant_final = cant_final + 1

        if cant_inicio == 0 or cant_final == 0:
            return "datos insuficientes"
        cambio = suma_final / cant_final - suma_inicio / cant_inicio
        if cambio > 2:
            return "SUBE (+" + str(round(cambio, 1)) + ")"
        elif cambio < -2:
            return "BAJA (" + str(round(cambio, 1)) + ")"
        else:
            return "ESTABLE"


# Datos de ejemplo (valores ilustrativos, no son mediciones reales)

def cargar_datos_ejemplo(monitor):
    monitor.agregar_zona("Bocas de Ceniza",    [72, 76, 83, 79, 86, 91, 88])
    monitor.agregar_zona("Cienaga Mallorquin", [65, 68, 63, 74, 70, 77, 81])
    monitor.agregar_zona("Puerto Colombia",    [50, 55, 61, 58, 66, 63, 70])
    monitor.agregar_zona("Salgar",             [40, 44, 47, 43, 50, 48, 52])
    monitor.agregar_zona("Pradomar",           [35, 38, 36, 41, 39, 43, 40])
    monitor.agregar_zona("Puerto Velero",      [22, 25, 21, 24, 23, 26, 22])
    monitor.agregar_zona("Santa Veronica",     [18, 20, 19, 22, 21, 20, 19])


# Funciones para leer datos del usuario sin que el programa falle

def leer_entero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje)
        if texto.isdigit():
            numero = int(texto)
            if numero >= minimo and numero <= maximo:
                return numero
        print("Valor inválido. Escriba un número entre", minimo, "y", maximo)


def elegir_zona(monitor):
    print()
    for i in range(len(monitor.zonas)):
        print(str(i + 1) + ". " + monitor.zonas[i].nombre)
    return leer_entero("Elija la zona: ", 1, len(monitor.zonas)) - 1



# Programa principal con menú

def mostrar_menu():
    print()
    print("====== MONITOR DE CONTAMINACION COSTERA ======")
    print("======    Barranquilla - Atlantico     ======")
    print("1. Registrar medición")
    print("2. Ver matriz de mediciones")
    print("3. Promedio por zona")
    print("4. Zona más contaminada")
    print("5. Ranking de zonas")
    print("6. Alertas")
    print("7. Promedio por día")
    print("8. Tendencia por zona")
    print("9. Cambiar umbral de alerta")
    print("0. Salir")


def main():
    monitor = Monitor(60)
    cargar_datos_ejemplo(monitor)

    opcion = -1
    while opcion != 0:
        mostrar_menu()
        opcion = leer_entero("Opción: ", 0, 9)

        if opcion == 1:
            i = elegir_zona(monitor)
            dia = leer_entero("Día (1 a " + str(NUM_DIAS) + "): ", 1, NUM_DIAS) - 1
            valor = leer_entero("Índice de contaminación (0 a 100): ", 0, 100)
            monitor.registrar_medicion(i, dia, valor)
            print("Medición registrada.")
            if valor > monitor.umbral:
                print("¡Atención! Supera el umbral de", monitor.umbral)

        elif opcion == 2:
            monitor.mostrar_matriz()

        elif opcion == 3:
            promedios = monitor.promedios_por_zona()
            print()
            for i in range(len(monitor.zonas)):
                if promedios[i] == SIN_DATO:
                    print(monitor.zonas[i].nombre.ljust(20), "sin datos")
                else:
                    print(monitor.zonas[i].nombre.ljust(20), round(promedios[i], 1))

        elif opcion == 4:
            i = monitor.zona_mas_contaminada()
            promedio = monitor.zonas[i].promedio()
            print()
            print("Zona más crítica:", monitor.zonas[i].nombre,
                  "con promedio", round(promedio, 1))

        elif opcion == 5:
            tabla = monitor.ranking()
            print()
            print("Ranking (de más a menos contaminada):")
            for i in range(len(tabla)):
                print(str(i + 1) + ". " + tabla[i][0].ljust(20) + str(round(tabla[i][1], 1))) 

        elif opcion == 6:
            alertas = monitor.generar_alertas()
            print()
            print("Umbral actual:", monitor.umbral)
            if len(alertas) == 0:
                print("No hay alertas.")
            else:
                for alerta in alertas:
                    alerta.mostrar()
                print("Total de alertas:", len(alertas))

        elif opcion == 7:
            promedios = monitor.promedios_por_dia()
            print()
            for j in range(NUM_DIAS):
                if promedios[j] == SIN_DATO:
                    print("Día", j + 1, ": sin datos")
                else:
                    print("Día", j + 1, ":", round(promedios[j], 1))

        elif opcion == 8:
            print()
            for i in range(len(monitor.zonas)):
                print(monitor.zonas[i].nombre.ljust(20), monitor.tendencia(i))

        elif opcion == 9:
            monitor.umbral = leer_entero("Nuevo umbral (0 a 100): ", 0, 100)
            print("Umbral actualizado.")

    print("Fin del programa.")


main() 