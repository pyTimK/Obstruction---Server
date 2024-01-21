import serial
import time

arduino_port = 'COM7'
ser = serial.Serial(arduino_port, 9600, timeout=1)
time.sleep(2)

#? Initialize variables
plate_number = "XXX 1111"
violation = "Unregistered"
email = "timkristianllanto.tk@gmail.com"

def send_command(ser, violation, plate_number, email):
    ser.write(("1-" + plate_number + '\n').encode())
    time.sleep(2)
    ser.write(("2-" + violation + '\n').encode())
    time.sleep(2)
    ser.write(("2-" + violation + '\n').encode())
    time.sleep(2)
    ser.write(("3-" + email + '\n').encode())

    

#? Send command to arduino
send_command(ser, violation, plate_number, email)


# # Read and print any response from the Arduino
# response = ser.readline().decode().strip()
# print(response)

# Close the serial connection
ser.close()