import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Simulating database connection leak
# In this function, a new connection is created on every request but is never closed.
@app.route('/payment', methods=['POST'])
def process_payment():
    # Database connection pool leak scenario
    conn = psycopg2.connect("dbname=payments user=postgres")
    cur = conn.cursor()
    cur.execute("SELECT 1")
    result = cur.fetchone()
    
    # BUG: conn.close() is missing here, causing a connection leak!
    # Over time under load, this will exhaust the database connection pool (max_connections = 100).
    cur.close()
    conn.close()
    
    return jsonify({"status": "success", "result": result[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
