# workflow

instructiones:

1. Descargar e instalar el intérprete de Python en www.python.org  (https://www.python.org/ftp/python/3.7.3/python-3.7.3.exe - aquí le facilito el link a la vesión más actual)
    -Al momento de instalarlo asegurarse de agregar Python a PATH para su fácil uso en Linea de Comando (CMD) o PowerShell (PS)

2. Descomprimir y ubicar la carpeta del proyecto en un lugar de fácil para su uso en CMD, o estando en la carpeta puede hacer "ClicDerecho + Shift" aparecerá una opción diciendo: "Open CommandLine (o PS) window here"

3. Crear base de datos. Por motivos de simpleza, se incluyen dos archivos .slq los cuales constan de una base
    de datos en esqueleto y otra con el sufijo "_test.sql" que tiene ya agregado records de prueba, especificamente:
    3 empleados (empleado común, gerente de planta y contador), 3 departamentos y gerentes (control, planta y finanzas). Más información en NOTAS.
    
4. Ejecutar los siguientes comandos:
    - virtualenv venv
        * Crea un entorno virtual, por cuestiones de organización y limpieza del entorno
    - venv/Scripts/activate
        * activa el entorno virtual
    - pip install -r requirements.txt
        * instala todas las dependencias requeridas actualmente por el proyecto
    - python webserver..py
        *ejecuta el proyecto  -- Revisar webserver.py para verificar que dirección ip (nombre del host) y puerto se usan para acceder al sitio



NOTAS: 
    - Si se usa la base de datos esqueleto (requisiciones.sql), se aconseja crear las instancias en este flujo: Departamentos -> Empleados -> Manager debido a las restricciones por las Foreign keys (Constrains) usadas

    -Al iniciar el servidor, se podrá acceder al sitio de dos formas:
        1. Mediante el ip del PC host y el puerto configurado por el proyecto (8080 en este caso) -> IpHost:puerto -- Ejemplo: 192.168.1.128:8080
        2. Mediante la dirección que la Linea de comando le provea al momento de activar "webserver.py"

	
	Creación de base de datos con python:

	*Activar el ambiente virtual en caso de que no esté activo:
 		-virtualenv venv
	Correr los siguientes comandos (Con tabulación incluida. Nota: solo es una tabulación)

from share.db_init() import db
import models.tables
from app import app

with app.app_context():
	db.create_all()
	db.sesssion.commit()
(volver a Presionar Enter)
