import sys
from pathlib import Path

import self as self
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton, QFileDialog,QPlainTextEdit

from Interfaz_CH_MAQUINA import *

class ChMaquina(QMainWindow):
#Creación del objeto que carga la interface
    def __init__(self):
        super(ChMaquina, self).__init__()
        self.initUI()
# Inicialización de la interface
    def initUI(self):
        #Variable global para asignar posiciones en memoria
        global contMemoria
        self.ui = Ui_CH_MAQUINA()
        self.ui.setupUi(self)
        # Botón y método de encendido
        self.ui.encender.clicked.connect(self.encender)
        # Botón apagar deshabilitado
        self.ui.apagar.setEnabled(False)
        # Botón imprimir deshabilitado
        self.ui.imprimir.setEnabled(False)
        # Botón abrir deshabilitado
        self.ui.abrir.setEnabled(False)
        #Botón ejecutar deshabilitado
        self.ui.ejecutar.setEnabled(False)
	#Spinner de memoria total asignada
        self.ui.spinMemoria.setValue(1000)
	#Spinner de kernel asignado
        self.ui.spinKernel.setValue(24)
	#Spinner memoria el cual ejecuta el método que calcula la memoria total
        self.ui.spinMemoria.valueChanged.connect(self.memoriaTotal)
	#Spinner memoria el cual ejecuta el método que calcula la memoria total
        self.ui.spinKernel.valueChanged.connect(self.memoriaTotal)
	#Botón apagar el cual ejecuta el método apagar	
        self.ui.apagar.clicked.connect(self.apagar)
	#Botón abrir el cual ejecuta el método cargar archivo
        self.ui.abrir.clicked.connect(self.cargarArchivo)
	#Botón actualizar archivo deshabilitado
        self.ui.analizarSinta.setEnabled(False)
	#Botón actualizar archivo el cual ejecuta el método sobreEscribir
        self.ui.analizarSinta.clicked.connect(self.sobreEscribir)
	#Se asigna el valor del Kernel al contador
        cont = self.ui.spinKernel.value()
        #Corre la interface
        self.show()


	# Método para encender el Sistema Operativo.
    def encender(self):
        global cont
        global nroPrograma
        global fila
        global nroVaria
        global nroEti
        global tipoVari
        global filaEti

	#Se desactiva el spinner del kernel
        self.ui.spinKernel.setEnabled(False)
	#Se desactiva el spinner de la memoria asignada
        self.ui.spinMemoria.setEnabled(False)
	#Se desactiva el botón de encendido
        self.ui.encender.setEnabled(False)
	#Se activa el botón de abrir
        self.ui.abrir.setEnabled(True)
	#Se activa el botón de apagar
        self.ui.apagar.setEnabled(True)
	# Se agrega el total de filas a la tabla
        self.ui.memoria.setRowCount(int(self.ui.spinMemoria.value()))  

#Se agrega la variable acumulador en la primera posición del sistema
        self.ui.memoria.setItem(0, 0, QTableWidgetItem('0'))
        self.ui.memoria.setItem(0, 1, QTableWidgetItem('0000'))
        self.ui.memoria.setItem(0, 2, QTableWidgetItem('-----'))
        self.ui.memoria.setItem(0, 3, QTableWidgetItem('Acumulador'))
        self.ui.memoria.setItem(0, 4, QTableWidgetItem('0'))

#Se agrega el kernel a la tabla de memoria
        for i in range(1, (self.ui.spinKernel.value() + 1)):
	    # Se llena la tabla con los datos del S.O.
            self.ui.memoria.setItem(i, 0,QTableWidgetItem(str(i)))
            self.ui.memoria.setItem(i, 1, QTableWidgetItem('0000'))
            self.ui.memoria.setItem(i, 2, QTableWidgetItem('-----'))
            self.ui.memoria.setItem(i, 3, QTableWidgetItem('Sistema Operativo'))
            self.ui.memoria.setItem(i, 4, QTableWidgetItem('0'))

