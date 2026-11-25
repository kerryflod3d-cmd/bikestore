BikeStore

Sistema de gestión de inventario de bicicletas desarrollado con Django y MariaDB para la asignatura de Programación Backend de INACAP.

Permite CRUD funcional, controlar el stock y realizar búsquedas y filtros.

Requisitos

Python 3.10 a 3.14 (probado con 3.14.4).

XAMPP con MariaDB 10.5 o superior.

Git.

Instalación y ejecución en Windows

1. Descargar el proyecto

Abrir PowerShell y ejecutar:

cd $HOME
git clone https://github.com/kerryflod3d-cmd/bikestore.git
cd bikestore

También se puede descargar el proyecto como ZIP desde GitHub y abrir una terminal en la carpeta extraída.

2. Crear el entorno virtual

py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

3. Instalar las dependencias

python -m pip install -r requirements.txt

4. Configurar la base de datos

Abrir XAMPP e iniciar Apache y MySQL.

Ingresar a http://localhost/phpmyadmin/ y ejecutar los siguientes comandos en la pestaña SQL, con una cuenta que tenga permisos administrativos:

CREATE DATABASE bikestore_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER 'bikestore_user'@'127.0.0.1'
IDENTIFIED BY 'TU_CONTRASENA';

GRANT ALL PRIVILEGES ON bikestore_db.*
TO 'bikestore_user'@'127.0.0.1';

Reemplazar TU_CONTRASENA por una contraseña propia.

Si la base de datos y el usuario ya existen, utilizar sus credenciales correspondientes.

5. Configurar las variables de entorno

Desde PowerShell:

Copy-Item .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Abrir el archivo .env y completar su contenido:

DJANGO_SECRET_KEY='CLAVE_GENERADA'
DB_NAME=bikestore_db
DB_USER=bikestore_user
DB_PASSWORD='TU_CONTRASENA'
DB_HOST=127.0.0.1
DB_PORT=3306

Utilizar la clave generada y la contraseña definida en MariaDB.

6. Aplicar las migraciones

python manage.py migrate
python manage.py check

7. Iniciar la aplicación

python manage.py runserver

Ingresar a http://127.0.0.1:8000/

Ejecución después de la instalación

Iniciar MySQL desde XAMPP y ejecutar desde la carpeta del proyecto:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python manage.py runserver

Pruebas

Para ejecutar las pruebas automatizadas, otorgar permisos sobre la base de datos de pruebas desde phpMyAdmin:

GRANT ALL PRIVILEGES ON test_bikestore_db.*
TO 'bikestore_user'@'127.0.0.1';

Luego ejecutar:

python manage.py test bicicletas

El proyecto superó las 19 pruebas automatizadas utilizando MariaDB.

Autor

Iván Morales.
