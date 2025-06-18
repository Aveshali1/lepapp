from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Get DB credentials from environment variables
server = os.environ.get('AZURE_SQL_SERVER')
database = os.environ.get('AZURE_SQL_DATABASE')
username = os.environ.get('AZURE_SQL_USERNAME')
password = os.environ.get('AZURE_SQL_PASSWORD')

# Build connection string
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server};DATABASE={database};UID={username};PWD={password}"
)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        uid = data['UID']
        name = data['Name']
        gender = data['Gender']

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO PatientRawSubmission (UID, Name, Gender) VALUES (?, ?, ?)",
                       uid, name, gender)
        conn.commit()
        conn.close()

        return jsonify({'status': 'success', 'message': 'Data inserted'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# Use the port from environment and bind to 0.0.0.0
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
