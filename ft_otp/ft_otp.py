# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/08 19:31:55 by alexsanc          #+#    #+#              #
#    Updated: 2023/05/10 15:42:00 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import base64
import hashlib
import hmac
import struct
import sys
import time


def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="A one-time password generar based on the RFC6238 standard.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", metavar="KEY_FILE", help="generate a new secret key and save it to KEY_FILE")
    group.add_argument("-k", metavar="KEY_FILE", help="generate a new one-time password using the secret key stored in KEY_FILE")
    args = parser.parse_args()

    if args.g:
        key = args.g
        with open(key, 'r') as f:
            key_data = f.read().strip()
            if len(key_data) != 64:
                raise argparse.ArgumentTypeError("Invalid key length. The key must be 64 hexadecimal characters.")
        return args
    else:
        return args


def generate_key(filename):
    """Generates a new secret key and saves it to a file."""
    key = base64.b32encode(hmac.new(b"", digestmod=hashlib.sha1).digest()).decode()
    with open(filename, 'w') as f:
        f.write(key)
        print(f"Secret key was successfully saved in {filename}.")

def generate_otp(key):
    """Generates a new one-time password."""
    counter = int(time.time()) // 30
    hmac_digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = hmac_digest[-1] & 0xf
    truncated_hash = (struct.unpack(">I", hmac_digest[offset:offset+4])[0] & 0x7fffffff) % 1000000
    return f"{truncated_hash:06d}"


def main():
    """Main function."""
    try:
        args = parse_args()
        if args.g:
            generate_key(args.g)
        elif args.k:
            with open(args.k, 'rb') as f:
                key = f.read()
                otp = generate_otp(key)
                print(otp)
    except argparse.ArgumentTypeError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
