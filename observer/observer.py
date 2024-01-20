import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
import requests
import json
from src.is_valid_plate_number import is_valid_plate_number
from src.apply_fuzzy_logic import apply_fuzzy_logic
from src.compute_violation import compute_obstruction
from src.compute_violation import compute_missing
from src.compute_violation import compute_coding
from src.constants import url_base, headers

def parse_filename(filename):
    # sample:  plate_numbers\2024_01_14_12_48_32__1__N6Y090X_plate1705207714342.jpg

    if filename[:14] != "plate_numbers\\":
        raise Exception("Invalid filename: " + filename + " (must start with 'plate_numbers\\')")
    
    filename = filename[14:] # remove "plate_numbers\"

    # split by underscore
    filename = filename.split("_")

    # parse datetime
    year = filename[0]
    month = filename[1]
    day = filename[2]
    hour = filename[3]
    minute = filename[4]
    second = filename[5]

    # construct datetime object
    date = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

    # parse plate number
    plate_number = filename[9]

    # fuzzy logic
    plate_number = apply_fuzzy_logic(plate_number)
    print(plate_number)
    

    if not is_valid_plate_number(plate_number):
        raise Exception("Invalid plate number: " + plate_number)

    reading = {
                "plate_number": plate_number,
                "date": date.isoformat(),
                "violations": [], #TODO: get violations
            }
    
    return reading



def on_created(event):
    try:
        print("------------------------------")
        print("Creating new reading entry...")
        violations = []

        #? Get Reading object
        reading = parse_filename(event.src_path)
        car_found = True
        print(f"Reading: {reading}")

        #? Get Car object
        response = requests.get(f"{url_base}/car/{reading['plate_number']}", headers=headers)
    
        if response.status_code != 200:
            car_found = False
            print("Car not found. Violations not computed")

        #? Compute violations
        if car_found:
            car = json.loads(response.json()["id"])
            violation_time = datetime.fromisoformat(reading["date"]) 
            print(f"Car: {car}")

            #? Compute obstruction
            obstruction = compute_obstruction(car, violation_time)
            if obstruction:
                violations.append("Obstruction")

            #? Compute missing
            missing = compute_missing(car, violation_time)
            if missing:
                violations.append("Missing")

            #? Compute coding
            coding = compute_coding(car, violation_time)
            if coding:
                violations.append("Coding")

            #? Save Car object
            response = requests.put(f"{url_base}/car/{car['_id']}", json=json.dumps(car), headers=headers)

            if len(violations) != 0:
                print("Violations: ", violations)
                #? Create Violation object if there are violations
                violation = {
                    "plate_number": car["_id"],
                    "model": car["model"],
                    "color": car["color"],
                    "violations": violations,
                    "date": datetime.now().isoformat(),
                }

                #? Save Violation object
                response = requests.post(f"{url_base}/violation", json=json.dumps(violation), headers=headers)
                print(response)

                if response.status_code != 200:
                    print("Error saving violation")
                    raise Exception("Error saving violation")

        #? Save Reading object
        reading["violations"] = violations
        print(reading)
        response = requests.post(f"{url_base}/reading", json=json.dumps(reading), headers=headers)

        if response.status_code != 200:
            print("Error saving reading")
            print(response.json())
            raise Exception("Error saving reading")
        
        print("Reading, Violation entries created!")
        print("------------------------------")
        
        
    except Exception as e:
        print(f"ERROR: {e}")




if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created


    path = "plate_numbers"
    go_recursively = False
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)


    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()