import re

def is_valid_plate_number(plate_number):
    # Define the regular expression pattern
    plate_number_pattern = re.compile(r'^[a-zA-Z]{3}[\s-]*\d{3,4}$')
    print(f'isValidPlateNumber: {plate_number_pattern.match(plate_number) is not None}')
    # Test if the plate number matches the pattern
    return plate_number_pattern.match(plate_number) is not None