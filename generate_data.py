import sqlite3
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta

def setup_database():
    conn = sqlite3.connect("tracemind.db")
    cursor = conn.cursor()
    
    # Create a simple table for our metrics and traces
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            timestamp DATETIME,
            trace_id TEXT,
            service_name TEXT,
            endpoint TEXT,
            latency_ms REAL,
            status_code INTEGER
        )
    ''')
    
    # Clear old data for a fresh run
    cursor.execute('DELETE FROM telemetry')
    conn.commit()
    return conn

def generate_simulated_traffic(conn):
    print("Generating 100 normal traces and 1 anomaly cascade...")
    cursor = conn.cursor()
    
    base_time = datetime.now() - timedelta(minutes=60)
    
    # 1. Generate Normal Traffic
    for i in range(100):
        trace_id = f"trace_norm_{i}"
        timestamp = base_time + timedelta(minutes=i*0.5)
        
        # API Gateway -> Order -> Database
        cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", 
                      (timestamp, trace_id, "API_Gateway", "/checkout", np.random.normal(50, 5), 200))
        cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", 
                      (timestamp, trace_id, "Order_Service", "/process", np.random.normal(80, 10), 200))
        cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", 
                      (timestamp, trace_id, "Database", "INSERT", np.random.normal(20, 2), 200))
        
    # 2. Inject a Root Cause Anomaly (Database locks up)
    anomaly_time = datetime.now() - timedelta(minutes=5)
    trace_id = "trace_ANOMALY_CRITICAL"
    
    # Database fails first (Root Cause)
    cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", 
                  (anomaly_time, trace_id, "Database", "INSERT", 5000.0, 503))
    
    # Order service cascades (Symptom 1)
    cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", 
                  (anomaly_time + timedelta(seconds=1), trace_id, "Order_Service", "/process", 5010.0, 500))
    
    # API Gateway cascades (Symptom 2)
    cursor.execute("INSERT INTO telemetry VALUES (?, ?, ?, ?, ?, ?)", 
                  (anomaly_time + timedelta(seconds=2), trace_id, "API_Gateway", "/checkout", 5020.0, 502))
    
    conn.commit()
    print("Data generation complete. Saved to tracemind.db")

if __name__ == "__main__":
    db_conn = setup_database()
    generate_simulated_traffic(db_conn)
    db_conn.close()