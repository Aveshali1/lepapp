from flask import Flask, request, jsonify
import sqlalchemy
import os

app = Flask(__name__)

server = os.environ.get('AZURE_SQL_SERVER')
database = os.environ.get('AZURE_SQL_DATABASE')
username = os.environ.get('AZURE_SQL_USERNAME')
password = os.environ.get('AZURE_SQL_PASSWORD')

# Connection string for pytds
connection_string = f"mssql+pytds://{username}:{password}@{server}:1433/{database}"

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        uid = data['UID']
        name = data['Name']
        gender = data['Gender']

        engine = sqlalchemy.create_engine(connection_string)
        with engine.connect() as conn:
            conn.execute(sqlalchemy.text(
                "INSERT INTO PatientRawSubmission (UID, Name, Gender) VALUES (:uid, :name, :gender)"
            ), {"uid": uid, "name": name, "gender": gender})

        return jsonify({'status': 'success', 'message': 'Data inserted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
