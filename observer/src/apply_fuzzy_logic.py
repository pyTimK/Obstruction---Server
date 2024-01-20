def apply_fuzzy_logic(plate_number: str):
    """
    Apply fuzzy logic to plate number
    """

    if len(plate_number) == 8:
        plate_number = plate_number[:7]

    if len(plate_number) != 6 and len(plate_number) != 7:
        return plate_number
    

    str_part = plate_number[:3]
    num_part = plate_number[3:]

    str_part = str_part.replace("0", "O")
    str_part = str_part.replace("1", "I")
    str_part = str_part.replace("5", "S")
    str_part = str_part.replace("8", "B")
    str_part = str_part.replace("6", "G")

    num_part = num_part.replace("O", "0")
    num_part = num_part.replace("I", "1")
    num_part = num_part.replace("S", "5")
    num_part = num_part.replace("B", "8")
    num_part = num_part.replace("G", "6")

    return str_part + num_part
    
    