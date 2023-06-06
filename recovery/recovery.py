# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    recovery.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/06/06 18:53:00 by alexsanc          #+#    #+#              #
#    Updated: 2023/06/06 21:39:39 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import win32com.client  # pip install pywin32 (Windows API)
import win32evtlog  # pip install pypiwin32 (Windows API)
import argparse
import datetime
import logging
import winapps  # pip install winapps, en VM win10
import winreg
import wmi  # pip install wmi (Windows Management Instrumentation). En VM win10
import os

# pip install browser-history (solo en VM win10). Acceso OK en Chrome, Firefox y Edge.
from browser_history import get_history


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

            print(
                'No se indicaron fechas. Se tomaron las fechas por defecto (últimos 30 días).\n')

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
                print(
                    "La fecha inicial es mayor que la fecha final, desea invertir las fechas? (s/n)")
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

    except ValueError:
    # Tambien podemos usar assert para comprobar que las fechas son válidas.
	# assert inicio < final, "La fecha inicial es mayor que la fecha final."
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


def cambios_registro(inicio, final):

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

        except OSError:
            pass

    return cambios

# Se obtienen los cambios en el registro, en un intervalo de fechas.
# Devuelve una lista con las fechas en las que se cambiaron ramas del registro.


def archivos_recientes(inicio, final):

    # Conjunto de archivos recientes
    archivos = set()

    # Obtener el directorio de archivos reciente por defecto.
    # En Recent se guardan los accesos directos a los archivos abiertos recientemente, por lo que se puede obtener la ruta real de los archivos.
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
                # Obtener la fecha de creación del enlace.
                # No confundir con la fecha de creación del archivo.
                # No contiene la hora.
                fecha = datetime.datetime.fromtimestamp(
                    os.path.getctime(directorio + '\\' + archivo))

                # Comprobar que el archivo está dentro del rango de fechas.
                # Si la fecha de creación del enlace es anterior a la fecha de inicio, se toma la fecha de inicio.
                if inicio <= fecha <= final:
                    archivos.add((fecha, ruta))

    return archivos


# Obtener todos los temps en un rango de fechas.
# Usaremos AppData Local Temp, ya que es el directorio por defecto de Windows.
# Devuelve una lista con los archivos temporales encontrados.
# El proceso es mas o menos el mismo que en archivos_recientes.
def archivos_temporales(inicio, final):

    # Creamos el conjunto de archivos temporales
    archivos = set()

    directorio = os.environ['USERPROFILE'] + '\\AppData\\Local\\Temp'

    for archivo in ficheros(directorio, None):
        try:
            fecha = datetime.datetime.fromtimestamp(os.path.getctime(archivo))

            if inicio <= fecha <= final:
                archivos.add((fecha, archivo))

        except OSError:
            pass

    return archivos


# Obtener los programas abiertos en este momento.
# Tendremos en cuenta que un programa es un proceso y seguiremos
# la nomenclatura de Windows.
# Devuelve una lista con los programas abiertos.
# Hay que tener en cuenta que el subject en ingles y en español no es el mismo.
def programas_abiertos():

    # Creamos la lista.
    procesos = []

    # Obtenemos todos los procesos abiertos.
    for proceso in conexion.Win32_Process():
        procesos.append(proceso.Name)

    return procesos


# Obtener los programas instalados en un rango de fechas.
# Devuelve una lista con los programas instalados.
# Se usa la librería winapps para obtener los programas instalados.
# Haremos distincion entre los programas que se sabe la fecha de instalación y los que no.
def programas_instalados(inicio, final):

    # Conjunto grande de programas instalados.
    programas = set(
        programa.Name for programa in conexion.Win32_InstalledWin32Program())

    # Conjunto de programas instalados.
    # Diferenciamos entre apps y programas porque no se puede obtener la fecha de instalación de las apps.
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
                # Por ejemplo, '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --uninstall --multi-install --chrome --system-level' -> 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                if ruta[0] == ruta[-1] == "\"":
                    ruta = ruta[1:-1]

                # Obtener fecha de creación del fichero (desinstalador).
                fecha = datetime.date.fromtimestamp(os.path.getctime(ruta))

            # Si finalmente se encontró una fecha de instalación, mostrarla.
            if fecha is not None and inicio.date() <= fecha <= final.date():
                aplicaciones.add((fecha, nombre))
                programas.remove(nombre)

        except OSError:
            pass

    # Devuelve los programas encontrados y los que no se sabe la fecha.
    return aplicaciones, programas


# Obtener el historial de navegación en un rango de fechas.
# Devuelve una lista con el historial de navegación.
# Se usa la librería browser-history para obtener el historial de navegación.
# Esta librería solo funciona en Windows 10 y con los navegadores Chrome, Firefox y Edge.
def historial_navegacion(inicio, final):

    # Desactivar mensajes de logging para evitar 'INFO: <browser> history not found', ya que no es relevante.
    logging.disable(logging.CRITICAL)

    # Conjunto de entradas de todos los historiales.
    entradas = set()

    # Entradas de los historiales de todos los navegadores instalados.
    historiales = get_history().histories

    for entrada in historiales:
        # Obtener datos de la tupla.
        fecha, url = entrada

        # Tratar fecha (ya que se obtiene con zona horaria)
        fecha = fecha.replace(tzinfo=None)

        # Comprobar que la entrada está dentro del rango de fechas.
        if inicio <= fecha <= final:
            entradas.add((fecha, url))

    return entradas