#Se agrega el S.O. a la tabla de procesos
        self.ui.procesos.setRowCount(1)
	#Se agrega el proceso actual a la tabla de procesos
        self.ui.procesos.setItem(0, 0, QTableWidgetItem('0000'))
        self.ui.procesos.setItem(0, 1, QTableWidgetItem('Sistema Operativo'))
        self.ui.procesos.setItem(0, 2, QTableWidgetItem(str(self.ui.spinKernel.value())))
        self.ui.procesos.setItem(0, 3, QTableWidgetItem('0000'))
        self.ui.procesos.setItem(0, 4, QTableWidgetItem('0000'))
        self.ui.procesos.setItem(0, 5, QTableWidgetItem('0000'))
        cont = self.ui.spinKernel.value() + 1
        nroPrograma = 1
        fila = 0
        nroVaria = 1
        nroEti = 1
        tipoVari = ''
        filaEti = 0

# Método para apagar el S.O. 
    def apagar(self):
        buttonReply = QMessageBox()#Alerta de apagado
	#Alerta de apagado
        buttonReply.setWindowTitle('Mensaje de alerta')
	#Alerta de apagado
        buttonReply.setText("Quieres apagar la máquina?")
	#Alerta de apagado
        btnQs = QPushButton('Si')
	#Alerta de apagado
        buttonReply.addButton(btnQs, QMessageBox.YesRole)
	#Alerta de apagado
        btnNo = QPushButton('No')
	#Alerta de apagado
        buttonReply.addButton(btnNo, QMessageBox.NoRole)
	#Alerta de apagado
        ret = buttonReply.exec_()
	#Alerta de apagado
        if buttonReply.clickedButton() == btnQs:
            self.initUI()
        else:
	#Alerta de apagado
            buttonRepl = QMessageBox()
	#Alerta de apagado
            buttonRepl.setWindowTitle('Mensaje de alerta')
	#Alerta de apagado
            buttonRepl.setText("Quieres apagar la máquina?")

# Método para la carga del programa CH 

    def nroProgamasCargados(self, nro):
        if (nro < 10):
            return ('0000'+str(nro))
        elif (nro > 9 and nro < 100):
            return ('000' + str(nro))
        elif (nro > 99 and nro < 100):
            return ('00' + str(nro))
    def contarLineas(self, URL):
        return sum(1 for line in open(URL))

    def cargarArchivo(self):
        try:
            
            global nroPrograma
            global nombreArchivo
            global URL
            nroPrograma   = 0
            options = QFileDialog.Options()#Ventana para abrir el programa CH
            options |= QFileDialog.DontUseNativeDialog#Ventana para abrir el programa CH

            #Ventana para abrir el programa CH
            fileName, _ = QFileDialog.getOpenFileName(self, "Abrir Programa CH", "C:/Users/dacua/OneDrive/Documentos/PHYTON/CHM",
                                                       "All Files (*);;txt Files (*.ch)", options=options)
	#Variable con el nombre del archivo
            nombreArchivo = Path(fileName).stem 
	#Variable con la dir del archivo
            URL = fileName.replace('/','\\')
	#Llamado del método que chequea la sintaxis del CH
            self.sintaxis(nombreArchivo, fileName.replace('/','\\'))
	#Activa botón ejecutar
            self.ui.ejecutar.setEnabled(True)
	#Activa botón abrir
            self.ui.abrir.setEnabled(True)
	#Activa el botón para actualizar el archivo
            self.ui.analizarSinta.setEnabled(True)
            self.agregarTablaProcesos(nombreArchivo, URL)
            nroPrograma += 1
        except:
	#Mensaje de error al no cargar el archivo

            QMessageBox.information(self, "Mensaje de alerta", "Debe seleccionar un archivo")
            self.ui.abrir.setEnabled(True)                                                   
        f = open(URL, 'r')              #Método para actualizar el total de la memoria
        nume = 0                        #Método para actualizar el total de la memoria
        for i in f.readlines():         #Método para actualizar el total de la memoria
            nume += 1                   #Método para actualizar el total de la memoria
        f.close()                       #Método para actualizar el total de la memoria
        self.memoriaTotal(nume)         #Método para actualizar el total de la memoria

    def agregarTablaProcesos(self, nombreArchivo, URL):
        global nroPrograma
        nroPrograma += 1
        rowPosition = self.ui.procesos.rowCount()
        self.ui.procesos.setRowCount(rowPosition + 1)
	 # Agrega el nombre del programa a la tabla procesos
        self.ui.procesos.setItem(rowPosition, 0, QTableWidgetItem(self.nroProgamasCargados(nroPrograma))) 
        self.ui.procesos.setItem(rowPosition, 1, QTableWidgetItem(nombreArchivo))
        self.ui.procesos.setItem(rowPosition, 2, QTableWidgetItem(str(self.contarLineas(URL))))
        self.ui.procesos.setItem(rowPosition, 3, QTableWidgetItem('0000'))
        self.ui.procesos.setItem(rowPosition, 4, QTableWidgetItem('0000'))
        self.ui.procesos.setItem(rowPosition, 5, QTableWidgetItem('0000'))

