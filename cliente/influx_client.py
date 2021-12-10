#!/usr/bin/env python3
from influxdb import InfluxDBClient
from datetime import datetime

def subir_comentario(client):
    # Crear y escribir en la base de datos una nueva entrada

    # Leemos por terminal los campos a guardar en la BBDD
    nombre = input("Introduce tu nombre: ")
    tema = input("Introduce el tema de tu comentario: ")
    comentario = input("Escribe el comentario que quieras guardar:\n")

    # Almacenamos los campos en un diccionario que será enviado al cliente de InfluxDB
    data = [{
        "measurement": "comments",      # - Algo similar a la "tabla" en la que almacenamos nuestros comentarios
        "time": datetime.now(),         # - Campo que guarda la fecha y hora en la que es añadido un comentario
        "fields": {                     # - Los valores importantes que queremos almacenar se guardan en el diccionario
            "creador": nombre,          #   "fields"
            "tema": tema,
            "comentario": comentario
        }
    }]

    client.write_points(data)   # Función que escribe los datos (en nuestro caso un solo comentario
                                # cada vez) a en la base de datos de InfluxDB


def leer_comentarios(client):
    # Leer los comentarios existentes

    result = client.query("SELECT * from comments") # Query de todos los datos de todos los comentarios
    comentarios = []    # Array que almacenará todos los comentarios leídos para guardarlos posteriormente
    comentarios.append("{:30}{:13}{:13}{}".format("Fecha","Creador","Tema","Comentario")) # Título. Para que quede elegante
    for t in result:
      for i in t:
        # Loop por todos los comentarios leídos en nuestra query
        comentarios.append("{} | {:10} | {:10} | {}".format(i['time'],i['creador'],i['tema'],i['comentario']))
        print(comentarios[-1])  # Imprimimos el comentario de forma "legible" por pantalla
    print('''
¿Quieres guardar los comentarios?
Podrás acceder a ellos en '/tmp/influx_comentarios/saves.txt'.
AVISO: Sobreescribiras los anteriores comentarios guardados.
''')
    choice = input("Y/n: ")
    try:
    # Si se desea, guardamos los comentarios en el directorio del volumen. Podrán ser accedidos desde el host.
      if (choice.lower() == 'y'):
        f = open("/tmp/influx_comentarios/saves.txt", "w")
        for i in comentarios:
          f.write(i + '\n')
    except Exception:
      pass


def main_loop():
    # Loop principal del programa

    # Creamos el cliente InfluxDB con la librería InfluxDBClient, aportándole los datos necesarios.
    client = InfluxDBClient(host = 'influxDB', port = 8086, username = 'admin', password = 'admin', database = 'influx_db')
    client.switch_database('influx_db') # equivalente a "USE influx_db"
    print('''
Bienvenido al almacen de comentarios.''')
    while True:
        # Loop hasta que se quiera salir del programa.
        print(
'''-------------------------------------------------
Pulse el número de la opción que desees realizar.
Cualquier otra opción terminará la sesión actual.
(1) - Escribir nuevo comentario
(2) - Leer comentarios existentes
''')
        elec = input("Elección: ")
        try:
            elec_int = int(elec)
        except ValueError:
            # No es un número. Salimos del loop.
            break

        if elec_int == 1:
            subir_comentario(client)
        elif elec_int == 2:
            leer_comentarios(client)
        else:
            # No es una elección válida. Salimos del loop.
            break
    print("bye!")


if __name__ == "__main__":
    main_loop()