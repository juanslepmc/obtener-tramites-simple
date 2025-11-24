# Exportador de Trámites a Excel
Este proyecto consiste en un script de Python diseñado para automatizar la extracción de datos de trámites desde una API REST y exportarlos a un reporte en formato Excel (.xlsx).

## Funcionalidades

* Conexión a API: Se conecta a la API de trámites utilizando un token de autenticación seguro y una URL base configurable.

* Paginación Automática: Recorre todas las páginas de resultados de la API automáticamente hasta obtener la totalidad de los registros.

* Procesamiento de Datos:

* Extrae campos principales (ID, Estado, Fechas).

* Aplana estructuras anidadas complejas (el arreglo datos) para extraer información específica dinámica definida por el usuario (ej. "Año Matrícula", "Comuna").

* Exportación a Excel: Genera un archivo .xlsx limpio y ordenado con la información consolidada.

* Configurable: Utiliza variables de entorno para facilitar el cambio de credenciales, URLs y campos a exportar sin tocar el código fuente.

##  Requisitos Previos
Python 3.8 o superior.

pip (gestor de paquetes de Python).

## Instalación

* Clonar o descargar el proyecto en tu carpeta local.

* Instalar las dependencias ejecutando el siguiente comando en la terminal (asegúrate de estar en la carpeta del proyecto):

```
pip install -r requirements.txt

```

## Configuración (.env)

```
TRAMITES_API_TOKEN = <token>
TRAMITES_API_BASE_URL = <url>
CAMPOS_DATOS_EXPORTAR = <string con todos los campos>
```

## Ejecución

```
python main.py
```

## Resultado 

Una vez finalizado el proceso, encontrarás un nuevo archivo en la carpeta del proyecto llamado:

* reporte_tramites.xlsx