# Método que chequea el número de instrucciones el programa CH 
    def errorIns(self, numero, linea):
	#Si la línea de instrucciones tiene menos de dos parámetros	
        if (numero < 2):
            self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
            self.ui.errores.append('La línea ' + '"' + ' '.join(str(e) for e in linea) + '"' + ' carece del número de '
                                                                                'instrucciones necesarias')
	#Si la línea de instrucciones tiene más de cuatro parámetros
        elif (numero > 4):
            self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
            self.ui.errores.append('La línea ' + '"' + ' '.join(str(e) for e in linea) + '"' + ' presenta más '
                                                                'instrucciones de las necesarias')
# Método que chequea el total de programas cargados en el S.O. CH 
    def instrucciones(self, nroPrograma, linea):
        global cont
        self.ui.memoria.setItem(cont, 0, QTableWidgetItem(str(cont)))
        if (nroPrograma <= 9):
            self.ui.memoria.setItem(cont, 1, QTableWidgetItem('000' + str(nroPrograma)))
        elif (nroPrograma > 9 and nroPrograma <= 99):
            self.ui.memoria.setItem(cont, 1, QTableWidgetItem('00' + str(nroPrograma)))
        elif (nroPrograma > 99 and nroPrograma <= 999):
            self.ui.memoria.setItem(cont, 1, QTableWidgetItem('0' + str(nroPrograma)))
        elif (nroPrograma > 999 and nroPrograma <= 9999):
            self.ui.memoria.setItem(cont, 1, QTableWidgetItem(str(nroPrograma)))
        else:
            QMessageBox.information(self, "Mensaje de alerta", "El número de programas sobrepasa la memoria")
        self.ui.memoria.setItem(cont, 2, QTableWidgetItem(linea[0]))
        self.ui.memoria.setItem(cont, 3, QTableWidgetItem(' '.join(str(e) for e in linea)))
        self.errorIns(len(linea), linea)

# Método para la corrección del programa CH 
    def sobreEscribir(self):
        global URL#Variable Global
        global nombreArchivo#Variable Global
        try:
            with open(URL, "w") as programa:#Abre el archivo en modo de escritura para poderlo editar
                editor = self.ui.editProgr.toPlainText()#Carga el contenido de textEdit en la variable
                self.ui.editProgr.setUndoRedoEnabled(True)#Activa hacer y deshacer
                self.ui.editProgr.setPlainText(editor)#Muestra el contenido del archivo en ventana
                programa.seek(0)#Lleva el cursor a la posición 0 del archivo
                programa.write(editor)#Sobre escribe el contenido del archivo con lo que se encuentra en el textEdit
            self.sintaxis(nombreArchivo, URL)#Realiza un nuevo chequeo de sintaxis y completa la tabla
            QMessageBox.information(self, "Mensaje de alerta", "Archivo actualizado")#Mensaje de confirmación
        except:
            QMessageBox.information(self, "Mensaje de alerta", "Archivo actualizado")#Mensaje de confirmación
