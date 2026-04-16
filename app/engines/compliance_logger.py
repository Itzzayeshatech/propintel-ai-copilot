import uuid
import json
import os
from datetime import datetime

def log_audit(input_data: dict, output_data: dict):
    """
    compliance_logger.py
    
    - Generate UNIQUE ID for every transaction
    - Store log in /data/audit_logs.json
    - Mark rbi_compliant = true
    """
    log_id = str(uuid.uuid4())
    log_entry = {
        "id": log_id,
        "timestamp": datetime.now().isoformat(),
        "input": input_data,
        "output": output_data,
        "rbi_compliant": True,
        "audit_trail_version": "1.0.0"
    }
    
    log_path = os.path.join("data", "audit_logs.json")
    
    # Ensure directory exists (should exist from mkdir)
    if not os.path.exists("data"):
        os.makedirs("data")
        
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r") as f:
                logs = json.load(f)
        except json.JSONDecodeError:
            logs = []
            
    logs.append(log_entry)
    
    with open(log_path, "w") as f:
        json.dump(logs, f, indent=2)
        
    return log_id
