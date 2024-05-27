import os
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256

def encrypt(key, filename):
	chunksize = 64*1024
	outputFile = 'D:\\datasets\\all_clusters_kamloops.zip.enc1' #"(enc)"+filename
	filesize = str(os.path.getsize(filename)).zfill(16)
	IV = Random.new().read(16)

	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, 'rb') as infile:#rb means read in binary
		with open(outputFile, 'wb') as outfile:#wb means write in the binary mode
			outfile.write(filesize.encode('utf-8'))
			#outfile.write(IV)

			while True:
				chunk = infile.read(chunksize)

				if len(chunk) == 0:
					break
				elif len(chunk)%16 != 0:
					chunk += b' '*(16-(len(chunk)%16))

				outfile.write(encryptor.encrypt(chunk))

def decrypt(key, filename):
	chunksize = 64*1024
	outputFile = 'D:\\datasets\\decrypted\\decrypted.zip' #filename[11:]

	with open(filename, 'rb') as infile:
		filesize = int(infile.read(16))
		IV = infile.read(16)
		print( 'before: ' + str(key))
		decryptor= AES.new(key, AES.MODE_CBC, IV)
		print('after: ' + str(key))
		with open(outputFile, 'wb') as outfile:
			while True:
				chunk = infile.read(chunksize)
				print('chunksize: ' + str(chunksize))
				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(filesize)

def getKey(password):
	hasher = SHA256.new(password.encode('utf-8'))
	return hasher.digest()

def Main():
	choice = input("Would you like to (E)encrypt or (D)Decrypt ")

	if choice == 'E':
		filename = 'D:\\datasets\\all_clusters_kamloops.zip'   # input("File to encrypt: ")
		password = 'chariot kinetic impeding gerbil dislodge raking calculus femur commode quaking altitude dweller glider amber reselect' #input("Password: ")
		encrypt(getKey(password), filename)
		print('Done.')
	elif choice == 'D':
		filename =  'D:\\datasets\\all_clusters_kamloops.zip.enc1'   # input("File to decrypt: ")
		#  yummy handheld doorpost bogus graftinclsg transfer lanky pedicure citable hermit
		password =  'chariot kinetic impeding gerbil dislodge raking calculus femur commode quaking altitude dweller glider amber reselect'  # input("Password: ")
		decrypt(getKey(password),filename)
		print("Done.")

	else:
		print("No option selected, closing...")


Main()