# Método para el chequeo del programa CH 
    def sintaxis(self, nombrePrograma, URL):
    	global datos
    	global cont
    	global nroPrograma
    	global fila
    	global nroVaria
    	global nroEti
    	global tipoVari
    	global filaEti
    	with open(URL, "r") as programa:#Abre el archivo que contiene el programa CH
            editor = programa.read()#Muestra el contenido del archivo en pantalla
            self.ui.editProgr.setPlainText(editor)#Se muestra el contenido en el editor
            self.ui.variables.setRowCount(1)#Se agrega una fila a la tabla de variables
            programa.seek(0)#lleva el cursor a la posición 0 del archivo
            lineas = programa.readlines()  #Arreglo con todas las líneas del texto
            for i in lineas: #Recorre el arreglo y chequea cada una de las palabras contenidas en la línea
                linea = i.split()
                if (linea[0].upper() == 'CARGUE'):#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
                elif(linea[0].upper() == 'ALMACENE'):#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
                elif (linea[0].upper() == 'VAYA'):#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
                elif (linea[0].upper() == 'VAYASI'):#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
                elif (linea[0].upper() == 'NUEVA'):#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                    self.instrucciones(nroPrograma, linea)
	#Chequea si el nombre de la variable comienza con letra y es menor a 255 caracteres
                    if ((linea[1].split())[0].isalpha() and len(linea[1].split()) < 255):#

