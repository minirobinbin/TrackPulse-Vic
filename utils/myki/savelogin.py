import csv
import os
from cryptography.fernet import Fernet
import base64

def savelogin(username, password, id):
    # Create the directory if it doesn't exist
    os.makedirs('logins', exist_ok=True)
    
    with open(f'utils/myki/logins/{id}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the inputs as a new row in the CSV
        writer.writerow([username, password])

def readlogin(id):
    with open(f'utils/myki/logins/{id}.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            return row
    
def create_key(user_key: str) -> bytes:
    # Ensure the user key is 32 bytes long by encoding and padding
    return base64.urlsafe_b64encode(user_key.ljust(32)[:32].encode())

def encryptPW(key, password):
    # Create a Fernet cipher object using the custom key
    cipher_suite = Fernet(create_key(key))

    # Encrypt the message
    encrypted_message = cipher_suite.encrypt(password.encode())

    return encrypted_message
    
def decryptPW(user_key: str, encrypted_message: bytes) -> str:
    cipher_suite = Fernet(create_key(user_key))
    decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
    return decrypted_message

# print(encryptPW('chode', 'hello'))

# print(decryptPW('chode', b'gAAAAABm-PDAxH2jQu7Hyjt694uIL-uCQmfBcahgRp1TpkSH9QyKfqNbk1VA3TcsyNvV-rWIMZRJQsWLF200B25txbo8kcq-Zw=='))