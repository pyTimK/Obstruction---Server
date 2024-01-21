from datetime import datetime
import requests
from .constants import url_base, headers
import json

seconds_still_present = 60 * 2
seconds_for_violation = 60 * 5

def more_than_last_time(now: datetime, car):
    last_snapshot = datetime.fromisoformat(car['snapshots'][-1])
    difference = now - last_snapshot
    return difference.seconds > seconds_still_present

def more_than_violation_time(now: datetime, car):
    first_snapshot = datetime.fromisoformat(car['snapshots'][0])
    difference = now - first_snapshot
    return difference.seconds > seconds_for_violation


def compute_obstruction(car, violation_time: datetime):
    violation_time_iso = violation_time.isoformat()

    if not car['is_detected'] or more_than_last_time(violation_time, car):
        car['is_detected'] = True
        car['snapshots'] = [violation_time_iso]
        return False
    
    if more_than_violation_time(violation_time, car):
        car['is_detected'] = False
        car['snapshots'] = []
        return True
    
    car['snapshots'].append(violation_time_iso)
    return False


def compute_unregistered(car, violation_time: datetime) -> bool:
    return car['missing']

def compute_coding(car, violation_time: datetime) -> bool:
    #? Get day
    day = violation_time.strftime("%A").lower()

    #? Get Coding object
    response = requests.get(f"{url_base}/coding/{day}", headers=headers)
    
    if response.status_code != 200:
        print("ERROR: Coding day not found")
        return False

    coding = json.loads(response.json()["id"])

    #? Check if car is coding
    return car['_id'][-1] in coding['not_allowed']
    


    