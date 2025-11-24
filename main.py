import requests
import sys
import os
from dotenv import load_dotenv
import pandas as pd # Importamos la librería pandas para manejar y exportar datos a Excel

# 1. Cargar las variables de entorno desde el archivo .env
# Esto debe ejecutarse al inicio para que os.getenv() pueda leer el archivo.
load_dotenv()

# La URL base de la API, incluyendo el proceso ID.
API_BASE_URL = os.getenv('URL_API', '')

# 2. Obtener el token de la API desde la variable de entorno 'TRAMITES_API_TOKEN'
# Usamos os.getenv() para leer la variable. Si no existe, el script sale con un error.
API_TOKEN = os.getenv('TRAMITES_API_TOKEN', '')
if not API_TOKEN:
    print("Error: La variable de entorno TRAMITES_API_TOKEN no está configurada. Asegúrese de tener un archivo .env válido.", file=sys.stderr)
    sys.exit(1) # Salimos del programa si no hay token

API_PARAMS = {
    'maxResults': 20,
    'token': API_TOKEN
}

def fetch_all_tramites():
    """
    Obtiene todos los trámites de la API manejando la paginación con un token.
    El token es cargado de forma segura desde las variables de entorno.
    """
    tramites = []
    next_page_token = None
    
    print("Iniciando la obtención de trámites...")

    try:
        # El bucle 'while True' simula el 'do...while' de JS, y se rompe con 'break'.
        while True:
            # Creamos una copia de los parámetros base para añadir el token de la página
            params = API_PARAMS.copy()
            
            # Si existe un token de página, lo agregamos a los parámetros de la solicitud
            if next_page_token:
                params['pageToken'] = next_page_token
                print(f"  -> Solicitando página con token: {next_page_token[:10]}...")
            else:
                print("  -> Solicitando la primera página...")

            # Realizar la solicitud a la API
            response = requests.get(API_BASE_URL, params=params)

            # Comprobar si la respuesta fue exitosa (código 200-299)
            # Esto es equivalente a '!response.ok' de JS y lanzará una excepción si falla.
            response.raise_for_status()

            data = response.json()

            # Extraer los datos y el token de la siguiente página, siguiendo la estructura del JSON.
            # Se usa .get() para evitar errores si las claves no existen.
            tramites_data = data.get('tramites', {})
            items = tramites_data.get('items')
            
            if items and isinstance(items, list):
                # Agregar los trámites obtenidos a la lista principal (tramites.concat en JS)
                tramites.extend(items)
                
                # Actualizar el token para la siguiente iteración
                next_page_token = tramites_data.get('nextPageToken')
                
                # Si el token es None o una cadena vacía, salimos del bucle.
                if not next_page_token:
                    break
            else:
                # Si la estructura del JSON no es la esperada o no hay items
                print('Error: La estructura del JSON no es la esperada o no hay trámites. Deteniendo paginación.')
                break # Salir del bucle si no hay items o la estructura es incorrecta

    except requests.exceptions.RequestException as e:
        # Capturar errores de red, timeouts o errores de respuesta HTTP (e.g., 404, 500)
        print(f'Error al obtener los trámites (requests exception): {e}', file=sys.stderr)
        return []
    except Exception as e:
        # Capturar cualquier otro error, como un fallo al parsear JSON
        print(f'Error inesperado al obtener los trámites: {e}', file=sys.stderr)
        return []

    print(f"Proceso completado. Total de trámites obtenidos: {len(tramites)}")
    return tramites


def export_to_excel(tramites_list, filename="reporte_tramites.xlsx"):
    """
    Exporta una lista de trámites a un archivo Excel (.xlsx), seleccionando
    las columnas principales y extrayendo campos específicos del arreglo 'datos'.
    
    :param tramites_list: Lista de diccionarios con la información completa de los trámites.
    :param filename: Nombre del archivo de salida.
    """
    if not tramites_list:
        print("No hay trámites para exportar. Archivo Excel no generado.")
        return

    # 1. Definir los campos que queremos extraer del nivel superior
    campos_principales = [
        "id",
        "estado",
        "proceso_id",
        "fecha_inicio",
        "fecha_termino",
    ]
    
    # 2. Definir los campos anidados que queremos extraer del arreglo 'datos'
    campos_datos_exportar_str = os.getenv('CAMPOS_DATOS_EXPORTAR', '')
    campos_anidados_datos = []
    # .split(',') crea una lista bruta
    lista_sucia = campos_datos_exportar_str.split(',')           

    for c in lista_sucia:                            # Recorremos la lista sucia
        limpio = c.strip()                           # Quitamos espacios
        if limpio:                                   # Si no está vacío
            campos_anidados_datos.append(limpio)     # Lo guardamos

    datos_exportables = []
    
    for tramite in tramites_list:
        # Inicializar el nuevo diccionario con los campos principales
        registro_final = {campo: tramite.get(campo) for campo in campos_principales}

        # 3. Procesar el arreglo 'datos' para aplanar los campos
        datos_anidados = tramite.get('datos', [])
        
        # El arreglo 'datos' es una lista de objetos donde cada uno tiene una sola clave.
        # Lo convertimos en un único diccionario de mapeo {clave: valor}
        datos_aplanados = {}
        for item in datos_anidados:
            # Copiamos todas las claves y valores en el diccionario aplanado
            datos_aplanados.update(item)
            
        # 4. Extraer solo los campos anidados requeridos del diccionario aplanado
        for campo in campos_anidados_datos:
            # Intentamos obtener el valor y lo añadimos al registro final
            # Usamos .get(campo, None) para manejar casos donde el campo no exista
            registro_final[campo] = datos_aplanados.get(campo)

        datos_exportables.append(registro_final)

    # 5. Crear un DataFrame de pandas a partir de los datos filtrados
    df = pd.DataFrame(datos_exportables)

    try:
        # 6. Exportar el DataFrame a un archivo Excel.
        df.to_excel(filename, index=False)
        print(f"\nÉxito: Datos exportados a '{filename}' ({len(df)} filas).")
    except Exception as e:
        print(f"\nError al intentar guardar el archivo Excel '{filename}': {e}", file=sys.stderr)


# Ejemplo de uso:
if __name__ == '__main__':
    all_tramites = fetch_all_tramites()
    
    # Exportar los trámites obtenidos a Excel
    export_to_excel(all_tramites)