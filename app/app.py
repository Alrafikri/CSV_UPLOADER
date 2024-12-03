from flask import Flask, request, jsonify
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, text

app = Flask(__name__)

# Set up PostgreSQL connection
DATABASE_URL = "postgresql://alrafikri:password@db:5432/lelesg"
engine = create_engine(DATABASE_URL)

@app.route('/upload', methods=['POST'])
def upload_csv():
    file = request.files['file']
    table_name = request.form['table_name']
    df = pd.read_csv(file)
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    return jsonify({'message': 'File uploaded successfully'})

@app.route('/tables', methods=['GET'])
def get_tables():
    query = text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    with engine.connect() as connection:
        result = connection.execute(query)
        tables = [row[0] for row in result]
    return jsonify(tables)

@app.route('/query', methods=['POST'])
def run_query():
    sql_query = request.json['query']
    query = text(sql_query)
    with engine.connect() as connection:
        result = connection.execute(query)
        rows = [dict(zip(result.keys(), row)) for row in result]
    return jsonify({'results': rows})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
