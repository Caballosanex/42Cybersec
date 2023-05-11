# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/08 19:31:55 by alexsanc          #+#    #+#              #
#    Updated: 2023/05/11 15:50:56 by alexsanc         ###   ########.fr        #
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
    parser = argparse.ArgumentParser(
        description="A one-time password generator based on the RFC6238 standard.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-g", metavar="KEY_FILE",
                       help="generate a new secret key and save it to KEY_FILE")
    group.add_argument("-k", metavar="KEY_FILE",
                       help="generate a new one-time password using the secret key stored in KEY_FILE")
    args = parser.parse_args()

    if args.g:
        key = base64.b32encode(
            hmac.new(b"", digestmod=hashlib.sha1).digest()).decode()
        with open(args.g, 'w') as f:
            f.write(key)
            print(f"Secret key was successfully saved in {args.g}.")
    elif args.k:
        with open(args.k, 'r') as f:
            key_data = f.read().strip()
            if len(key_data) != 32:
                raise argparse.ArgumentTypeError(
                    "Invalid key length. The key must be 32 characters.")
            key = base64.b32decode(key_data.encode())
            otp = generate_otp(key)
            print(otp)
    else:
        raise argparse.ArgumentTypeError("Either -g or -k must be specified.")


def generate_otp(key):
    """Generates a new one-time password."""
    counter = int(time.time() / 30)
    print(counter)
    counter = struct.pack(">Q", counter)
    print(counter)
    hmac_digest = hmac.new(key, counter, hashlib.sha1).digest()
    print(hmac_digest)
    offset = hmac_digest[-1] & 0xf
    print(offset)
    truncated_hash = struct.unpack(">I", hmac_digest[offset:offset+4])
    print(truncated_hash)
    truncated_hash = truncated_hash[0] & 0x7fffffff
    print(truncated_hash)
    truncated_hash = truncated_hash % 1000000
    print(truncated_hash)
    return f"{truncated_hash:06d}"


def main():
    """Main function."""
    try:
        parse_args()
    except argparse.ArgumentTypeError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# USAGE:
# $ openssl rand -hex 32 > key.hex
# $ python3 ft_otp.py -g key.hex
# $ python3 ft_otp.py -k key.hex
