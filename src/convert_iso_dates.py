import json
from datetime import datetime

def convert_iso_dates(obj):
    if isinstance(obj, list):
        return [convert_iso_dates(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_iso_dates(value) for key, value in obj.items()}
    elif isinstance(obj, str):
        try:
            return datetime.fromisoformat(obj)
        except ValueError:
            return obj
    else:
        return obj
    
    