# Obtener los dispositivos conectados en este momento.
# Devuelve una lista con los dispositivos conectados.
# Incluye medios extraíbles y unidades físicas y lógicas.
def dispositivos_conectados():

    def unidades_fisicas():
        # Conjunto de dispositivos conectados.
        dispositivos = set()

        # Obtener todos los dispositivos conectados con la API de Windows.
        if not conexion.Win32_PhysicalMedia():
            print(
                "No se han encontrado dispositivos físicos conectados.")

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
                "No se han encontrado dispositivos CDROMs conectados")

        else:
            for dispositivo in conexion.Win32_CDROMDrive():
                if dispositivo.Name is not None:
                    dispositivos.add(dispositivo.Name)

        # Obtener todos los USBs conectados.
        if not conexion.Win32_USBController():
            dispositivos.add(
                "No se han encontrado dispositivos USBs conectados")

        else:
            for dispositivo in conexion.Win32_USBController():
                if dispositivo.Name is not None:
                    dispositivos.add(dispositivo.Name)

        return dispositivos

    # Conjunto total de dispositivos conectados.
    # Se usa unión para evitar duplicados.
    return unidades_fisicas().union(medios_extraibles())


# Obtener los registros de eventos del sistema.
# No confundir con los registros de eventos de Windows.
# Devuelve una lista con los registros de eventos.
def eventos_sistema():

    # Inicializar variables auxiliares.
    manejador = win32evtlog.OpenEventLog(None, 'EventLogRegister')
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    # Conjunto de registros de eventos como tuplas (fecha, nombre).
    registros = set()

    # Obtener todos los registros de eventos.
    for registro in win32evtlog.ReadEventLog(manejador, flags, 0):
        nombre = registro.SourceName
        fecha = registro.TimeWritten.date()

        # Comprobar que la entrada está dentro del rango de fechas.
        # Mismo proceso que en historial_navegacion y archivos_recientes...
        if inicio.date() <= fecha <= final.date():
            registros.add((fecha, nombre))

    return registros


# Toda la información obtenida se imprime por pantalla.
if __name__ == "__main__":
    # Leer los argumentos de la línea de comandos.
    inicio, final = leer_argumentos()

    # Tratar las fechas recibidas.
    inicio, final = tratar_fechas(inicio, final)

    # Establecemos conexion con el sistema usando la libreria wmi.
    conexion = wmi.WMI()

    # Obtener los cambios en las ramas de registro.
    cambios = cambios_registro
    (inicio, final)
    print("Cambios en el registro:")

    for fecha, cambio in sorted(cambios):
        print("\t{}\t{}".format(fecha.strftime("%d-%m-%Y"), cambio))

    # Obtener los archivos recientes en un rango de fechas.
    recientes = archivos_recientes(inicio, final)
    print("Archivos recientes:")

    for fecha, archivo in sorted(recientes):
        print("\t{}\t{}".format(fecha.strftime("%d-%m-%Y"), archivo))

    # Obtener los archivos temporales en un rango de fechas.
    temporales = archivos_temporales(inicio, final)
    print("Archivos temporales:")

    for fecha, temporal in sorted(temporales):
        print("\t{}\t{}".format(fecha.strftime("%d-%m-%Y"), temporal))

    # Obtener los programas abiertos en un rango de fechas.
    abiertos = programas_abiertos()
    print("Programas (procesos) abiertos:")

    for programa in abiertos:
        print("\t" + programa)

    # Obtener programas instalados en un rango de fechas.
    instalados, misteriosos = programas_instalados(inicio, final)
    print("Programas instalados:")

    for (fecha, nombre) in sorted(instalados):
        print("\t{}\t{}".format(fecha.strftime('%d-%m-%Y'), nombre))

    print("\nProgramas instalados que no se sabe la fecha:")

    for nombre in misteriosos:
        print("\t\t" + nombre)

    # Obtener el historial de navegación en un rango de fechas.
    historial = historial_navegacion(inicio, final)
    print("\nHistorial de navegación:")

    for entrada in sorted(historial):
        print("\t{}\t{}".format(entrada[0].strftime("%d-%m-%Y"), entrada[1]))

    # Obtener los dispositivos conectados en este momento.
    dispositivos = dispositivos_conectados()
    print("\nDispositivos conectados:")

    for dispositivo in dispositivos:
        print("\t" + dispositivo)

    # Obtener el registro de eventos del sistema.
    registros = eventos_sistema()
    print("\nRegistros de eventos:")

    for (fecha, nombre) in sorted(registros):
        print("\t{}\t{}".format(fecha.strftime('%d-%m-%Y'), nombre))
