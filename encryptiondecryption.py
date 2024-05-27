
# import required module
# Python program to find SHA256 hexadecimal hash string of a file
import hashlib

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import SHA256

import os
from zipfile import ZipFile
from zipfile import BadZipfile
from datetime import datetime
import base64
from pathlib import Path   
#from os.path import exists 

import time  
# remove non-empty folders
# https://www.freecodecamp.org/news/python-delete-file-how-to-remove-files-and-folders/
import shutil

# source https://www.geeksforgeeks.org/encrypt-and-decrypt-files-using-python/
# more salt etc https://thepythoncode.com/article/encrypt-decrypt-files-symmetric-python
# https://github.dev/nkarasiak/HistoricalMap

# for displaying decrypted content
from qgis.core import QgsVectorLayer, QgsProject
import zipfile

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtGui import QColor

class EncryptionDecryption:  

    filename1 = ""
    filename2 = ""
    filename3 = ""
    original_level = ""
    little_obfuscated_level = ""
    more_obfuscated_level = ""
    level1_zip_file = ""
    level2_zip_file = ""
    level3_zip_file = ""
    unzip_dir_level3 = ""
    unzip_dir_level2 = "" 
    unzip_directory = ""
    filepath_file_to_be_decrypted = ""
    decrypted_level_zipfilename = ""
    passphrase_file_save_location = ""
    hash_value = ""
    root_dir = ""
    final_encrypted_volume_filename = ""
    final_encrypted_volumes_hash_value = ''

    def __init__(self):
        self.key_file = 'filekey.key'
        self.filename1 = "" 
        self.filename2 = "" 
        self.filename3 = "" 
        #decrypt_to_level = 2  # 1 = innermost level, 2 = middle, and 3 is the outer level
        self.working_dir                     = '' 
        self.first_level_encrypted_file      = ''
        self.second_level_encrypted_file     = ''
        self.third_level_encrypted_file      = ''
        self.filepath_file_to_be_decrypted   = ""

        self.level1_zip_file = "level1_zip_file.zip"
        self.level2_zip_file = "level2_zip_file.zip"
        self.level3_zip_file = "level3_zip_file.zip"

        self.unzip_dir_level3 = ""
        self.unzip_dir_level2 = "" 

        self.passphrase_file_first_level  = "passphrase_first_level.txt"
        self.passphrase_file_second_level = "passphrase_second_level.txt"
        self.passphrase_file_third_level  = "passphrase_third_level.txt"

        self.hash_value = ""

        self.decrypted_layer_layerName = None # decrypted layer

    def compute_hash(self, filename, label_hash_val, label_hash_value, label_final_encrypted_volume_notarise):
        sha256_hash = hashlib.sha256()
        with open(filename,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            self.hash_value = sha256_hash.hexdigest()
            print('hash_value: ' + self.hash_value)
            # set tyhe filename
            #self.label_final_encrypted_volume_notarise.setStyleSheet("color: #AA336A") 
            # set hash values in both places: encrypted tab and notarisation tab
            label_final_encrypted_volume_notarise.setStyleSheet("color: #AA336A")  #dark pink
            label_hash_val.setStyleSheet("color: #AA336A") 
            label_hash_val.setText(str(self.hash_value)) 
            label_hash_value.setStyleSheet("color: #AA336A")
            label_hash_value.setText(str(self.hash_value)) 
        return self.hash_value
    
    def compute_hash_encrypted(self, filename, label_hash_val):
        sha256_hash = hashlib.sha256()
        with open(filename,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            self.hash_value = sha256_hash.hexdigest()
            print('hash_value: ' + self.hash_value)
            label_hash_val.setStyleSheet("color: #AA336A") 
            label_hash_val.setText(str(self.hash_value)) 
            # label_hash_value.setStyleSheet("color: #AA336A")
            # label_hash_value.setText(str(self.hash_value)) 
        return self.hash_value

    # parameters
    #current_level_resulting_file : encryptedfile_name = Path(user_chosen_filename_level3).name + ".enc"
    def encrypt_level(self, previous_level_encrypted_file, current_level_file, passphrase, 
                      level_zip_file, 
                      #label_hash_value, label_enc_vol, 
                      current_level_resulting_file, info_file):
                      #filename, level_zip_file, previous_level, 
                      #obfuscated_level_final_filename, 
                      #label_hash_value, label_enc_vol):
       
        print ('\t\tlevel_zip_file: ' + level_zip_file)
        print ('\t\tprevious_level_encrypted_file: ' + str(previous_level_encrypted_file))
        print ('\t\tcurrent_level_file: ' + current_level_file)
        print ('\t\tcurrent_level_resulting_file: ' + current_level_resulting_file)
        print ('\t\tinfo_file: ' + info_file)

        current_level_file_just_filename = ""

        if current_level_file is None or current_level_file == "":
            print('current_level_file is None: ')
            QMessageBox.information(None, "DEBUG:", 'Current level file is None.') 
            #return False # we dont proceed any further
        else:
            # get just the filename
            current_level_file_just_filename = Path(current_level_file).name 
        
        # for all other levels except when encrypting only level 1. As there is no previous levels to encrypt
        if (previous_level_encrypted_file is not None):
            print('previous_level_encrypted_file is not None: ' + previous_level_encrypted_file)
            previous_level_encrypted_file_just_filename = Path(previous_level_encrypted_file).name         

        # Create a zipfile of the two files # Create a ZipFile Object
        with ZipFile(level_zip_file, 'w') as zip_object: 
            # for all other levels except when encrypting only level 1. As there is no previous levels to encrypt
            if (previous_level_encrypted_file is not None):               
                zip_object.write(previous_level_encrypted_file, arcname = previous_level_encrypted_file_just_filename) # Adding files that need to be zipped
            zip_object.write(current_level_file, arcname = current_level_file_just_filename) # Adding files that need to be zipped
            zip_object.write(info_file, "info.txt") # Adding info file
            #zip_object.writestr('info.txt', '3')
        
        # Check to see if the zip file is created
        if os.path.exists(level_zip_file):
            print("\t\tZIP file created: " + level_zip_file)
        else:
            print("\t\tZIP file not created")        
               
        # Encrypt ZIP file here
        # level_zip_file = os.path.join(self.working_dir, self.level3_zip_file)          (= "level3_zip_file.zip")
        # current_level_resulting_file = Path(user_chosen_filename_level3).name + ".enc" (= "all_clusters_kamloops_masked.gpkg.enc")
        self.aes_encrypt(passphrase, level_zip_file, current_level_resulting_file)
                        
        #hash = self.compute_hash(self.current_level_resulting_file, label_hash_value) # hash
        
        # update the location of encrypted volume shown to user
        #label_enc_vol.setText("Encryted: " + str(self.current_level_file)) 

        # delete the zipfiles as they were temporary
        if os.path.exists(level_zip_file):
            os.remove(level_zip_file)
            print("\t\tTemporary zipfile " + level_zip_file  + " deleted")
        else:
            print("\t\tThe file " + level_zip_file  + "does not exist")        

    def decrypt_level(self, unzip_dir_level, decrypted_fullpath_filename, passphrase):    

        #self.compute_hash(encrypted_level) # hash
        print('unzip_dir_level ' + str(unzip_dir_level)) # level to decrypt

        # write to temporary directory

        # delete the zipfiles as they were temporary
        # if os.path.exists(level_zip_file):
        #     os.remove(level_zip_file)
        #     print("Temporary zipfile " + level_zip_file  + " deleted")
        # else:
        #     print("The file " + level_zip_file  + "does not exist")

    def listToString(self, s, length): 
        print('input string: ' + s)
        my_string = s.split()[:length] # first 4 words
        print(str(my_string))
        # initialize an empty string
        str1 = ""    
        # traverse in the string
        for ele in my_string:
            str1 = str1 + ' ' + ele
        # return string
        print('output string: ' + str1)
        return str1
    
    def check_level_filename(self, levels_to_encrypt, user_chosen_filename_level):
        #if levels_to_encrypt == 1: 
        if user_chosen_filename_level is None or user_chosen_filename_level == "":
            print("Level " + levels_to_encrypt + " filename is Null")
            QMessageBox.information(None, "DEBUG:", 'Level ' + levels_to_encrypt +' filename is Null. ')
            return False
        else:
            return True     #success

    def encryption(self, passphrase, levels_to_encrypt, 
                    user_chosen_filename_level1, user_chosen_filename_level2, user_chosen_filename_level3, 
                    label_passphrase_loc, label_hash_val, label_hash_value, label_enc_volume, label_final_encrypted_volume_notarise,
                    working_directory, label_encryption_time, safeguard_progressBar): 
        
        print('chosen_filename_level1: ' + str(user_chosen_filename_level1))
        print('passphrase passed: ' + str(passphrase))
        print('Working directory set: ' + working_directory)
        self.working_dir = working_directory
        print('self.working_di: ' + self.working_dir)
        
        # first check if these filenames are not null
        if levels_to_encrypt == 1: 
            if (self.check_level_filename(1, user_chosen_filename_level1) == False):
                return
        if levels_to_encrypt == 2: 
            if (self.check_level_filename(1, user_chosen_filename_level1) == False):
                return
            if (self.check_level_filename(2, user_chosen_filename_level2) == False):
                return
        if levels_to_encrypt == 3: 
            if (self.check_level_filename(1, user_chosen_filename_level1) == False):
                return
            if (self.check_level_filename(2, user_chosen_filename_level2) == False):
                return
            if (self.check_level_filename(3, user_chosen_filename_level3) == False):
                return

        current = time.time()
        print ('start: ' + str(current))
        
        if(levels_to_encrypt == 0):
            print("#### Levels to encrypt == 0")
            QMessageBox.information(None, "DEBUG:", 'Please Choose Files to encrypt. ')

        # begin by encrypting the first 'innermost' level
        if(levels_to_encrypt >= 1):       
            print("#### Encrypting Level 1 - Inner Level")       
            # writing the encrypted data to a file
            # full name of file  'all_clusters_kamloops.zip'
            file_name = os.path.basename(user_chosen_filename_level1)   
            print('file_name: ' + str(file_name))
            #just file filename 'all_clusters_kamloops'
            #filename_without_extension = Path(file_name).stem            
            #encryptedfile_name = Path(user_chosen_filename_level1).name + ".enc"
            #encryptedfile_name = os.path.join(self.working_dir, self.level2_zip_file + ".enc") # should instead be in the form 'level number zip file' 
            encryptedfile_name  = os.path.join(self.working_dir, file_name + ".enc")
            
            # add level to filename to signify how many levels are encrypted in one volume, without having to decrypt
            if levels_to_encrypt == 1:
                encryptedfile_name = encryptedfile_name.replace(".enc", ".enc1")  # add level '1' to encrypted volumé's filename 
            
            self.first_level_encrypted_file = os.path.join(self.working_dir, encryptedfile_name) # + '.' + filename_suffix)            
            #self.original_level_file = chosen_filename_level1
           
            # Add encryption information in the final encrypted volume - added at the most outer level each time.
            # this information is needed to notify users when they are trying to decrypt the third level, when only one level is encrypted
            # and to delete invalid decrypted files of third and second level when only the one (first) level has been encrypted
            # python still decrypts these files but they are invalid/corrupt
            info_file = 'info.txt'
            with open(info_file, 'w') as f:
                f.write(str(levels_to_encrypt))  # 3 level encryption

            print ('\tlevels_to_encrypt >=1 ')
            print ('\tself.first_level_encrypted_file '    + self.first_level_encrypted_file) # "D:\datasets\all_clusters_kamloops.zip.enc"
            print ('\tuser_chosen_filename_level1 '        + user_chosen_filename_level1)     # "D:/datasets/all_clusters_kamloops.zip"
            print ('\tself.level1_zip_file '               + self.level1_zip_file)            # "level1_zip_file.zip"
            print ('\tself.first_level_encrypted_file '    + self.first_level_encrypted_file) # "D:\datasets\all_clusters_kamloops.zip.enc"
            print ('\tencryptedfile_name '                 + encryptedfile_name)              # "D:\datasets\all_clusters_kamloops.zip.enc"

            #Creates a zip file, containing the files and then call the encrypt function
            self.encrypt_level(None,                               # previous encrypted level (from above operation)
                               user_chosen_filename_level1,        # user chosen current level
                               passphrase,                         # original passphrase
                               self.level1_zip_file,               # name of zip file at this level to be created  = ('.zip') filename already declared                            
                               #label_hash_value, label_enc_volume, # labels for updating
                               self.first_level_encrypted_file,    # name of final encrypted file for this level = '.enc' file
                               info_file)                          # txt 'info' file
            
            #### original code
            #self.aes_encrypt(passphrase, user_chosen_filename_level1,    # inputfile
            #                            encryptedfile_name)  #self.first_level_encrypted_file) # outputfile
            
            # update the location of encrypted volume shown to user
            label_enc_volume.setText(str(self.first_level_encrypted_file))            
            label_final_encrypted_volume_notarise.setText(str(encryptedfile_name))
            self.final_encrypted_volume_filename = self.first_level_encrypted_file
            self.save_passphrase(passphrase, self.passphrase_file_first_level, label_passphrase_loc) 

            
        # then encrypt the second 'middle' level if needed
        if(levels_to_encrypt >= 2): 
            print("#### Encrypting Level 2 - Middle Level")
            # the filename for this level's encrypted file
            #encryptedfile_name = Path(user_chosen_filename_level2).name + ".enc"            
            encryptedfile_name = Path(user_chosen_filename_level2).name + ".enc"   
            # add level to filename to signify how many levels are encrypted in one volume, without having to decrypt
            if levels_to_encrypt == 2:
                encryptedfile_name = encryptedfile_name.replace(".enc", ".enc2")  # add level '3' to encrypted volumé's filename          
            self.second_level_encrypted_file = os.path.join(self.working_dir, encryptedfile_name)
            self.level2_zip_file = os.path.join(self.working_dir, self.level2_zip_file) 
            print ('\tself.level2_zip_file ' + self.level2_zip_file)
            print ('\tlittle_obfuscated_level ' + self.second_level_encrypted_file)
            # substring from the main 15 term passphrase
            tenterm_passphrase = self.listToString(passphrase, 10)
            print ('\ttenterm_passphrase ' + tenterm_passphrase)

            # Add encryption information in the final encrypted volume - added at the most outer level each time.
            # this information is needed to notify users when they are trying to decrypt the third level, when only one level is encrypted
            # and to delete invalid decrypted files of third and second level when only the one (first) level has been encrypted
            # python still decrypts these files but they are invalid/corrupt
            info_file = 'info.txt'
            with open(info_file, 'w') as f:
                f.write(str(levels_to_encrypt))  # 3 level encryption

            print ('\tlevels_to_encrypt >=2 ')
            print ('\tself.first_level_encrypted_file '    + self.first_level_encrypted_file)
            print ('\tuser_chosen_filename_level2 '        + user_chosen_filename_level2)
            print ('\tself.level2_zip_file '               + self.level2_zip_file)
            print ('\tself.second_level_encrypted_file '   + self.second_level_encrypted_file)

            # Creates a zip file, containing the files and then call the encrypt function
            self.encrypt_level(self.first_level_encrypted_file,    # previous encrypted level (from above operation)
                               user_chosen_filename_level2,        # user chosen current level
                               tenterm_passphrase,                 # reduced passphrase
                               self.level2_zip_file,               # name of this level zip file to be created   = '.zip' file                            
                               #label_hash_value, label_enc_volume, # labels for updating
                               self.second_level_encrypted_file,   # name of final encrypted file for this level = '.enc' file
                               info_file)                          # info file
            
            # overwrite the final encrypted volume filename shown to user
            self.final_encrypted_volume_filename = self.second_level_encrypted_file
            # update the location of encrypted volume shown to user
            label_enc_volume.setText(str(self.second_level_encrypted_file))
            label_final_encrypted_volume_notarise.setText(str(encryptedfile_name))
            self.save_passphrase(tenterm_passphrase, self.passphrase_file_second_level, label_passphrase_loc)

            # delete the first level '.enc' file - Check if the file exists before attempting to delete it
            self.delete_previous_level_files(self.first_level_encrypted_file, self.level2_zip_file)

        if(levels_to_encrypt == 3): 
            print("#### Encrypting Level 3 - Outer Level")
            # the filename for this level's encrypted file            
            encryptedfile_name = Path(user_chosen_filename_level3).name + ".enc"
            # add level to filename to signify how many levels are encrypted in one volume, without having to decrypt
            if levels_to_encrypt == 3:
                encryptedfile_name = encryptedfile_name.replace(".enc", ".enc3")  # add level '3' to encrypted volumé's filename          
            self.third_level_encrypted_file = os.path.join(self.working_dir, encryptedfile_name)   
            self.level3_zip_file = os.path.join(self.working_dir, self.level3_zip_file)  
            print ('\tmore_obfuscated_level ' + self.third_level_encrypted_file)
            # substring from the main 15 term passphrase
            fiveterm_passphrase = self.listToString(passphrase, 5)

            info_file = 'info.txt'
            info_file_fullpath = os.path.join(self.working_dir, info_file) 
            with open(info_file_fullpath, 'w') as f:
                f.write(str(levels_to_encrypt))  # 3 level encryption
            
            print ('\tlevels_to_encrypt == 3 ')
            print ('\tself.second_level_encrypted_file '  + self.second_level_encrypted_file)
            print ('\tuser_chosen_filename_level3 '       + user_chosen_filename_level3)
            print ('\tself.level3_zip_file '              + self.level3_zip_file)
            print ('\tself.third_level_encrypted_file '   + self.third_level_encrypted_file)

            #self.aes_encrypt(tenterm_passphrase, filename2, self.original_level_file)
            self.encrypt_level(self.second_level_encrypted_file,   # previous encrypted level (from above operation)
                               user_chosen_filename_level3,        # user chosen current level
                               fiveterm_passphrase,                # reduced passphrase
                               self.level3_zip_file,               # name of this level zip file to be created                               
                               #label_hash_value, label_enc_volume, # labels for updating
                               self.third_level_encrypted_file,    # name of final encrypted file for this level            
                               info_file_fullpath)                          # info file
            
            # overwrite the final encrypted volume filename shown to user
            self.final_encrypted_volume_filename = self.third_level_encrypted_file
            # update the location of encrypted volume shown to user
            label_enc_volume.setText(str(self.third_level_encrypted_file))
            label_final_encrypted_volume_notarise.setText(str(encryptedfile_name))
            self.save_passphrase(fiveterm_passphrase, self.passphrase_file_third_level, label_passphrase_loc) 

            # delete the second level '.enc' file - Check if the file exists before attempting to delete it
            self.delete_previous_level_files(self.second_level_encrypted_file, self.level3_zip_file)
            
        end = time.time()
        print('end ' + str(end))
        diff = end - current

        print('Encryption Time taken ' + str(diff))
        #label_encryption_time.setStyleSheet("background-color: lightgreen") 
        label_encryption_time.setText( " Completed "+ str( round(diff, 2) )  + " seconds" )

        safeguard_progressBar.setValue(66) 

        # concetanate
        #self.save_passphrase() 
        #self.compute_hash(self.original_level) # hash 
        #self.save_passphrase(passphrase, self.passphrase_file_first_level, label_passphrase_loc) 
        #self.save_passphrase(tenterm_passphrase, self.passphrase_file_second_level, label_passphrase_loc)
        #self.save_passphrase(fiveterm_passphrase, self.passphrase_file_third_level, label_passphrase_loc) 
        self.final_encrypted_volumes_hash_value = self.compute_hash(self.final_encrypted_volume_filename, 
                                                                    label_hash_val, label_hash_value,
                                                                    label_final_encrypted_volume_notarise)    

    def delete_previous_level_files(self, previous_level_encrypted_file, level_zip_file):
        try:
            if os.path.exists(previous_level_encrypted_file):
                os.remove(previous_level_encrypted_file)
                os.remove(level_zip_file)
                print("The file 'previous_level_encrypted_file' has been deleted.")
            else:
                print("The file 'previous_level_encrypted_file' does not exist.")
        except OSError as e:
            print(f"Error delete_previous_level_files() - {e}")
            pass# hash 

        #self.create_pdf()

    def get_final_encrypted_volume_filename(self):
        file_name = Path(self.final_encrypted_volume_filename).name
        return file_name
    
    def get_final_encrypted_volumes_hash_value(self):
        return self.final_encrypted_volumes_hash_value
    
    def save_passphrase(self, passphrase, passphrase_file_save_file, label_passphrase_loc):
        try:
            passphrase_file_save_location = os.path.join(self.working_dir, passphrase_file_save_file)   
            with open(passphrase_file_save_location, 'w') as filekey:  # 'wb' - we dont want binary
                filekey.write(str(passphrase).strip())
            print('Passphrase saved in file : ' + passphrase_file_save_location)
            p = Path(passphrase_file_save_location)        
            #label_passphrase_loc.setText('Saved at ' + str(p.parent)) 
            label_passphrase_loc.setText(passphrase_file_save_location) # 'Saved in file : ' +
        except Exception as e:
            print(f"Error save_passphrase() - {e}")

    ######## Decryption
    # EXPLANATION
    # IN EVERY CASE GOES THROUGH EACH LEVEL DECRYPTION
    # If we have only the first level encrypted, it will be decrypted in the third if else
    # If we have two levels encrypted, it will be decrypted in the second and third if else
    # Only have to take care of zip file
            
    # CASES
    # All 3 levels are encrypted (needs 5 term passphrase), 
    # we try decrypt, if it does not exist, returns error and it should go to the next level to try and decrypt
    #     2 levels are encrypted (needs 10 term passphrase)
    #     1 level is encrypted   (needs 15 term passphrase)

    
    # VARIABLE DEFINITIONS
    # self.filepath_file_to_be_decrypted : the full filepath of file to be decrypted and is also used to refer to the decrypted file

    def decryption(self, encrypted_volume_filename, decrypt_to_level, passphrase, working_directory, label_decryption_time,
                   label_decrypted_volume, verification_progressBar, btnDecrypt, btn_dec_volume_location, tabWidget_3,
                   volume_encrypted_level, to_verify_display):
        
        # set a temporary working directory 'decrypted' for the decryption, using the global 'fixed' working dir
        # This seprate decrypted directory prevents ovewriting of original 'plaintext' files
        decryption_working_dir = os.path.join(working_directory, "decrypted")
        print('Decryption working_dir: ' + str(decryption_working_dir))
        # delete and recretae the working directory
        self.recreate_working_directory(decryption_working_dir)

        # set the working directory for the three levels, using the 'decrypted' working dir
        level3_decryption_working_dir = os.path.join(decryption_working_dir, "level3")
        print('level3_decryption_working_dir: ' + str(level3_decryption_working_dir))
        #set a temporary working directory for this level, using the global 'fixed' working dir
        level2_decryption_working_dir = os.path.join(decryption_working_dir, "level2")
        print('level2_decryption_working_dir: ' + str(level2_decryption_working_dir))
        level1_decryption_working_dir = os.path.join(decryption_working_dir, "level1")
        print('level1_decryption_working_dir: ' + str(level1_decryption_working_dir))

        print('self.working_dir: ' + self.working_dir)
        #print('passphrase passed: ' + passphrase)
        print('passphrase passed: ' + str(passphrase))
        print('decrypt_to_level ' + str(decrypt_to_level)) # level to decrypt
        print('encrypted_volume_filename ' + str(encrypted_volume_filename)) # D:/datasets/kx-site-of-significance-SHP.zip.enc ....file chosen by user to be decrypted
       
        current = time.time()
        print ('start ' + str(current))       

        # User chosen filename - loaded encrypted volume (from verification tab), and remove the ".enc" extension so that it can be used as the name of the decrypted zip file 
        #user_chosen_fullfile_to_decrypt = encrypted_volume_filename.replace(".enc", "")   # D:/datasets/kx-site-of-significance-SHP.zip
        #print("user_chosen_fullfile_to_decrypt " + str(user_chosen_fullfile_to_decrypt))  # kx-site-of-significance-SHP.zip
        user_chosen_file_to_decrypt = Path(encrypted_volume_filename).name.replace(".enc", "")   # kx-site-of-significance-SHP.zip
        print("user_chosen_file_to_decrypt " + str(user_chosen_file_to_decrypt))  # kx-site-of-significance-SHP.zip
        decrypted_fullpath_filename = None

        # Decrypting Level 3 - Outer Level
        # 'decrypt_to_level'        is what the user has chosen
        # 'volume_encrypted_level'  is what can be decrypted based on what has been encrypted

        # 'volume_encrypted_level == 3' to Consider if the number of encrypted levels is equals 2 or 1, we skip and go to next else if block    
        # we dont need to encryt a third level (that is not there), if only 2 levels were encrypted
        # if encrypted levels are 2 or 1, it shoudl skip this if statement

        # more explanation - one factor is to what level is the volume encrypted
        # the other is to what level the user wants to decrypt
        #
        # volume_encrypted_level    decrypt_to_level 
        # 1                         1
        # 2                         1 or 2
        # 3                         1, 2 or 3
        
        # The following line basically means that, if more that 3 levels have been encrypted 
        # and we want to decrypt to level 2 or 1, we exceute this code block

        if(decrypt_to_level <= 3 and volume_encrypted_level == 3): 
            
            print("#### Decrypting Level 3 - Outer Level")
            print("\tlevel3_decryption_working_dir b " + str(level3_decryption_working_dir))  
            #print("\tself.unzip_dir_level3 " + str(self.unzip_dir_level3))
            print("\tself.level3_zip_file " + str(self.level3_zip_file))
            #print("\tuser_chosen_file_to_decrypt " + str(user_chosen_file_to_decrypt))
            print("\tencrypted_volume_filename " + str(encrypted_volume_filename))

            # create the temporary working directory for this level 
            self.create_working_dir_for_this_level(level3_decryption_working_dir)

            print('self.decryption_working_dir: ' + str(level3_decryption_working_dir))
            decrypted_fullpath_filename = os.path.join(level3_decryption_working_dir, self.level3_zip_file) #user_chosen_file_to_decrypt)  #self.level3_zip_file) #
            print('decrypted_fullpath_filename: ' + str(decrypted_fullpath_filename))
            # decryption of this level only requires 5 terms of the full passphrase
            fiveterm_passphrase = self.listToString(passphrase, 5)            
            # call AES decryption, passing the encrypted volume filename, and where to store the decrypted file - which will be zipfile - since a zipped file was encrypted
            self.aes_decrypt(fiveterm_passphrase, encrypted_volume_filename, decrypted_fullpath_filename)
            self.level3_zip_file = decrypted_fullpath_filename # decrypted zip file
            display_map_dir = level3_decryption_working_dir
            # for next level decryption, try extracting the zip file
            # the zip file contains everything in the current level zipped (shapefile, info.txt, and inner level enc file)
            # and these need to be unzipped for the enc file to be decrypted in the next level
            print('self.extract_zip_file: ')
            self.extract_zip_file(level3_decryption_working_dir,  # D:\datasets\decrypted\level3
                                  #self.unzip_dir_level3,         # None
                                  self.level3_zip_file)           # level3_zip_file.zip

            # retrieve the zip file for display            
            self.filepath_file_to_be_decrypted = self.return_file_type_in_directory(level3_decryption_working_dir, ".zip")
            if self.filepath_file_to_be_decrypted is None:
                self.filepath_file_to_be_decrypted = self.return_file_type_in_directory(level3_decryption_working_dir, ".gpkg")
            print('self.filepath_file_to_be_decrypted: ' + str(self.filepath_file_to_be_decrypted))

        #  and complete == False

        # we skip this block if there was only one level encrypted, i.e. 'volume_encrypted_level' == 1  
        # we consider all ptehr cases, 'volume_encrypted_level' == 3 or 2, in case there were 3 or 2 levels of encryption 
        
        # one factor is to what level is the volume encrypted
        # the other is to what level the user wants to decrypt
        #
        # volume_encrypted_level    decrypt_to_level 
        # 1                         1
        # 2                         1 or 2
        # 3                         1, 2 or 3
        
        # The following line basically means that, if more that one level is encrypted (volume_encrypted_level = 2 or 3) 
        # and we want to decrypt to level 2 or 1, we exceute this code block        
        if(decrypt_to_level <= 2 and (volume_encrypted_level == 3 or volume_encrypted_level == 2) ):  
            print("\n#### Decrypting Level 2 - Middle Level ")    
            
            # create the temporary working directory for this level  
            self.create_working_dir_for_this_level(level2_decryption_working_dir)
            
            tenterm_passphrase = self.listToString(passphrase, 10)
            # get the name of any file with an '.enc' file extension in the directory
            enc_file_in_previous_directory = self.return_file_type_in_directory(level3_decryption_working_dir, ".enc")
            print('\tenc_file_in_previous_directoryXX : ' + str(enc_file_in_previous_directory))
            # If there is an '.enc' encrypted file to be decrypted in the level 1 directory (above), 
            # means multi-level encryption, and we need to decrypt using a ten term passphrase   
            if(enc_file_in_previous_directory is not None): 
                print('\tenc_file is not None, enc file ' + str(enc_file_in_previous_directory))
                
                # remove the ".enc" extension, leaving just the ".zip" file extension
                file_to_be_decrypted = enc_file_in_previous_directory.replace(".enc2", "")
                # using basename function from os  # module to print file name
                file_to_be_decrypted = os.path.basename(file_to_be_decrypted)
                print('\tfile_to_be_decrypted: ' + str(file_to_be_decrypted))
                self.filepath_file_to_be_decrypted = os.path.join(level2_decryption_working_dir, file_to_be_decrypted) 
                print('\tfilepath_file_to_be_decrypted: ' + str(self.filepath_file_to_be_decrypted))
                # decrypt    
                print("\ttenterm_passphrase: " + str(tenterm_passphrase)) 
                print("\tenc_file_in_previous_directory: " + str(enc_file_in_previous_directory)) 
                #self.filepath_file_to_be_decrypted = self.filepath_file_to_be_decrypted.replace(".enc","")  # remove the .enc file extension
                self.aes_decrypt(tenterm_passphrase, enc_file_in_previous_directory, self.filepath_file_to_be_decrypted) # file_to_be_decrypted #self.filepath_file_to_be_decrypted)
                #decrypted_fullpath_filename = os.path.join(level1_decryption_working_dir, user_chosen_file_to_decrypt) 
                display_map_dir = level2_decryption_working_dir

                print("\tlevel2_decryption_working_dir: " + str(level2_decryption_working_dir)) 
                print("\tself.level2_zip_file: " + str(self.level2_zip_file))
                
                # for level 1, it did not unzip with this line, but is needed for level 2
                # there should be a better way to resolve this issue, but use this for the timebeing
                if decrypt_to_level == 2 and '.zip' in file_to_be_decrypted:
                    file_to_be_decrypted = file_to_be_decrypted.replace(".enc", "")
                    #file_to_be_decrypted = file_to_be_decrypted.replace(".enc", "")                   
                # for next level decryption, try extracting the zip file
                self.extract_zip_file(level2_decryption_working_dir, #self.unzip_dir_level2, 
                                      file_to_be_decrypted) #self.level2_zip_file)  # file_to_be_decrypted


            # If there is no '.enc' encrypted file to be decrypted, it could mean only a 2 level encryption, 
            # Means there was two level (file) that needs to be decrypted, and it must be the user chosen file
            elif(enc_file_in_previous_directory is None): 
                print('\tenc_file_in_previous_directory is None ')                
                decrypt_to_file = encrypted_volume_filename.replace(".enc2", "")
                print('\tdecrypt_to_file ' + str(decrypt_to_file)) # output filename
                print('\tlevel2_decryption_working_dir ' + str(level2_decryption_working_dir)) # output filename
                print('\tself.level2_zip_file ' + str(self.level2_zip_file)) # output filename
                self.filepath_file_to_be_decrypted = os.path.join(level2_decryption_working_dir, self.level2_zip_file ) #user_chosen_file_to_decrypt) 
                print('\tfilepath_file_to_be_decrypted a ' + str(self.filepath_file_to_be_decrypted))
                
                print("\ttenterm_passphrase: " + str(tenterm_passphrase)) 
                self.aes_decrypt(tenterm_passphrase, 
                                encrypted_volume_filename, #decrypt_to_file, #user_chosen_file_to_decrypt,       #decrypt_to_file,          # input file
                                self.filepath_file_to_be_decrypted)     #self.filepath_file_to_be_decrypted)  # output file
                print("\tDecrypted")
                #decrypted_fullpath_filename = os.path.join(level2_decryption_working_dir, user_chosen_file_to_decrypt) 
                
                display_map_dir = level2_decryption_working_dir
                
                # for next level decryption, extra check, if there is a zip file there, try extracting the zip file 
                self.extract_zip_file(level2_decryption_working_dir, 
                                      #self.unzip_dir_level2, 
                                      self.level2_zip_file)
                # the original encrypted volume (chosen by user) will be used for the second level layername
                file_name = os.path.basename(decrypt_to_file) 
                self.filepath_file_to_be_decrypted = os.path.join(level2_decryption_working_dir, file_name) #user_chosen_file_to_decrypt) 
                print('\tfilepath_file_to_be_decrypted b ' + str(self.filepath_file_to_be_decrypted))

            else:
                print("Single or Double level decryption")
                
        # and complete == False
        if(decrypt_to_level == 1): 
            print("\n#### Decrypting Level 1 - Inner Level ")  
            # create the temporary working directory for this level  
            self.create_working_dir_for_this_level(level1_decryption_working_dir)
            enc_file_in_previous_directory = None
            decrypt_to_file = encrypted_volume_filename.replace(".enc1", "")
            # get the name of any file with an '.enc' file extension in the previous level decryption
            enc_file_in_previous_directory = self.return_file_type_in_directory(level2_decryption_working_dir, ".enc") #previous_level_dir)
            print('enc file ' + str(enc_file_in_previous_directory))   

            print('level1_decryption_working_dir ' + str(level1_decryption_working_dir))

            # If there is an '.enc' encrypted file to be decrypted in the level 2 directory (above), 
            # means multi-level encryption, and we need to decrypt using a five term passphrase             
            if(enc_file_in_previous_directory is not None):
                print('\nenc_file_in_previous_directory is not None : ' + str(enc_file_in_previous_directory))
                # remove the ".enc" extension, leaving just the ".zip" file extension
                file_to_decrypt_from_previous_level = enc_file_in_previous_directory.replace(".enc1", "")
                print('level1_decryption_working_dir ' + str(level1_decryption_working_dir))
                print('file_to_decrypt ' + str(file_to_decrypt_from_previous_level))
                filename = os.path.basename(file_to_decrypt_from_previous_level)
                self.filepath_file_to_be_decrypted = os.path.join(level1_decryption_working_dir, filename) 
                print('filepath_file_to_be_decrypted ' + str(self.filepath_file_to_be_decrypted))

                # decrypt    
                print("passphrase: " + str(passphrase)) 
                self.aes_decrypt(passphrase, enc_file_in_previous_directory, self.filepath_file_to_be_decrypted)
                # needed to output at the end
                decrypted_fullpath_filename = os.path.join(level1_decryption_working_dir, user_chosen_file_to_decrypt) 
                print("Decrypted: ") 
                print('\tdecrypted_fullpath_filename ' + str(decrypted_fullpath_filename))
                print('\tlevel1_decryption_working_dir ' + str(level1_decryption_working_dir))
                print('\tdisplay_map_dir ' + str(display_map_dir))
                print('\tself.filepath_file_to_be_decrypted ' + str(self.filepath_file_to_be_decrypted))
                #self.filepath_file_to_be_decrypted
                display_map_dir = level1_decryption_working_dir

                # for next level decryption, try extracting the zip file
                self.extract_zip_file(level1_decryption_working_dir, #self.unzip_dir_level2, 
                                      self.level1_zip_file)
                
            # If there is no '.enc' encrypted file to ve decrypted, meaning no multi-level encryption, 
            # Means there was only single level (file) that needs to be decrypted, and it must be the user chosen file
            elif(enc_file_in_previous_directory is None): 
                print('\nenc_file_in_previous_directory is None : ' + str(enc_file_in_previous_directory))
                # fifteen term_passphrase = self.listToString(passphrase, 15) 
                # if no enc file from previous level decryption is found, we check the (original) user chosen directory
                # from the user chosen file 'encrypted_volume_filename' remove the ".enc" extension, leaving just the filename
                file_to_decrypt = encrypted_volume_filename.replace(".enc1", "") # D:/datasets/all_clusters_kamloops.zip.enc
                print('file_to_decrypt ' + str(file_to_decrypt))                # D:/datasets/all_clusters_kamloops.zip
                # output filename
                self.filepath_file_to_be_decrypted = os.path.join(level1_decryption_working_dir, user_chosen_file_to_decrypt) 
                print('filepath_file_to_be_decrypted ' + str(self.filepath_file_to_be_decrypted)) # D:\datasets\decrypted\level1\all_clusters_kamloops.zip

                # decrypt   
                print("passphrase: " + str(passphrase)) 
                print("file_to_decrypt: " + str(file_to_decrypt)) 
                print("self.filepath_file_to_be_decrypted: " + str(self.filepath_file_to_be_decrypted)) 
                print("level1_decryption_working_dir: " + str(level1_decryption_working_dir)) 
                self.aes_decrypt(passphrase, 
                                encrypted_volume_filename, #file_to_decrypt, #user_chosen_file_to_decrypt,       #file_to_decrypt,          # input file
                                self.filepath_file_to_be_decrypted)     #self.filepath_file_to_be_decrypted)  # output file
                # needed to output at the end
                decrypted_fullpath_filename = os.path.join(level1_decryption_working_dir, user_chosen_file_to_decrypt) 
                display_map_dir = level1_decryption_working_dir
                print('decrypted_fullpath_filename ' + str(decrypted_fullpath_filename))
                print('display_map_dir ' + str(display_map_dir))

                # for next level decryption, extra check, if there is a zip file there, try extracting the zip file 
                self.extract_zip_file(level1_decryption_working_dir, 
                                      #self.unzip_dir_level2, 
                                      self.level1_zip_file)

            else:
                print("Neither multiple or single level decryption")

        end = time.time()
        print('end ' + str(end))
        diff = end - current

        verification_progressBar.setValue(66) 
        print('\tself.filepath_file_to_be_decrypted: ' + str(self.filepath_file_to_be_decrypted))

        # Verify if decryption succesfull and Display map
        verified = False

        # if we want to verify and automatically display the map just after decryption
        if to_verify_display:
            #layer_fullfilename - fullpath of layername,   e.g. c:\datasets\level1\all_clusters_kamloops.zip
            #path_to_extract    - for extracting zip files e.g. c:\datasets\level1\        
            verified = self.verify_decryption__display_level_map(self.filepath_file_to_be_decrypted, #decrypted_fullpath_filename,                      # full layername
                                display_map_dir, decrypt_to_level, level1_decryption_working_dir,
                                level2_decryption_working_dir,level3_decryption_working_dir) #level1_decryption_working_dir)  # path to extract
                

            if verified:
                print('Decryption Time taken ' + str(diff))
                #label_decryption_time.setStyleSheet("background-color: lightgreen") 
                #label_decryption_time.setStyleSheet("color: #AA336A") 
                btnDecrypt.setText("Decrypted") 
                label_decrypted_volume.show()
                btn_dec_volume_location.show()
                label_decryption_time.setText( " Completed "+ str( round(diff, 2) )  + " seconds" )   
                #label_decrypted_volume.setStyleSheet("background-color: lightgreen")
                label_decrypted_volume.setStyleSheet("color: #AA336A") 
                if (decrypted_fullpath_filename is not None):
                    label_decrypted_volume.setText( decrypted_fullpath_filename ) 
                else:
                    label_decrypted_volume.setText( self.filepath_file_to_be_decrypted )  

                # enable the next - display - tab
                tabWidget_3.setTabEnabled(2, True) #enable/disable the decryption tab
                verification_progressBar.setValue(66)  
            
                # delete temp files 
                #print('Delete_temp_files ')
                #self.delete_temp_files(decrypt_to_level, level3_decryption_working_dir, level2_decryption_working_dir,
                #                       level1_decryption_working_dir)

            else:
                print('Decrypted files Not verified ')

    def recreate_working_directory(self, decryption_working_dir):
        try:
            if os.path.exists(decryption_working_dir):                
                print("Directory '% s' already exists." % decryption_working_dir) 
                # delete if exists, to prevent the below code getting confused 
                shutil.rmtree(decryption_working_dir)  
            # create the directory in all cases
            os.mkdir(decryption_working_dir) 
            print("Directory '% s' created" % decryption_working_dir)         
        except Exception as e:
            print(f"Directory creation failed - {e}")

    def remove_enc_extension(directory):   
        try: 
            for filename in os.listdir(directory):
                # Check if the file has the '.enc' extension
                if filename.endswith('.enc'):
                    # Construct the new file name without the '.enc' extension
                    new_filename = filename[:-4]                
                    # Build the full paths for the old and new file names
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_filename)                
                    # Rename the file
                    os.rename(old_path, new_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
        except BadZipfile:
                print("\t\tUnzip did not work ")        
        except Exception as e:
            print(f"        An exception occurred while unzipping file - {e}")
            #QMessageBox.information(None, "DEBUG:", 'An exception occurred while unzipping file. ')


    # extract a zip file and delete it afterwards
    # parameters .. 
    # level_decryption_working_dir = directory
    # level_zip_file               = name of file
    def extract_zip_file(self, level_decryption_working_dir, level_zip_file):
        print('\tInSide function of self.extract_zip_file: ')
        print("\t\tlevel_decryption_working_dir: " + str(level_decryption_working_dir)) # directory to extract zip file
        #print("\tunzip_dir_level: " + str(unzip_dir_level)) 
        print("\t\tlevel_zip_file: " + str(level_zip_file)) 
        #print("\tself.filepath_file_to_be_decrypted: " + str(self.filepath_file_to_be_decrypted)) 
        # full path of zipfile to be extracted
        level_zipfile_fullpath_filename = os.path.join(level_decryption_working_dir, level_zip_file)
        #print("\t\tlevel_zipfile_fullpath_filename: " + str(level_zipfile_fullpath_filename)) 

        try:                        
            print('\t\tlevel_zipfile_fullpath_filename After : ' + str(level_zipfile_fullpath_filename))

            if os.path.isfile(level_zipfile_fullpath_filename):
                print('\t\tos.path.isfile(level_zipfile_fullpath_filename)')
                    # extract zipfile contents
                            # self.filepath_file_to_be_decrypted
                with ZipFile(level_zipfile_fullpath_filename, 'r') as zip_ref:
                    zip_ref.extractall(level_decryption_working_dir) # 'd:/datasets/decrypted/level3'    #self.unzip_dir_level2)
                        # Check to see if extracted zipfile contains and '.enc' file
                    if os.path.exists(level_decryption_working_dir): #unzip_dir_level2):
                        print("\t\tunzip_dir_level2 exists : " + level_decryption_working_dir)
                    else:
                        print("\t\tunzip_dir_level not created ")  
            
                # delete the zipfile after extrating it
                # As this creates two zipfiles, which confuses which zip file to extract when displaying map
                os.remove(level_zipfile_fullpath_filename)
                print("\t\tDELETED level_zipfile_fullpath_filename: " + str(level_zipfile_fullpath_filename)) 
            else:
                print("\t\tNOT TRUE: os.path.isFile(level_zipfile_fullpath_filename) " + str(level_zipfile_fullpath_filename))             
                

        except BadZipfile:
                print("\t\tUnzip did not work ")        
        except Exception as e:
            print(f"        An exception occurred while unzipping file - {e}")
            QMessageBox.information(None, "DEBUG:", 'An exception occurred while unzipping file. ') 

    def create_working_dir_for_this_level(self, level3_decryption_working_dir):
        try:                           
            self.unzip_dir_level3 = level3_decryption_working_dir
            if not os.path.exists(self.unzip_dir_level3):
                os.mkdir(self.unzip_dir_level3) 
                print("\t\tDirectory '% s' created" % self.unzip_dir_level3) 
        except Exception as e:
            print(f"        Directory creation failed - {e}")
            QMessageBox.information(None, "DEBUG:", 'Directory creation failed. ') 
    
    # if level 1, we delete levels 2 and 3
    # if level 2, we delete level 3
    # if level 3, we wont go as far as level 2 or 3
    def delete_temp_files(self, decrypt_to_level, level3_decryption_working_dir, level2_decryption_working_dir,
                          level1_decryption_working_dir):
        try:
            if(decrypt_to_level == 1): 
                shutil.rmtree(level2_decryption_working_dir)  #os.rmdir(level2_decryption_working_dir)
                shutil.rmtree(level3_decryption_working_dir)  #os.rmdir(level3_decryption_working_dir)
                # display map
                # self.display_level(level1_decryption_working_dir, "test.shp")
            elif(decrypt_to_level == 2): 
                shutil.rmtree(level1_decryption_working_dir) #os.rmdir(level3_decryption_working_dir)
                shutil.rmtree(level3_decryption_working_dir) #os.rmdir(level3_decryption_working_dir)
            # the following wont happen as after decrypting level 3, the flow does not proceed into the 2nd and 1st levels
            # but remains of a previous decryption can be deleted 
            elif(decrypt_to_level == 3): 
                shutil.rmtree(level1_decryption_working_dir) #os.rmdir(level3_decryption_working_dir)
                shutil.rmtree(level2_decryption_working_dir) #os.rmdir(level3_decryption_working_dir)
        
        except Exception as e:
            print(f"         Error delete_temp_files() - {e}")
            QMessageBox.information(None, "DEBUG:", 'Delete_temp_files folder doesn\'t exist. ') 

    def return_file_type_in_directory(self, directory, filetype):
        print('\tFunction: return_file_type_in_directory: ' + str(directory))
        
        try:
            if os.path.exists(directory):    
                for file in os.listdir(directory):
                    if file.endswith(filetype):
                        path = os.path.join(directory, file)
                        return path
            else:
                print('directory does not exist ' + str(directory))
        except Exception as e:
            print(f"Error save_passphrase() - {e}")

    # display shapefile or gpkg map from each level
    # level_fullfilename - fullpath of layername, e.g. c:\datasets\level1\all_clusters_kamloops.zip
    # path_to_extract  - for extracting zip files e.g. c:\datasets\level1\
    def verify_decryption__display_level_map(self,  level_fullfilename, path_to_extract, 
                                             decrypt_to_level, level1_decryption_working_dir,
                                             level2_decryption_working_dir,level3_decryption_working_dir):   
        
        print('Verify_decryption__display_level_map() Function : ' + str(path_to_extract)) 

        # we unload previpus decrypted layer, before uploading a new one 
        self.unload_previous_decrypted_layer()

        layername = None
        spatial_File = None
        verified = False 

        # there will be many formats, so we deal one by one
        print('\tlevel_fullfilename : ' + str(level_fullfilename))   # D:\datasets\decrypted\level1\all_clusters_kamloops.zip
        print('\tpath_to_extract : ' + str(path_to_extract))         # D:\datasets\decrypted\level1\
                        
        try:
            # THERE CAN BE TWO ZIPFILES
            # 1. The zipfile of the level
            # 2. The shapefile (but then there could be a any OS file instead as well)

            #Extract the level zip file 
            if(zipfile.is_zipfile(level_fullfilename)): # it returns True
                # opening Zip using 'with' keyword in read mode
                with zipfile.ZipFile(level_fullfilename, 'r') as file:
                    # printing all the information of archive file contents using 'printdir' method
                    print(file.printdir())
                    # extracting the files using 'extracall' method
                    print('\tExtracting all files in ...' + str(path_to_extract))
                    file.extractall(path_to_extract)
                    print('\tDone!') # check your directory of zip file to see the extracted files
                
                # for first level (if only one level has been encrypted), we have to delete the zip file 
                # of this level, as with a shapefile, there will be two zip files 
                #if decrypt_to_level == 1:
                if os.path.exists(level_fullfilename):
                    os.remove(level_fullfilename)
                    print("\tZipFile successfully deleted.")
                else:
                    print("\tZipFile does not exist.")

                # First try shapefile zip file. If its a zip file, we extract to 'working directory' and open the shp file
                # open the zipped (shapefile) file inside the level zip file
                print('\tExtracting zipped shapefile ')
                zip_File = None
                if os.path.exists(path_to_extract):
                    print('\tpath_to_extract: ' + str(path_to_extract))
                    zip_File = self.return_file_type_in_directory(path_to_extract, ".zip") #previous_level_dir)
                    print('\tzip_file: ' + str(zip_File))    

                    if zip_File is None:
                        print('\tNo zip file in directory: ' + str(path_to_extract))
                    # use the 'path_to_extract'
                    elif(zipfile.is_zipfile(zip_File)):
                        # opening Zip using 'with' keyword in read mode
                        with zipfile.ZipFile(zip_File, 'r') as file:
                            # printing all the information of archive file contents using 'printdir' method
                            print(file.printdir())
                            # extracting the files using 'extracall' method
                            print('\tExtracting all files in ...' + str(path_to_extract))
                            file.extractall(path_to_extract)
                            print('\tDone!')

                else:
                    print('\tPath does not exist: ' + str(path_to_extract)) 
                    #return

                # get the name of shp file
                print('\tlevel_fullfilename ' +str(level_fullfilename))
                dirname = os.path.dirname(level_fullfilename) 
                print('\tdirname ' + str(dirname))
                spatial_File = self.return_file_type_in_directory(dirname, ".shp") #previous_level_dir)
                print('\tspatial_File ' + str(spatial_File))

                # get the layername from full directory, using basename function from os 
                # module to print file name
                file_name = os.path.basename(level_fullfilename)           
                layername = file_name 
                # remove the '.enc' from filename, so that it can be used as the layername 
                layername = layername.replace('.enc', '')
                # should be doing this earlier in the code
                layername = layername.replace('.zip1', '.zip')
                print('\tfile_name: ' + str(file_name) + '\tlayername: ' + str(layername))

                #layername = file_name

            else:
                print('zipfile.is_zipfile: False')

            # use the 'info.txt' file as marker for sucessful decryption
            # Check sucessfull decryption by looking for the 'info.txt' file, which should exist at each if this levels.
            # level3_decryption_working_dir
            if(decrypt_to_level == 1):            
                path_to_file = os.path.join(level1_decryption_working_dir,"info.txt")       # path_to_decrypt
            elif(decrypt_to_level == 2):            
                path_to_file = os.path.join(level2_decryption_working_dir,"info.txt")       # path_to_decrypt
            elif(decrypt_to_level == 3):            
                path_to_file = os.path.join(level3_decryption_working_dir,"info.txt")       # path_to_decrypt
            print('path_to_file: ' + str(path_to_file))  

            # adding 2 seconds time delay
            #time.sleep(2)

            # If the info.txt file was extracted from the decrypted zip file, we ascertain that the decryption was sucessful
            if os.path.exists(path_to_file):
                print('Decryption was sucessfull') 
                verified = True               
            else:
                print('Decryption was unsucessfull')
                #QMessageBox.information( self, 'Warning', 'Decryption unsucessfull. You entered an incorrect passphrase.' )
                QMessageBox.information(None, "DEBUG:", 'Decryption unsucessfull. You entered an incorrect passphrase.') 
                #return   
                verified = False

            if verified == False:
                return False     # we dont proceed any further
            
            # Display map has to be after decryption and deletion
            print('Verify decryption completed sucessfully and Display map at level ')

            # Second, try geopagkage file 
            if(layername is None):
                print('\tAttempting to open geopackage file ' + str(spatial_File))
                # get the name of shp file
                dirname = os.path.dirname(level_fullfilename) 
                spatial_File = self.return_file_type_in_directory(dirname, ".gpkg") #previous_level_dir)
                print('\tspatial_File : ' + str(spatial_File))
                # get the layername from full directory, using basename function from os 
                # module to print file name
                file_name = os.path.basename(level_fullfilename)           
                print('\tfile_name: ' + str(file_name))
                layername = file_name

                # Load the QPKG layer
                layer = QgsVectorLayer(spatial_File, "QPKG Layer", "ogr")

            # if we found something
            # layername is the name whe show as the layer
            if(layername is not None):
                layer = QgsVectorLayer(spatial_File, layername, "ogr")
                
                if not layer.isValid():
                    print("\tLayer failed to load A!")
                    print("\tspatial_File: " + str(spatial_File))
                    print("\tlayername: " + str(layername))
                else:
                    print("\tLayer was loaded successfully A! ")
                    print("\tspatial_File: " + str(spatial_File))
                    print("\tlayername: " + str(layername))
                    print("\tlayer: " + str(layer))
                    print("\tLayer was loaded successfully!")

            # unload previous decrypted layer
            self.unload_previous_decrypted_layer()

            #root = QgsProject.instance().layerTreeRoot()

            QgsProject.instance().addMapLayer(layer)
            
            # add this to the variable, that is going to be use to unload layer
            self.decrypted_layer_layerName = layer

            # color the layer in a fixed way so that if all three layers are (decrypted) and displayed, they are distinct 
            if(decrypt_to_level == 1):            
                layer.renderer().symbol().setColor(QColor("#e15989"))      # path_to_decrypt
            elif(decrypt_to_level == 2):            
                layer.renderer().symbol().setColor(QColor("#8fff49"))      # path_to_decrypt
                #root.insertLayer(1, layer)
            elif(decrypt_to_level == 3):            
                layer.renderer().symbol().setColor(QColor("#f6e016"))       # path_to_decrypt
                #root.insertLayer(2, layer)
            
        except ValueError:
            print("Error: ValueError.")

        except Exception as e:
            print(f"Some error during Function verify_decryption__display_level_map() + {e}")
            QMessageBox.information(None, "DEBUG:", 'Exception during decryption. ') 

        return verified

    # unload any previous decrypted layer, 
    # since two layers showing different resolutions dont show together
    def unload_previous_decrypted_layer(self):
        # dict decrypted_layers
        for layer in QgsProject.instance().mapLayers().values():
            if layer.name() == self.decrypted_layer_layerName:
                QgsProject.instance().removeMapLayers( [layer.id()] )  
    #https://gis.stackexchange.com/questions/370808/remove-layers-only-if-layers-already-exist-using-pyqgis

    # Source https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
    # also https://debugpointer.com/python/create-sha256-hash-of-a-file-in-python
    def hash_computation(): 
        filename = input("Enter the input file name: ")
        with open(filename,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest();
            print(readable_hash)     

        # for large files
        filename = input("Enter the input file name: ")
        sha256_hash = hashlib.sha256()
        with open(filename,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            print(sha256_hash.hexdigest())  

        
    #def getKey(password):
	#    hasher = SHA256.new(password.encode('utf-8'))
	#    return hasher.digest()

    # https://github.com/anchal27sri/AES-file-encryption/blob/master/AES.py
    def aes_encrypt(self, key, inputFile, outputFile):
        
        try:
            # key      
            print('Encryption key: ' + key)  
            print('Encryption key str : ' + str(key))
            #key = 'password'
            print('inputFile: ' + str(inputFile))
            key = SHA256.new(key.encode('utf-8')).digest()	    
            chunksize = 64*1024
            filesize = str(os.path.getsize(inputFile)).zfill(16)
            IV = Random.new().read(16)
            print('outputFile: ' + str(outputFile))
            encryptor = AES.new(key, AES.MODE_CBC, IV)

            with open(inputFile, 'rb') as infile:           #rb means read in binary
                with open(outputFile, 'wb') as outfile:     #wb means write in the binary mode
                    outfile.write(filesize.encode('utf-8'))
                    outfile.write(IV)

                    while True:
                        chunk = infile.read(chunksize)
                        if len(chunk) == 0:
                            break
                        elif len(chunk)%16 != 0:
                            chunk += b' '*(16-(len(chunk)%16))
                        outfile.write(encryptor.encrypt(chunk))
        except ValueError:
            print("Error: ValueError.")

        except Exception as e:
            print(f"Exception during encryption + {e}")
            QMessageBox.information(None, "DEBUG:", 'Exception during encryption. ') 

    

    def aes_decrypt(self, key, inputFile, outputFile):
        try:
            # key      
            print('\t\tDecryption key: ' + key)   
            print('\t\tDecryption key str: ' + str(key))
            #key = 'password'
            print('\t\tinputFile: ' + str(inputFile) )
            print('\t\toutputFile: ' + str(outputFile))
            key = SHA256.new(key.encode('utf-8')).digest()	    
            chunksize = 64*1024
            

            with open(inputFile, 'rb') as infile:
                filesize = int(infile.read(16))
                IV = infile.read(16)
                decryptor= AES.new(key, AES.MODE_CBC, IV)

                with open(outputFile, 'wb') as outfile:
                    while True:
                        chunk = infile.read(chunksize)
                        if len(chunk) == 0:
                            break
                        outfile.write(decryptor.decrypt(chunk))
                    outfile.truncate(filesize)
        
        except ValueError:
            print("\t\tError: ValueError.")

        except Exception as e:
            print(f"Exception during decryption + {e}")
            QMessageBox.information(None, "DEBUG:", 'Exception during decryption. ') 