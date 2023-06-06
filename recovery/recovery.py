# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recovery.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/06/06 18:53:00 by alexsanc          #+#    #+#              #
#    Updated: 2023/06/06 19:13:20 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
Crear un programa que, dado un rango de fechas, sea capaz de extraer diversa información
de un sistema Windows como la actividad del usuario, los programas abiertos, el historial
de navegación, distinta información del registro de Windows... en dicho rango de tiempo.

El programa recibirá un rango de fechas y mostrará por consola una lista ordenada de ficheros,
directorios y programas abiertos en dicho rango de tiempo.

Usará el módulo 'argparse' para recibir los parámetros de entrada.
"""

import win32com.client # pip install pywin32 (Windows API)
import win32evtlog # pip install pypiwin32 (Windows API)
import argparse
import datetime
import logging
import winapps # pip install winapps, en VM win10
import winreg
import wmi # pip install wmi (Windows Management Instrumentation). En VM win10
import os

from browser_history import get_history # pip install browser-history (solo en VM win10). Acceso OK en Chrome, Firefox y Edge.


# Constantes.
# Leer argumentos de entrada al programa.
def leer_argumentos():
    analizador = argparse.ArgumentParser(
        description='Informacion de registro, navegador, programas y otras fuentes en WIN10.',
    )
    
	# Inicio del rango de fechas. Si no se especifica, automáticamente se toma la fecha 0 (01-01-1970).
    analizador.add_argument(
        '-i',
        metavar='inicio',
        help="Indica fecha inicial del rango. Si no se especifica, se toma la fecha 0 (01-01-1970)."
    )

    # Fecha de fin. Si no se especifica, automáticamente se toma la fecha actual.
    analizador.add_argument(
        '-f',
        metavar='final',
        help="Indica fecha final del rango. Si no se especifica, se toma la fecha actual."
    )

    analizador = analizador.parse_args()

    return analizador.i, analizador.f
# Esta nueva forma de realizar el programa es más eficiente, ya que se evita repetir código. Returnea la lista con los datos que se le pide.


# Tratar las fechas recibidas. Si no se especifican, se toman por defecto. Si se especifican, se comprueba que son válidas.
# La comprobación de fechas se hace en la función 'tratar_fechas'. Esto se hace tomando como referencia el formato 'DD-MM-AAAA'.
def tratar_fechas(inicio, final):
    try:
        # Comprobar los argumentos recibidos.
		# El primer if comprueba si se ha especificado la fecha de inicio y no la de fin. Si es así, se toma la fecha actual.
        if inicio and not final:
            inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
            final = datetime.datetime.now()

		# El segundo if comprueba si se ha especificado la fecha de fin y no la de inicio. Si es así, se toma la fecha 0.
        elif not inicio and final:
            inicio = datetime.datetime.fromtimestamp(0)
            final = datetime.datetime.strptime(final, '%d-%m-%Y')

		# El tercer if comprueba si no se ha especificado ninguna fecha. Si es así, se toma el rango por defecto (30 días atrás).
        elif not inicio and not final:

            # Fecha de ejecución del programa.
            ahora = datetime.datetime.now()

            # Un mes antes de la fecha de hoy.
            inicio = ahora - datetime.timedelta(days=30)
            final = ahora

            print('No se indicaron fechas. Se tomaron las fechas por defecto (últimos 30 días).\n')

		# El cuarto if comprueba si se ha especificado la misma fecha para inicio y fin. Si es así, se toma la fecha actual.
        elif inicio == final:
            inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
            final = inicio + datetime.timedelta(days=1)

		# Este else comprueba si se han especificado ambas fechas. Si es así, se comprueba que son válidas.
        else:
            inicio = datetime.datetime.strptime(inicio, '%d-%m-%Y')
            final = datetime.datetime.strptime(final, '%d-%m-%Y')

            # Comprobar que las fechas están ordenadas.
            if final < inicio:
                print("La fecha inicial es mayor que la fecha final, desea invertir las fechas? (s/n)")
                respuesta = input().lower()

                if respuesta == 's':
                    inicio, final = final, inicio
                    print("Fechas invertidas.")

                else:
                    if respuesta == 'n':
                        print("Fechas no invertidas, ademas eres un poco tonto, no?")

                    else:
                        print("Opción no válida.")

                    exit()

    except:
        print("Formato invalido. El formato debe ser DD-MM-AAAA.")
        exit()

    return inicio, final


# Lista ficheros en una ruta de forma recursiva.
# Devuelve una lista con los ficheros encontrados.
def ficheros(ruta, extension):

    lista = []

    for ruta, _, ficheros in os.walk(ruta):

        # Comprobar que el fichero tiene la extensión indicada.
        for fichero in ficheros:
            if extension is None or fichero.endswith("." + extension):
                # Añadir el fichero a la lista.
                lista.append(os.path.join(ruta, fichero))

    return lista

# Cambios en el registro, en un intervalo de fechas.
# Devuelve una lista con las fechas en las que se cambiaron ramas del registro.
def cambios_ramas_registro(inicio, final):

    # Conjunto de fechas en las que se cambiaron ramas del registro.
    cambios = set()

    # Tipos de registros a analizar. Usa la API de Windows para acceder al registro.
	# Usamos HKEY_LOCAL_MACHINE y HKEY_CURRENT_USER ya que son los más comunes.
    tipos_clave = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]

    # Obtener los cambios.
    for clave in tipos_clave:
        try:
            # Navegar por el registro. Se accede a la rama 'Run' de la clave 'Software\\Microsoft\\Windows\\CurrentVersion'.
            manejador = winreg.OpenKey(
                clave, "Software\\Microsoft\\Windows\\CurrentVersion\\Run")

            # Usar la función 'QueryInfoKey' para obtener la fecha del cambio.
            timestamp = winreg.QueryInfoKey(
                manejador)[2] / 10000000 - 11644473600

            # Obtener la fecha del cambio (en formato 'DD-MM-AAAA').
            fecha = datetime.datetime.fromtimestamp(timestamp)

            # Comprobar que la fecha está dentro del intervalo de fechas.
            if inicio <= fecha <= final:
                # Añadir la fecha al conjunto de cambios.
                cambios.add((fecha, clave))

        except:
            pass

    return cambios


def archivos_recientes(inicio, final):
    """
    Obtiene los archivos recientes en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de archivos recientes.
    """

    # Conjunto de archivos recientes
    archivos = set()

    # Obtener el directorio de archivos reciente por defecto.
    directorio = os.environ['USERPROFILE'] + \
        '\\AppData\\Roaming\\Microsoft\\Windows\\Recent'

    # Obtener todos enlaces directos del directorio de archivos recientes.
    for archivo in os.listdir(directorio):
        # Comprobar que el elemento es un archivo '.lnk' (enlace simbólico de Windows).
        if archivo.endswith('.lnk'):
            # Obtener la ruta real de los enlaces.
            shell = win32com.client.Dispatch("WScript.Shell")
            ruta = shell.CreateShortCut(directorio + '\\' + archivo).targetpath

            if os.path.isfile(ruta):
                # Obtener la fecha de creación del enlace (sin la hora).
                fecha = datetime.datetime.fromtimestamp(
                    os.path.getctime(directorio + '\\' + archivo))

                # Comprobar que el archivo está dentro del rango de fechas.
                if inicio <= fecha <= final:
                    archivos.add((fecha, ruta))

    return archivos


def archivos_temporales(inicio, final):
    """
    Obtiene los archivos temporales en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de archivos temporales.
    """

    # Conjunto de archivos temporales
    archivos = set()

    # Obtener el directorio de archivos temporales por defecto.
    directorio = os.environ['USERPROFILE'] + '\\AppData\\Local\\Temp'

    # Obtener todos enlaces directos del directorio de archivos temporales.
    for archivo in ficheros(directorio, None):
        try:
            # Obtener la fecha de creación del archivo.
            fecha = datetime.datetime.fromtimestamp(os.path.getctime(archivo))

            # Comprobar que el archivo está dentro del rango de fechas.
            if inicio <= fecha <= final:
                archivos.add((fecha, archivo))

        except:
            pass

    return archivos


def programas_abiertos():
    """
    Obtiene los procesos abiertos en este momento.
    Los "programas" abiertos según el subject en español.

    :return: Lista de procesos abiertos.
    """

    # Lista de procesos abiertos.
    procesos = []

    # Obtener todos los procesos abiertos.
    for proceso in conexion.Win32_Process():
        procesos.append(proceso.Name)

    return procesos


def programas_instalados(inicio, final):
    """
    Obtiene los programas instalados en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de programas instalados.
    """

    # Conjunto grande de programas instalados.
    programas = set(
        programa.Name for programa in conexion.Win32_InstalledWin32Program())

    # Conjunto de programas instalados.
    aplicaciones = set()

    # Obtener programas instalados.
    for aplicacion in winapps.list_installed():
        try:
            # Obtener los datos de la aplicación.
            nombre = aplicacion.name
            fecha = aplicacion.install_date
            ruta = aplicacion.uninstall_string      # Ruta del desinstalador.

            # Si no se encuentra la fecha de instalación pero sí la ruta de su desinstalador.
            if not fecha and ruta:
                # Ajustar el texto para que no tenga comillas adicionales.
                if ruta[0] == ruta[-1] == "\"":
                    ruta = ruta[1:-1]

                # Obtener fecha de creación del fichero (desinstalador).
                fecha = datetime.date.fromtimestamp(os.path.getctime(ruta))

            # Si finalmente se encontró una fecha de instalación, mostrarla.
            if fecha is not None and inicio.date() <= fecha <= final.date():
                aplicaciones.add((fecha, nombre))
                programas.remove(nombre)

        except:
            pass

    # Devuelve los programas encontrados y los que no se sabe la fecha.
    return aplicaciones, programas


def historial_navegacion(inicio, final):
    """
    Obtiene el historial de navegación en un rango de fechas.

    :param inicio: Fecha de inicio del rango de fechas.
    :param final: Fecha de fin del rango de fechas.

    :return: Lista de historial de navegación.
    """

    # Desactivar mensajes de logging para evitar 'INFO: <browser> ...'.
    logging.disable(logging.CRITICAL)

    # Conjunto de entradas de todos los historiales.
    entradas = set()

    # Entradas de los historiales de todos los navegadores instalados.
    historiales = get_history().histories

    for entrada in historiales:
        # Obtener datos de la tuplpa.
        fecha, url = entrada

        # Tratar fecha (ya que se obtiene con zona horaria)
        fecha = fecha.replace(tzinfo=None)

        # Comprobar que la entrada está dentro del rango de fechas.
        if inicio <= fecha <= final:
            entradas.add((fecha, url))

    return entradas


def dispositivos_conectados():
    """
    Obtiene información sobre los dispositivos conectados al sistema en este momento.
    Se entiende por "dispositivo" los medios extraíbles y las unidades físicas y lógicas.

    :return: Lista de dispositivos conectados.
    """

    def unidades_fisicas():
        # Conjunto de dispositivos conectados.
        dispositivos = set()

        # Obtener todos los dispositivos conectados.
        if not conexion.Win32_PhysicalMedia():
            print(
                "\033[0;33mNo se han encontrado dispositivos físicos conectados.\033[0m")

        else:
            for dispositivo in conexion.Win32_PhysicalMedia():
                if dispositivo.Name is not None:
                    dispositivos.add(dispositivo.Name)

        return dispositivos

    def medios_extraibles():
        # Conjunto de dispositivos conectados.
        dispositivos = set()

        # Obtener todos los dispositivos conectados.
        if not conexion.Win32_CDROMDrive():
            dispositivos.add(
                "\033[0;33mNo se han encontrado dispositivos CDROMs conectados\033[0m")

        else:
            for dispositivo in conexion.Win32_CDROMDrive():
                if dispositivo.Name is not None:
                    dispositivos.add(dispositivo.Name)

        # Obtener todos los USBs conectados.
        if not conexion.Win32_USBController():
            dispositivos.add(
                "\033[0;33mNo se han encontrado dispositivos USBs conectados\033[0m")

        else:
            for dispositivo in conexion.Win32_USBController():
                if dispositivo.Name is not None:
                    dispositivos.add(dispositivo.Name)

        return dispositivos

    # Conjunto total de dispositivos conectados.
    return unidades_fisicas().union(medios_extraibles())


def eventos_sistema():
    """
    Obtiene los registros de eventos del sistema.

    :return: Lista de eventos del sistema.
    """

    # Inicializar variables auxiliares.
    manejador = win32evtlog.OpenEventLog(None, 'EventLogRegister')
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    # Conjunto de registros.
    registros = set()

    # Obtener todos los registros de eventos.
    for registro in win32evtlog.ReadEventLog(manejador, flags, 0):
        nombre = registro.SourceName
        fecha = registro.TimeWritten.date()

        # Comprobar que la entrada está dentro del rango de fechas.
        if inicio.date() <= fecha <= final.date():
            registros.add((fecha, nombre))

    return registros


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos.
    inicio, final = leer_argumentos()

    # Tratar las fechas recibidas.
    inicio, final = tratar_fechas(inicio, final)

    # Establecer conexión con el sistema.
    conexion = wmi.WMI()

    # Obtener los cambios en las ramas de registro.
    cambios = cambios_ramas_registro(inicio, final)

    # Imprimir los cambios en las ramas de registro.
    print("\033[1mCambios en las ramas de registro:\033[0m")

    for fecha, cambio in sorted(cambios):
        print("\t{}\t{}".format(fecha.strftime("%d-%m-%Y"), cambio))

    # Obtener los archivos recientes en un rango de fechas.
    recientes = archivos_recientes(inicio, final)

    # Imprimir los archivos recientes.
    print("\n\033[1mArchivos recientes:\033[0m")

    for fecha, archivo in sorted(recientes):
        print("\t{}\t{}".format(fecha.strftime("%d-%m-%Y"), archivo))

    # Obtener los archivos temporales en un rango de fechas.
    temporales = archivos_temporales(inicio, final)

    # Imprimir los archivos temporales.
    print("\n\033[1mArchivos temporales:\033[0m")

    for fecha, temporal in sorted(temporales):
        print("\t{}\t{}".format(fecha.strftime("%d-%m-%Y"), temporal))

    # Obtener los programas abiertos en un rango de fechas.
    abiertos = programas_abiertos()

    # Imprimir los programas abiertos.
    print("\n\033[1mProgramas (procesos) abiertos:\033[0m")

    for programa in abiertos:
        print("\t" + programa)

    # Obtener programas instalados en un rango de fechas.
    instalados, misteriosos = programas_instalados(inicio, final)

    # Imprimir los programas instalados.
    print("\n\033[1mProgramas instalados:\033[0m")

    for (fecha, nombre) in sorted(instalados):
        print("\t{}\t{}".format(fecha.strftime('%d-%m-%Y'), nombre))

    print("\n\t\033[1mProgramas instalados que no se sabe la fecha:\033[0m")

    for nombre in misteriosos:
        print("\t\t" + nombre)

    # Obtener el historial de navegación en un rango de fechas.
    historial = historial_navegacion(inicio, final)

    # Imprimir el historial de navegación.
    print("\n\033[1mHistorial de navegación:\033[0m")

    for entrada in sorted(historial):
        print("\t{}\t{}".format(entrada[0].strftime("%d-%m-%Y"), entrada[1]))

    # Obtener los dispositivos conectados en este momento.
    dispositivos = dispositivos_conectados()

    # Imprimir los dispositivos conectados.
    print("\n\033[1mDispositivos conectados:\033[0m")

    for dispositivo in dispositivos:
        print("\t" + dispositivo)

    # Obtener el registro de eventos del sistema.
    registros = eventos_sistema()

    # Imprimir los registros de eventos.
    print("\n\033[1mRegistros de eventos:\033[0m")

    for (fecha, nombre) in sorted(registros):
        print("\t{}\t{}".format(fecha.strftime('%d-%m-%Y'), nombre))
