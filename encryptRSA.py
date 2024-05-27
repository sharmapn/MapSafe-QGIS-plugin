# Generating a key
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

import ctypes 

import base64
base64.encodestring = base64.encodebytes
base64.decodestring = base64.decodebytes

import os

# example adopted from: https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/

# https://nitratine.net/blog/post/asymmetric-encryption-and-decryption-in-python/
# the following may work or may not work..better to use symmetic ley encryption and protect the password with public ley
# as xplained here
# https://stackoverflow.com/questions/6309958/encrypting-a-file-with-rsa-in-python

# Public-key cryptography is usually used for small amounts of data only. It is slow, and can be hard to use right. 
# The usual practice is to use other methods to reduce the asymmetric problem to one where the security is provided by a shared key, 
# then use public-key cryptography to protect that shared key. For example:
# - To encrypt a file, randomly generate a secret key for a block or stream cipher (e.g. AES). Store the data encrypted with this cipher, and store the secret key encrypted with the public key alongside the encrypted payload.
# - To sign a file, compute a cryptographic digest (e.g. SHA-256). Sign the digest of the file with the private key and store that alongside the file.
# So here's a sketch of how encryption can look like (warning, untested code, typed directly in the browser):

# Encrypting and decrypting
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

class PublicKeyEncryption:

    # https://github.com/hmenn/RSA-helper-python/blob/master/RSA_Helper.py

    pub_keyFile     = "" 
    pri_keyFile     = "" 
    private_key     = ""
    public_key      = ""
    passphrase      = ""

    # for when to enable the encrypt and decrypt button - 
    # enable encrypt only when the passphrase file and public key is chosen
    # passphrase_file_chosen          = False
    public_key_chosen               = False
    # enable decrypt only when the passphrase file and public key is chosen    
    # encrypted_passphrase_file_chosen = False
    private_key_chosen               = False


    def __init__(self):
        # create the keys
        print("init")

    def generate_keys(self, working_dir, label_generated_key_pair, label_generated_keys):

        # set the locations
        self.pub_keyFile = os.path.join(working_dir, "public_key.pem")
        self.pri_keyFile = os.path.join(working_dir, "private_key.pem")

        self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )

        self.public_key = self.private_key.public_key()
        print('Public key' + str(self.public_key)) 

        # Storing the keys
        pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )           

        #write to keyFile
        with open(self.pri_keyFile, 'wb') as f:
            f.write(pem)
        print('Private Key written ' + str(self.pri_keyFile)) 
        
        pem = self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        
        # use same variable to write public key
        with open(self.pub_keyFile, 'wb') as f:
            f.write(pem)
        print('Public key written ' + str(self.public_key)) 
        # we just show in label, not message box
        #ctypes.windll.user32.MessageBoxW(0, "Key Pair Generated! See " + str(self.pub_keyFile), "Key Pair", 1)  
        
        # show the label
        label_generated_key_pair.show()
        label_generated_keys.setStyleSheet("color: #AA336A") 
        label_generated_keys.setText(str(self.pri_keyFile))

    # Reading the keys back in (for demonstration purposes)
    def readKeys(self):
        with open(self.pri_keyFile, "rb") as key_file:
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

        with open(self.pub_keyFile, "rb") as key_file:
                self.public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

    def show_public_key(self):
        print('self.public_key') 
        print(self.public_key) 

    def show_private_key(self):
        print('self.private_key')  
        print(self.private_key)    

    def read_PubKey(self, keyFile):        
        with open(keyFile, "rb") as key_file:  # self.pub_keyFile
                self.public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

        self.public_key_chosen = True
    
    def read_PriKey(self, keyFile):        
        with open(keyFile, "rb") as key_file:  # self.pri_keyFile
                self.private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

        self.private_key_chosen = True

    #Encrypting and Decrypting Files
    #To encrypt and decrypt files, you will need to use read and write binary when opening files. You can simply substitute the values I previously used for message with the contents of a file. For example:
    def encrypt(self, working_dir, file_addrress, label_encrypted_passphrase, label_encrypted_passphrase_file):
        
        # set the locations
        self.encrypted_file = os.path.join(working_dir, "passphrase.enc")

        f = open(file_addrress, 'rb')
        passphrase = f.read()
        f.close()

        # encrypt
        encrypted = self.public_key.encrypt(        
            passphrase,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
            )

        print ('encrypted ' + str(encrypted))

        f = open(self.encrypted_file, 'wb')
        f.write(encrypted)
        f.close()

        print('Passphrase encrypted ' + self.encrypted_file)
        label_encrypted_passphrase.show()
        label_encrypted_passphrase_file.setStyleSheet("color: #AA336A") 
        label_encrypted_passphrase_file.setText(self.encrypted_file)
        #self.label_enc_passphrase.setText(self.encrypted_file)

    def decrypt(self, working_dir, file_addrress, txt_passphrase, label_decrypted_passphrase, label_decrypted_passphrase_file):
      
         # set the locations
        self.decrypted_file = os.path.join(working_dir, "decrypted_passphrase.txt")

        f = open(file_addrress, 'rb')
        encrypted_passphrase = f.read()
        f.close()
        
        # decrypt
        original_message = self.private_key.decrypt(
                encrypted_passphrase,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

        # # Checking the results
        print(original_message)
        
        #output = data.decode()
        self.passphrase = original_message.decode()
        txt_passphrase.setText(self.passphrase)

        #encrypted = 'data from encryption'
        f = open(self.decrypted_file, 'wb')
        f.write(original_message)
        f.close()

        print('Passphrase decrypted ' + self.decrypted_file)
        label_decrypted_passphrase.show()
        label_decrypted_passphrase_file.setStyleSheet("color: #AA336A")
        label_decrypted_passphrase_file.setText(self.decrypted_file)

    def return_passphrase(self):
         return self.passphrase      