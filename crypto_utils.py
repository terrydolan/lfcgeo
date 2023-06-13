# -*- coding: utf-8 -*-
"""
crypto_utils.py: crypto helper functions

Help with encrypt and decrypt of files.
"""

from pathlib import Path
from cryptography.fernet import Fernet

    
def generate_key():
    """Returns a Fernet key."""
    key = Fernet.generate_key()
    # print(key)    
    return key

def encrypt_to_file(filename, key):
    """Encrypt file using key and save as file.
    
    Output file has .enc extension"""
    
    fk = Fernet(key)
    
    filename_path = Path(filename)
    filename_path_encrypted =  filename_path.with_suffix('.enc')
    # print(f"{filename_path=}, \n{filename_path_encrypted=}")
    
    with open(filename, "rb") as file_in:
        # read all file data
        file_data = file_in.read()
    
        # encrypt the data
        encrypted_data = fk.encrypt(file_data)
        
    # write the encrypted file
    with open(filename_path_encrypted, "wb") as file_out:
        file_out.write(encrypted_data)
        
    return filename_path_encrypted
            

def decrypt_to_bytes(filename, key):
    """Decrypt a file using key and return file bytes.""" 
    
    fk = Fernet(key)
    
    with open(filename, "rb") as file_in:
        # read the encrypted data
        file_encrypted_data = file_in.read()
        
    # decrypt data
    file_decrypted_bytes_data = fk.decrypt(file_encrypted_data)
    
    return file_decrypted_bytes_data

from cryptography.fernet import Fernet
# import streamlit as st


# with open('filekey.key', 'wb') as filekey:
#    filekey.write(key)
   
# with open('filekey.key', 'rb') as filekey:
#     fk = filekey.read()
#     print(fk)
    
# def write_key():
#     """
#     Generates a key and save it into a file
#     """
#     key = Fernet.generate_key()
#     print(key)
#     with open("key.key", "wb") as key_file:
#         key_file.write(key)
        
# def load_key():
#     """
#     Loads the key from the current directory named `key.key`
#     """
#     key = open("key.key", "rb").read()
    
#     return key
    
# if __name__ == "__main__":
#     # write_key()
#     # key = load_key()
#     # print(key)
#     # generate_key()
#     key = st.secrets["key"].encode()
#     print(key)
    
#     # file_encrypted = encrypt_to_file('data/tmp.csv', key)
    
#     # file_decrypted_bytes_data = decrypt_to_byes_data(file_encrypted, key)

#     SQUAD_PLAYERS_GEO_CSV_FILE = 'data/dflfc_squad_players_geo_Sep2020.csv'
#     # file_encrypted = encrypt_to_file(SQUAD_PLAYERS_GEO_CSV_FILE, key)
#     SQUAD_PLAYERS_GEO_CSV_FILE_ENC = 'data/dflfc_squad_players_geo_Sep2020.enc'
    
#     import pandas as pd
#     # from io import StringIO
#     from io import BytesIO
    
#     # df=pd.read_csv(data)
#     # df = pd.read_csv(StringIO(str(decrypt_to_data(SQUAD_PLAYERS_GEO_CSV_FILE_ENC, key), 'utf-8')))
#     df = pd.read_csv(BytesIO(decrypt_to_bytes(SQUAD_PLAYERS_GEO_CSV_FILE_ENC, key)))
#     print(df.head)
        
#     pass