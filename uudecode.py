# uudecode.py

__version__ = '1.0.20240726'  # Major.Minor.Patch

# Created by Chris Drake.
# uudecode for micropython  https://github.com/gitcnd/uudecode
# write <stdin> to the filename given in the uudecode "begin" header

import sys

def uudecode_line(line):
    """Decode a single UUencoded line into binary data."""
    if len(line) < 2:
        return b''
    
    # The first character indicates the length of the decoded data
    length_char = line[0]
    length = ord(length_char) - 32
    
    # Decode the rest of the line
    encoded_data = line[1:]
    
    # Convert the encoded data to binary form
    binary_data = bytearray()
    buffer = 0
    buffer_len = 0
    
    for char in encoded_data:
        buffer = (buffer << 6) | (ord(char) - 32)
        buffer_len += 6
        
        while buffer_len >= 8:
            buffer_len -= 8
            binary_data.append((buffer >> buffer_len) & 0xFF)
    
    return binary_data[:length]

# Read the header line to get the filename
header_line = input().strip()
if not header_line.startswith('begin '):
    print("Invalid header line. Expected 'begin filename'.", file=sys.stderr)
    sys.exit(1)

# Extract the filename from the header line
filename = header_line.split(' ')[-1].strip()

try:
    # Open the file for writing in binary mode
    with open(filename, 'wb') as file:
        while True:
            # Read a line of UUencoded data
            line = input().strip()

            if line == "end" or line == "`":
                break

            if len(line) == 0:
                continue

            # Decode the line and write to the file
            decoded_data = uudecode_line(line)
            
            # Validate length of decoded data
            length = ord(line[0]) - 32
            if length != len(decoded_data):
                print(f"Warning: Length specified ({length}) does not match the actual decoded length ({len(decoded_data)}).", file=sys.stderr)

            # Write the required number of bytes to the file
            try:
                file.write(decoded_data)
            except Exception as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                break

    print(f"Data successfully decoded and written to {filename}")

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)

