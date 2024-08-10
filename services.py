import logging, random
import requests
from datetime import datetime

# Configurar el logger
logger = logging.getLogger('MiLogger')
logger.setLevel(logging.DEBUG)
service_name = 'Servicio1'
# URL del servidor Flask
url = 'http://localhost:5000/logs'

# API key para autorización
api_key = 'abc123'

# Función para enviar el log al servidor
def send_log_to_server(timestamp, service_name, severity_level, message):
    # Estructura del log en JSON
    log_entry = {
        'timestamp': timestamp,
        'service_name': service_name,
        'severity_level': severity_level,
        'message': message
    }
    
    try:
        # Envío de la solicitud POST con la API key en el encabezado
        response = requests.post(url, json=log_entry, headers={'Authorization': api_key})
        if response.ok:
            print('Log enviado con éxito')
        else:
            print('Error al enviar el log:', response.text)
    except requests.exceptions.RequestException as e:
        print('Excepción al enviar el log:', e)

# Configurar el StreamHandler para capturar los logs y enviarlos al servidor
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)

# Definir un formato para los logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)

# Añadir una función personalizada al handler para enviar logs al servidor
def handle_log(record):
   
    timestamp = datetime.now().isoformat()
    severity_level = record.levelname
    message = record.getMessage()
    
    # Enviar el log al servidor
    send_log_to_server(timestamp, service_name, severity_level, message)

# Reemplazar la función emit con handle_log
stream_handler.emit = handle_log  
logger.addHandler(stream_handler)

def generate_logs(service_name):
    for i in range(3):
        log_option = random.randint(1,5)

        if log_option == 1:
            logger.debug(f'Este es un mensaje de debug {service_name}')
        elif log_option == 2:
            logger.info(f'Este es un mensaje de información {service_name}')
        elif log_option == 3:
            logger.warning(f'Este es un mensaje de advertencia {service_name}')
        elif log_option == 4:
            logger.error(f'Este es un mensaje de error {service_name}')
        elif log_option == 5:
            logger.critical(f'Este es un mensaje crítico {service_name}')

service_name = 'Servicio1'
generate_logs(service_name)

api_key = 'def456'
service_name = 'Servicio2'
generate_logs(service_name)

api_key = 'ghi789'
service_name = 'Servicio3'
generate_logs(service_name)
