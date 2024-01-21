from flask_socketio import SocketIO
from typing import Callable
import json
from flask import request
from .convert_iso_dates import convert_iso_dates
from .convert_objectid_to_str import convert_objectid_to_str

def request_wrapper(socketio: SocketIO, to_emit: str, db_callback: Callable, with_body = True):
    result = None
    error = None

    try:
        data = None
        if with_body:
            print(f"---> REQUEST.JSON: {request.json}")
            data = json.loads(request.json)
            data = convert_iso_dates(data)

        result = db_callback(data)

        socketio.emit(to_emit, True)

    except Exception as e:
        print(f"----> ERROR: {e}")
        error = str(e)

    id = convert_objectid_to_str(result)
    success = result is not None and error is None and id is not None and id != 'null'
    status = 200 if success else 400
    

    result = {"success": success, 
            "id": id, 
            "status": status, 
            "error": error}
    
    print(f"----> RESULT: {result}")

    return result, status