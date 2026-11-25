# BikeStore

Aplicación académica de gestión de inventario de bicicletas, para Programación Backend (Django + MySQL/MariaDB).

**Estudiante:** Iván Rodrigo Morales Pérez.  
**Entidad:** Bicicleta.  
**Modalidad:** individual, con asistencia de IA para el desarrollo y estudio. La evaluación de la modalidad individual corresponde al docente.

## Funcionalidades

- Inicio con indicadores calculados desde la base de datos.
- Listado, búsqueda por marca/modelo y filtro por tipo.
- Formularios diferenciados de creación y edición; validación en el servidor.
- Eliminación con pantalla de confirmación y solicitud POST protegida por CSRF.
- Diseño adaptable con CSS local. No requiere CDN, JavaScript, login ni registro de usuarios.

## Requisitos

El entorno de referencia del estudiante usa Python 3.14.4, Django 5.2.19, mysqlclient 2.3.2 y MariaDB 10.11.19 (XAMPP). Las versiones exactas de Python y las dependencias corresponden al entorno existente; consultar `requirements.txt`.

## Ejecutar en el equipo existente

Con MySQL de XAMPP iniciado, abrir PowerShell en `bikestore` y activar el entorno existente si no está activo:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python manage.py check
python manage.py migrate
python manage.py makemigrations --check --dry-run
python manage.py runserver
```

Abrir http://127.0.0.1:8000/. Apache solo es necesario para utilizar phpMyAdmin. Mantener `.env` existente en la raíz, fuera de Git. No sustituirlo por `.env.example`.

## Instalación desde cero (solo si hace falta)

1. Instalar Python compatible y XAMPP con MariaDB compatible con Django 5.2.
2. Crear el entorno: `py -3.14 -m venv .venv`; activarlo e instalar `python -m pip install -r requirements.txt`.
3. En phpMyAdmin (SQL), ejecutar, reemplazando la contraseña de ejemplo:

```sql
CREATE DATABASE bikestore_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bikestore_user'@'127.0.0.1' IDENTIFIED BY 'CONTRASENA_LOCAL_SEGURA';
GRANT ALL PRIVILEGES ON bikestore_db.* TO 'bikestore_user'@'127.0.0.1';
```

4. Copiar `.env.example` a `.env`, rellenar los valores; generar una clave secreta con `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. No compartirla.
5. Aplicar migraciones y ejecutar el servidor según las instrucciones anteriores.

## Arquitectura

| Archivo | Función |
|---|---|
| `config/settings.py` | Configuración, variables de entorno, conexión MariaDB |
| `config/urls.py` | Delega rutas a la aplicación |
| `bicicletas/models.py` | Modelo y reglas de datos |
| `bicicletas/migrations/0001_initial.py` | Migración inicial existente |
| `bicicletas/forms.py` | ModelForms de creación y edición |
| `bicicletas/views.py` | Funciones HTTP y consultas ORM |
| `bicicletas/urls.py` | Rutas del inventario |
| `templates/` | HTML renderizado por Django |
| `bicicletas/static/bicicletas/estilos.css` | Estilos locales |
| `bicicletas/tests.py` | Pruebas automatizadas |

## Pruebas automatizadas con MariaDB

Django crea una base de pruebas separada llamada `test_bikestore_db`. El usuario de la aplicación original tiene permisos solo sobre `bikestore_db`; por ello, desde phpMyAdmin con el usuario administrador, conceder permisos adicionales **solo sobre la base de pruebas**:

```sql
GRANT ALL PRIVILEGES ON test_bikestore_db.* TO 'bikestore_user'@'127.0.0.1';
```

Después, en PowerShell:

```powershell
python manage.py test bicicletas -v 2
```

Se esperan 19 métodos de prueba (uno contiene 11 subcasos de datos inválidos). También se verifican búsqueda y filtro por separado, métodos HTTP no permitidos y restricciones de precio y stock directamente en MariaDB. Django crea y elimina la base de pruebas; no modifica el inventario habitual. No aceptar eliminar una base de pruebas preexistente si no se conoce su contenido. Las pruebas se entregan sin ejecución en el entorno de autoría, que no dispone de Django/MariaDB ni acceso a sus paquetes.

## Demostración de persistencia

En la web, crear un registro, consultar la tabla `bicicletas_bicicleta` desde phpMyAdmin, editar el precio y stock, comprobar los cambios, luego eliminar un registro de prueba y verificar su ausencia. Puede consultarse desde la pestaña SQL:

```sql
SELECT id, marca, modelo, tipo, aro, precio, stock
FROM bicicletas_bicicleta ORDER BY id;
```

Ejemplos de datos ficticios para el inventario de la presentación:

| Marca | Modelo | Tipo | Aro | Color | Precio CLP | Stock |
|---|---|---|---|---|---:|---:|
| Trek | Marlin 5 | Mountain Bike | 29 | Negro | 399990 | 5 |
| Oxford | Orion | Urbana | 26 | Azul | 199990 | 3 |
| Giant | Escape 3 | Urbana | 28 | Gris | 299990 | 0 |

## Alcance y seguridad

Proyecto académico local; `DEBUG=True` y sin autenticación por requisito. No publicar el servidor en Internet. `.env`, `.venv` y cachés se excluyen del control de versiones. La ausencia de `.env` en el ZIP no sanea el historial anterior de Git: comprobar que no figure en ninguna rama antes de publicar. Mantener los commits reales del estudiante y documentar la asistencia recibida si el docente la solicita.