#Dentro del bloque se revisa que la letra corresponda al tipo de dato
                        if (linea[2] == 'C' and len(linea) > 3):
                            if (linea[3].isalpha()):
                                self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(linea[4])))
                                tipoVari = 'Cadena'
                            else:
                                self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                                self.ui.errores.append('La variable '+ '"'+linea[3]+ '"' + " no es una cadena")
                        if (linea[2] == 'I' and len(linea) > 3):
                            if (linea[3].isdigit()):
                                self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(linea[3])))
                                tipoVari = 'Entero'
                            else:
                                self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                                self.ui.errores.append('La variable '+ '"'+linea[3]+ '"' + " no es un entero")
                        elif (linea[2] == 'R' and len(linea) > 3):
                            if (linea[3].isdecimal()):
                                self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(linea[3])))
                                tipoVari = 'Real'
                            else:
                                self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                                self.ui.errores.append('La variable '+ '"'+linea[3]+ '"' + " no es "
                                    "un número real o decimal")
                        elif (linea[2] == 'L'  and len(linea) > 3):
                            if (linea[3].isdigit() and (linea[3] == '1' or linea[3] == '0')):
                                self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(linea[3])))
                                tipoVari = 'Lógico'
                            else:
                                self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                                self.ui.errores.append('La variable '+ '"'+linea[3]+ '"' + " no es "
                                    "un valor Booleano")
                        elif (linea[2] == 'C' and len(linea) == 3):
                            self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(" ")))
                        elif (linea[2] == 'I' and len(linea) == 3):
                            self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(0)))
                        elif (linea[2] == 'R' and len(linea) == 3):
                            self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(0.0)))
                        elif (linea[2] == 'L' and len(linea) == 3):
                            self.ui.memoria.setItem(cont, 4, QTableWidgetItem(str(0)))
                        else:
                            self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                            self.ui.errores.append('No existen tipo de datos ' + '"' + linea[2] + '"')
                    else:
                        self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                        self.ui.errores.append('Error en la variable ' + '"' + linea[1] + '"' + ' Los nombres '
                                'de las variables deben comenzar por letras y tener menos de 255 carácteres')
                    self.ui.variables.setRowCount(nroVaria)
                    self.ui.variables.setItem(fila, 0, QTableWidgetItem(str(cont)))
                    self.ui.variables.setItem(fila, 1, QTableWidgetItem(self.ui.memoria.item(cont, 1)))
                    self.ui.variables.setItem(fila, 2, QTableWidgetItem(tipoVari))
                    self.ui.variables.setItem(fila, 3, QTableWidgetItem(linea[1]))
                    self.ui.variables.setItem(fila, 4, QTableWidgetItem(str(linea[3])))
                    # VOY ACÁ
                    fila += 1
                    nroVaria += 1
                    cont += 1
		#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'ETIQUETA'):
                    self.instrucciones(nroPrograma, linea)
                    self.ui.etiquetas.setRowCount(nroEti)
                    self.ui.etiquetas.setItem(filaEti, 0, QTableWidgetItem(str(cont)))
                    self.ui.etiquetas.setItem(filaEti, 1, QTableWidgetItem(self.ui.memoria.item(cont, 1)))
                    self.ui.etiquetas.setItem(filaEti, 2, QTableWidgetItem(linea[1]))
                    self.ui.etiquetas.setItem(filaEti, 3, QTableWidgetItem(' '.join(str(e) for e in linea)))
                    filaEti += 1
                    nroEti += 1
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'LEA'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'SUME'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'RESTE'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'MULTIPLIQUE'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones	
                elif (linea[0].upper() == 'DIVIDA'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'POTENCIA'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'MODULO'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'CONCATENE'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'ELIMINE'):
                    self.instrucciones(cont, nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'EXTRAIGA'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'Y'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'O'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'NO'):
                    self.instrucciones(cont, nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'MUESTRE'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'IMPRIMA'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].upper() == 'RETORNE'):
                    self.instrucciones(nroPrograma, linea)
                    cont += 1
	#Si la palabra corresponde a esta opción ejecuta el método instrucciones
                elif (linea[0].startswith('//',0)):
                    self.ui.memoria.setItem(cont, 0, QTableWidgetItem(str(cont)))
                    if (nroPrograma <= 9):
                        self.ui.memoria.setItem(cont, 1, QTableWidgetItem('000' + str(nroPrograma)))
                    elif (nroPrograma > 9 and nroPrograma <= 99):
                        self.ui.memoria.setItem(cont, 1, QTableWidgetItem('00' + str(nroPrograma)))
                    elif (nroPrograma > 99 and nroPrograma <= 999):
                        self.ui.memoria.setItem(cont, 1, QTableWidgetItem('0' + str(nroPrograma)))
                    else:
                        QMessageBox.information(self, "Mensaje de alerta",
                                                "El número de programas sobrepasa la memoria")
                    self.ui.memoria.setItem(cont, 2, QTableWidgetItem('Comentario'))
                    self.ui.memoria.setItem(cont, 3, QTableWidgetItem(' '.join(str(e) for e in linea)))
                    cont += 1
                else:
                    self.ui.errores.append('\n' + '---Error encontrado---' + '\n')
                    self.ui.errores.append('CÓDIGO DE OPERACIÓN NO RECONOCIDO EN LA LÍNEA ' + '"' +
                                                      ' '.join(str(e) for e in linea))

# Método para calcular la memoria total
	# Este método hace el cálculo del total de memoria una vez se inicializa el S.O. y lo muestra en pantalla
    def memoriaTotal(self, cont):
        memGlobal = 9999
	#Variable de memoria total asignada
        mem = int(self.ui.spinMemoria.value())
	#Variable correspondiente al kernel
        kern = int(self.ui.spinKernel.value())
	#Variable para la barra de progreso del kernel
        pbKernel = ((kern * 100)/mem)
	#Barra de progreso del kernel
        self.ui.pbKernel.setValue(int(pbKernel))
	#Variable para el total de la memoria
        total_memo = (mem - (kern + cont))
	#Label total de memoria
        self.ui.totalMemoria.setText(str(int(self.ui.spinMemoria.value()) - total_memo))
	#Barra de progreso total de memoria
        self.ui.pbMemoria.setValue((total_memo * 100) / int(self.ui.spinMemoria.value()))
	#Barra de progreso total de memoria Global
        self.ui.pbTotalMen.setValue((int(self.ui.spinMemoria.value()) * 100) / 1000)


# INICIO DEL Sistema Operativo ChMáquina.
if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    mi_app = ChMaquina()
    mi_app.memoriaTotal(0)
    sys.exit(aplicacion.exec_())
