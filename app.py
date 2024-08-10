from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Configurando sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
db = SQLAlchemy(app)

#Creando la base de datos
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    timestamp = db.Column(db.String, nullable = False)  
    service_name = db.Column(db.String, nullable = False)
    severity_level = db.Column(db.String, nullable = False)
    message = db.Column(db.String, nullable = False) 

with app.app_context():
    db.create_all()

VALID_API_KEYS = {
    "service_1": "abc123",
    "service_2": "def456",
    "service_3": "ghi789"
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logs', methods = ['POST'])
def receive_logs():
    api_key = request.headers.get('Authorization')

    if api_key not in VALID_API_KEYS.values():
        return jsonify({'error' : 'Acceso no autorizado'}), 401
    
    log_data = request.get_json()

    log_fields = {'timestamp', 'service_name', 'severity_level', 'message'}

    if log_data and log_fields.issubset(log_data):
        # Creación de un nuevo objeto Log
        new_log = Log(
            timestamp=log_data['timestamp'],
            service_name=log_data['service_name'],
            severity_level=log_data['severity_level'],
            message=log_data['message']
        )
        # Añadir y guardar el log en la base de datos
        db.session.add(new_log)
        db.session.commit()

        return jsonify({'status' : 'Log recibido con éxito'}), 200
    else:
        return jsonify({'error' : 'Error fatal. Datos inválidos'}), 400

@app.route('/logs/filter', methods=['GET'])
def filter_logs():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Log.query

    if start_date and end_date:
        # Convertir las fechas a objetos datetime
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Filtrar por rango de fechas
        query = query.filter(Log.timestamp.between(start_date, end_date))

    logs = query.all()

    result = []
    for log in logs:
        log_data = {
            'id': log.id,
            'timestamp': log.timestamp,
            'service_name': log.service_name,
            'severity_level': log.severity_level,
            'message': log.message
        }
        result.append(log_data)

    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)