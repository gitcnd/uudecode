# uudecode.py

__version__ = '1.0.20240726'  # Major.Minor.Patch

# Created by Chris Drake.
# uudecode for micropython  https://github.com/gitcnd/uudecode
# write <stdin> to the filename given in the uudecode "begin" header

import sys
import binascii

# UUencode and Base64 character sets
UUENCODE_CHARS = b'`!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_'
BASE64_CHARS = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# Create translation dictionary
translation_dict = {UUENCODE_CHARS[i]: BASE64_CHARS[i] for i in range(len(UUENCODE_CHARS))}

def uuencode_to_base64(uuencoded_bytes):
    """Translate UUencoded bytes to Base64 bytes using the translation dictionary."""
    return bytes(translation_dict.get(b, b) for b in uuencoded_bytes)

# Read the header line to get the filename
header_line = input("Paste/upload your uuencode data now, commending with \x1b[32;1mbegin ... filename\x1b[0m and ending with \x1b[32;1mend\x1b[0m\n").strip()
#header_line = sys.stdin.readline().strip()
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
            #line = sys.stdin.readline().strip()
            line = input()

            if line == "end":
                break

            if len(line) == 0 or line == "`":
                continue

            # Calculate expected length from the first character
            expected_length = ord(line[0]) - 32

            # Remove the length character from the line
            encoded_data = line[1:].encode()

            # Translate the line to Base64
            base64_data = uuencode_to_base64(encoded_data)

            # Decode the Base64 data
            decoded_data = binascii.a2b_base64(base64_data)

            # Validate the length of the decoded data
            if len(decoded_data) != expected_length:
                print(f"Warning: Length specified ({expected_length}) does not match the actual decoded length ({len(decoded_data)}).", file=sys.stderr)

            # Write the decoded data to the file
            try:
                #file.write(decoded_data)
                file.write(decoded_data[:expected_length])
            except Exception as e:
                print(f"Error writing to file: {e}", file=sys.stderr)
                break

    print(f"Data successfully decoded and written to {filename}")

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)

del sys.modules['uudecode']  # so another import will work again.

