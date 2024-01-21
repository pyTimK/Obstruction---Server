
import serial
import time
from typing import List

def format_plate_number(plate_number: str):
    formatted = "1-" + plate_number + '\n'
    print(formatted)
    return (formatted).encode()

def format_violation(violation: str):
    formatted = "2-" + violation + '\n'
    print(formatted)
    return (formatted).encode()

def format_email(email: str, i: str):
    formatted = "3" + i + "-" + email + '\n'
    print(formatted)
    return (formatted).encode()

def format_phone(phone: str):
    formatted = "4-" + phone + '\n'
    print(formatted)
    return (formatted).encode()

def format_send_plate_number():
    formatted = "5-\n"
    print(formatted)
    return (formatted).encode()


def send_sms_email_to_arduino(violations: List[str], plate_number: str, email: str, phone: str):

    #? Open Serial Connection
    arduino_port = 'COM7'
    ser = serial.Serial(arduino_port, 9600, timeout=1)
    time.sleep(2)

    
    #? 1. PHONE
    ser.write(format_phone(phone))
    time.sleep(3)

    #? 1. PLATE NUMBER
    ser.write(format_plate_number(plate_number))
    time.sleep(3)
    ser.write(format_send_plate_number())
    time.sleep(3)

    #? 1. VIOLATIONS
    for violation in violations:
        ser.write(format_violation(violation))
        time.sleep(5)
    
    #? 1. EMAIL
    email1 = email
    email2 = ""
    if len(email1) > 20:
        email1 = email1[:20]
        email2 = email[20:]

    ser.write(format_plate_number(plate_number))
    time.sleep(3)

    ser.write(format_email(email1, "1"))
    time.sleep(5)
    ser.write(format_email(email2, "2"))
    
    while True:
        response = ser.readline().decode().strip()
        print(response)
        if response == "DONE":
            break
    time.sleep(5)

    print("---> SENT TO ARDUINO")
    #? Close the serial connection
    ser.close()
    
