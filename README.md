# BikeStore

Sistema de gestión de inventario de bicicletas desarrollado con Django y MariaDB para la asignatura de Programación Backend.

Cuenta con un CRUD funcional. El inicio muestra las referencias registradas y el stock disponible.

## Ejecución

Con MySQL iniciado en XAMPP y el entorno virtual activo, instalar las dependencias si es necesario:

```powershell
python -m pip install -r requirements.txt
```

Crear la base de datos `bikestore_db` y configurar el archivo `.env` a partir de `.env.example` con las credenciales locales. Luego ejecutar:

```powershell
python manage.py migrate
python manage.py runserver
```

Abrir http://127.0.0.1:8000/

## Pruebas

```powershell
python manage.py test bicicletas
```

Las 19 pruebas se ejecutaron correctamente con MariaDB. El usuario de la base de datos necesita permisos sobre `test_bikestore_db` para ejecutarlas.

Desarrollo: Iván Morales
