# -*- coding: utf-8 -*-
"""
encrypt_csv.py

To run: 
    $python encrypt_csv.py

Simply script to encrypt lfcgeo csv.
"""

import filecmp
import crypto_utils


CSV_FNAME_TO_ENCRYPT = 'data/dflfc_squad_players_geo_Sep2020.csv'
CSV_FNAME_DECRYPTED_TEST = 'data/dflfc_squad_players_geo_Sep2020.dec.csv'
# CSV_FNAME_TO_ENCRYPT = 'data/test.csv'
# CSV_FNAME_DECRYPTED_TEST = 'data/test.dec.csv'
KEY_FILE = 'key.key'

# generate key
print("generating key...")
fk = crypto_utils.generate_key()
print(f"\tkey is: {fk}")

# save key to file
print(f"save key to key file: '{KEY_FILE}...")
with open(KEY_FILE, "wb") as key_file:
    key_file.write(fk)

# encrypt file with key and save
print(f"encrypting file '{CSV_FNAME_TO_ENCRYPT}' with key...")
encrypted_fname = crypto_utils.encrypt_to_file(CSV_FNAME_TO_ENCRYPT, fk)
print(f"\ndone, saved encrypted file at: '{encrypted_fname}'")

# testing decrypt
print("testing decrypt...")
file_decrypted_bytes_data = crypto_utils.decrypt_to_bytes(encrypted_fname, fk)
print("done")
print(f"\tsave decrypted file to: '{CSV_FNAME_DECRYPTED_TEST}...")
with open(CSV_FNAME_DECRYPTED_TEST, "wb") as file:
    file.write(file_decrypted_bytes_data)

print("\tcomparing files...")
if filecmp.cmp(CSV_FNAME_TO_ENCRYPT, CSV_FNAME_DECRYPTED_TEST):
    print("\t\tfiles are same")
else:
    raise Exception("unexpected error: files are different")

# final reminder
print((
       '\nNote that the key must be saved to streamlit secrets'
       '(local and cloud) before running lfcgeo_app.py'))
