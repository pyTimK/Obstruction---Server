from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from src.MongoDBHelper import MongoDBHelper
from src.request_wrapper import request_wrapper

#! INITIALIZE ---------------------------------

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
socketio = SocketIO(app, debug=True, cors_allowed_origins="*")
socketio.init_app(app)

db = MongoDBHelper("localhost", 27017, "obstruction")

  

@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")

#! ---------------------------------------------


#TODO: Car CRUD -------------------------------------
#! Car Watch
@socketio.on("car_read_page")
def handle_car_read_page(page_number: int, page_size: int):
    data, is_last_page = db.car_read_page({}, page_number, page_size)
    emit("car_read_page", {'data': data, 'is_last_page': is_last_page})

#! Car Read
@app.route("/car/<car_id>", methods=["GET"])
@cross_origin()
def car_read(car_id: str):
    print('waaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    return request_wrapper(
        socketio, 
        "car_read",
        lambda _: db.car_read(car_id),
        with_body=False
    )

#! Car Add
@app.route("/car", methods=["POST"])
@cross_origin()
def car_create():
    return request_wrapper(
        socketio, 
        "car_edited", 
        db.car_create
    )


#! Car Update
@app.route("/car/<car_id>", methods=["PUT"])
@cross_origin()
def car_update(car_id: str):
    return request_wrapper(
        socketio, 
        "car_edited", 
        lambda data: db.car_update(car_id, data)
    )

#! Car Delete
@app.route("/car/<car_id>", methods=["DELETE"])
@cross_origin()
def car_delete(car_id: str):
    return request_wrapper(
        socketio, 
        "car_edited", 
        lambda _: db.car_delete(car_id),
        with_body=False
    )


#TODO: Violations CRUD -------------------------------------
#! Violations Watch
@socketio.on("violation_read_page")
def handle_violation_read_page(page_number: int, page_size: int):
    data, is_last_page = db.violation_read_page({}, page_number, page_size)
    emit("violation_read_page", {'data': data, 'is_last_page': is_last_page})


#! Violations Read
@app.route("/violation/<violation_id>", methods=["GET"])
@cross_origin()
def violation_read(violation_id: str):
    return request_wrapper(
        socketio, 
        "violation_read",
        lambda _: db.violation_read(violation_id),
        with_body=False
    )

#! Violations Add
@app.route("/violation", methods=["POST"])
@cross_origin()
def violation_create():
    return request_wrapper(
        socketio, 
        "violation_edited", 
        db.violation_create
    )


#! Violations Update
@app.route("/violation/<violation_id>", methods=["PUT"])
@cross_origin()
def violation_update(violation_id: str):
    return request_wrapper(
        socketio, 
        "violation_edited", 
        lambda data: db.violation_update(violation_id, data)
    )

#! Violations Delete
@app.route("/violation/<violation_id>", methods=["DELETE"])
@cross_origin()
def violation_delete(violation_id: str):
    return request_wrapper(
        socketio, 
        "violation_edited", 
        lambda _: db.violation_delete(violation_id),
        with_body=False
    )



#TODO: Readings CRUD -------------------------------------
#! Readings Watch
@socketio.on("reading_read_page")
def handle_reading_read_page(page_number: int, page_size: int):
    data, is_last_page = db.reading_read_page({}, page_number, page_size)
    emit("reading_read_page", {'data': data, 'is_last_page': is_last_page})


#! Readings Read
@app.route("/reading/<reading_id>", methods=["GET"])
@cross_origin()
def reading_read(reading_id: str):
    return request_wrapper(
        socketio, 
        "reading_read",
        lambda _: db.reading_read(reading_id),
        with_body=False
    )

#! Readings Add
@app.route("/reading", methods=["POST"])
@cross_origin()
def reading_create():
    return request_wrapper(
        socketio, 
        "reading_edited", 
        db.reading_create
    )


#! Readings Update
@app.route("/reading/<reading_id>", methods=["PUT"])
@cross_origin()
def reading_update(reading_id: str):
    return request_wrapper(
        socketio, 
        "reading_edited", 
        lambda data: db.reading_update(reading_id, data)
    )


#! Readings Delete
@app.route("/reading/<reading_id>", methods=["DELETE"])
@cross_origin()
def reading_delete(reading_id: str):
    return request_wrapper(
        socketio, 
        "reading_edited", 
        lambda _: db.reading_delete(reading_id),
        with_body=False
    )




#TODO: Coding CRUD -------------------------------------
#! Coding Watch
@socketio.on("coding_read_page")
def handle_coding_read_page(page_number: int, page_size: int):
    data, is_last_page = db.coding_read_page({}, page_number, page_size)
    emit("coding_read_page", {'data': data, 'is_last_page': is_last_page})

    
#! Coding Read
@app.route("/coding/<day>", methods=["GET"])
@cross_origin()
def coding_read(day: str):
    return request_wrapper(
        socketio, 
        "coding_read",
        lambda _: db.coding_read(day),
        with_body=False
    )

#! Coding Update
@app.route("/coding/<day>", methods=["PUT"])
@cross_origin()
def coding_update(day: str):
    return request_wrapper(
        socketio, 
        "coding_edited", 
        lambda data: db.coding_update(day, data)
    )



#! REAL TIME COMMUNICATION
def main():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)



#! ROUTES
@app.route("/try", methods=["POST"])
@cross_origin()
def check_if_performed():
    return {"error": "Not Found", "success": False}, 404
        


#! BEFORE REQUEST
@app.before_request
def before_request():
    print(f"---> REQUEST: {request.method} {request.url}")



#! MAIN
if __name__ == "__main__":
    main()
