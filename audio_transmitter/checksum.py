def calculate_checksum(data: bytes):
    checksum = 0
    for byte in data:
        checksum = checksum ^ byte
    
    return checksum