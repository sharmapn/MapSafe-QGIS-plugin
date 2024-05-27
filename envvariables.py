from qgis.PyQt.QtGui import *
from PyQt5.QtGui import *
from qgis.PyQt.QtWidgets import QAction, QApplication, QLabel, QComboBox, QFileDialog, QWidget

from PyQt5 import (uic, QtWidgets, QtCore)
from qgis.core import QgsVectorLayer, QgsGeometry, QgsFeature, QgsProject 

# from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QPushButton, QVBoxLayout
# from PyQt5.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction, QApplication, QLabel, QComboBox, QFileDialog

from qgis.PyQt.QtGui import *
from pathlib import Path
from qgis.utils import iface

#from .h3_grid_from_layer import HexTest
from qgis.utils import iface
from qgis.PyQt.QtCore import QVariant
# for progressbar
from PyQt5.QtWidgets import (QApplication, QDialog, QProgressBar, QPushButton)

from PyQt5.QtWidgets import QWidget, QFormLayout, QApplication, QLabel
from pyqt_switch import PyQtSwitch
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 

import os

# loading parameters from env file
from dotenv import load_dotenv
load_dotenv()
import dotenv
from os import environ

# open window to save env variables
#from mapsafe_dialog import MapSafeDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'envvariables.ui'))

###################################

class envvariables(QtWidgets.QDialog, FORM_CLASS):

  internal_envfile_loc = None

  web3 = ''
  abi = ''

  # Notarisation details
  CONTRACT_ADDRESS   = ''
  BLOCKCHAIN_ADDRESS = ''
  PRIVATE_KEY        = ''
  NODE_URL           = '' 
  WORKING_DIR        = '' 
  
  def __init__(self,  parent=None):
    super(envvariables, self).__init__(parent)
    self.setupUi(self)
    print('Set Variables')
    self.setWindowTitle("Set Variables")
    # self.pushButton.setText("Grettings")
    self.btc_save.clicked.connect(self.save_env_variables)

    # previous line
    #dotenv_path = Path('D:\\datasets\\.env')
    ##dotenv_path = Path(env_file_loc)
    # new line 
    self.plugin_dir = os.path.dirname(__file__)
    self.internal_envfile_loc = f'{self.plugin_dir}/.env'  
    print('self.internal_envfile_loc: ' + self.internal_envfile_loc)

    # the location of the env file is within the internal file
    # we simply read the location from the internal file and then pass that location to this function
    # f = open(self.internal_envfile_loc, "r") # In this example, we will be opening a file to read-only.
    # env_file_loc = f.readline()        
    # f.close()  # closing the file
    # print('env_file_loc: ' + env_file_loc)
    

    #print('PPPP dotenv_path: ' + str(dotenv_path))
    # previous line
    #load_dotenv(dotenv_path=dotenv_path)
    #load_dotenv()
    
    # self.PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    # self.BLOCKCHAIN_ADDRESS = os.getenv('BLOCKCHAIN_ADDRESS')
    # self.CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')    
    # self.NODE_URL = os.getenv('NODE_URL') 
    # self.WORKING_DIR = environ['WORKING_DIR']

    # print('ENV Variables read from file ') 
    # print('self.BLOCKCHAIN_ADDRESS: '   + str(self.BLOCKCHAIN_ADDRESS))
    # print('self.CONTRACT_ADDRESS: '     + str(self.CONTRACT_ADDRESS))
    # print('self.NODE_URL: '             + str(self.NODE_URL))
    # print('self.PRIVATE_KEY: '          + str(self.PRIVATE_KEY))
    # print('self.WORKING_DIR: '          + str(self.WORKING_DIR))

    # self.txt_blockchain_addr.setPlainText(str(self.BLOCKCHAIN_ADDRESS)) 
    # self.txt_contract_addr.setPlainText(str(self.CONTRACT_ADDRESS)) 
    # self.txt_node_url.setPlainText(str(self.NODE_URL)) 
    # self.txt_private_key.setPlainText(str(self.PRIVATE_KEY)) 
    # self.txt_working_dir.setPlainText(str(self.WORKING_DIR)) 

    self.read_env_variables()
    #load_dotenv(self.internal_envfile_loc) #"D:\\datasets\\.env")
    #dotenv_path = Path(env_file_loc)

    # have to check this
    # note the init function is only called when notarisation is invoked from the notarisation tab
    #self.check_env_variables()

  def read_env_variables(self):
      print('read_env_variables(): ')
      self.plugin_dir = os.path.dirname(__file__)
      self.internal_envfile_loc = f'{self.plugin_dir}/.env'  
      print('self.internal_envfile_loc: ' + self.internal_envfile_loc)
      
      #load_dotenv(self.internal_envfile_loc) 

      try:   
        # Check if the .env file exists
        if not os.path.isfile(self.internal_envfile_loc):
            raise FileNotFoundError(f"The file '{self.internal_envfile_loc}' does not exist.")

        # Read the contents of the .env file
        with open(self.internal_envfile_loc, 'r') as file:
            lines = file.readlines()
               
        for line in lines:
            if line.startswith('PRIVATE_KEY'):
                self.PRIVATE_KEY = line.replace('PRIVATE_KEY=','').replace('"','').strip()
                print('PRIVATE KEY FOUND = ' + self.PRIVATE_KEY)
            if line.startswith('BLOCKCHAIN_ADDRESS'):
                self.BLOCKCHAIN_ADDRESS = line.replace('BLOCKCHAIN_ADDRESS=','').replace('"','').strip()
                print('BLOCKCHAIN_ADDRESS FOUND = ' + self.BLOCKCHAIN_ADDRESS)
            if line.startswith('CONTRACT_ADDRESS'):
                self.CONTRACT_ADDRESS = line.replace('CONTRACT_ADDRESS=','').replace('"','').strip()
                print('CONTRACT_ADDRESS FOUND = ' + self.CONTRACT_ADDRESS)
            if line.startswith('NODE_URL'):
                self.NODE_URL = line.replace('NODE_URL=','').replace('"','').strip()
                print('NODE_URL FOUND = ' + self.NODE_URL)
            if line.startswith('WORKING_DIR'):
                self.WORKING_DIR = line.replace('WORKING_DIR=','').replace('"','').strip()
                print('WORKING_DIR FOUND = ' + self.WORKING_DIR)

            self.txt_blockchain_addr.setPlainText(str(self.BLOCKCHAIN_ADDRESS)) 
            self.txt_contract_addr.setPlainText(str(self.CONTRACT_ADDRESS)) 
            self.txt_node_url.setPlainText(str(self.NODE_URL)) 
            self.lineEdit_private_key.setText(str(self.PRIVATE_KEY)) 
            self.txt_working_dir.setPlainText(str(self.WORKING_DIR)) 

        file.close()
        print('END read_env_variables(): ')

      except Exception as e:
          print(f'Exception checking environment variables. Please check + {e}')
          #QMessageBox.information(None, "DEBUG:", 'Exception checking environment variables. ') 
           
    #   self.PRIVATE_KEY = os.getenv('PRIVATE_KEY')
    #   self.BLOCKCHAIN_ADDRESS = os.getenv('BLOCKCHAIN_ADDRESS')
    #   self.CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')    
    #   self.NODE_URL = os.getenv('NODE_URL') 
    #   self.WORKING_DIR = environ['WORKING_DIR']

  def save_env_variables(self):
      
      self.plugin_dir = os.path.dirname(__file__)
      self.internal_envfile_loc = f'{self.plugin_dir}/.env'  
      #print('self.internal_envfile_loc: ' + self.internal_envfile_loc)      
      #load_dotenv(self.internal_envfile_loc) 

      error = False

      self.BLOCKCHAIN_ADDRESS = self.txt_blockchain_addr.toPlainText() 
      self.CONTRACT_ADDRESS   = self.txt_contract_addr.toPlainText() 
      self.NODE_URL           = self.txt_node_url.toPlainText() 
      self.PRIVATE_KEY        = self.lineEdit_private_key.text() 
      self.WORKING_DIR        = self.txt_working_dir.toPlainText() 
      print('self.WORKING_DIR: ' + self.WORKING_DIR) 

      try:
          if self.PRIVATE_KEY is None or self.PRIVATE_KEY == "":
              error = True
              #print("PRIVATE_KEY not set in ENV file.")
              err_message = 'PRIVATE_KEY '
          if self.BLOCKCHAIN_ADDRESS is None or self.BLOCKCHAIN_ADDRESS == "":
              error = True
              #print("BLOCKCHAIN_ADDRESS not set in ENV file.")
              err_message = err_message + str('BLOCKCHAIN_ADDRESS ')
          if self.CONTRACT_ADDRESS is None or self.CONTRACT_ADDRESS == "":
              error = True
              #print("CONTRACT_ADDRESS not set in ENV file.")
              err_message = err_message + str('CONTRACT_ADDRESS ')
          if self.NODE_URL is None or self.NODE_URL == "":
              error = True
              #print("NODE_URL not set in ENV file.")
              err_message = err_message + str('NODE_URL ')

          # Write changes to .env file.
          if self.WORKING_DIR is None or self.WORKING_DIR == "":
              print("WORKING_DIR must be set.")
              QMessageBox.information(None, "DEBUG:", 'WORKING_DIR must be set. ')
          else:
            #   dotenv.set_key(self.internal_envfile_loc, 'WORKING_DIR', self.WORKING_DIR )
            #   dotenv.set_key(self.internal_envfile_loc, 'PRIVATE_KEY', self.PRIVATE_KEY )
            #   dotenv.set_key(self.internal_envfile_loc, 'BLOCKCHAIN_ADDRESS', self.BLOCKCHAIN_ADDRESS )
            #   dotenv.set_key(self.internal_envfile_loc, 'CONTRACT_ADDRESS', self.CONTRACT_ADDRESS )
            #   dotenv.set_key(self.internal_envfile_loc, 'NODE_URL', self.NODE_URL )
             
              # modify the env variables in the env file
              self.modify_env_value(self.internal_envfile_loc)
              
              # reload the env variables
              #load_dotenv(self.internal_envfile_loc) 
              # read variables into the textboxes in the dialog box              
              self.read_env_variables() 
              
              print("Environment variables saved.")
          
          if error:
              print(err_message)
              QMessageBox.information(None, "DEBUG:", err_message)

          #return error
      except Exception as e:
          print(f'Exception checking environment variables. Please check + {e}')
          QMessageBox.information(None, "DEBUG:", 'Exception checking environment variables. ') 

      return error    


  def modify_env_value(self, env_file): 
    try:   
        # Check if the .env file exists
        if not os.path.isfile(env_file):
            raise FileNotFoundError(f"The file '{env_file}' does not exist.")

        # Read the contents of the .env file
        with open(env_file, 'r') as file:
            lines = file.readlines()

        # Modify the value of the specified key
        modified_lines = []
        for line in lines:
            if line.startswith("PRIVATE_KEY"):
                modified_lines.append(f"PRIVATE_KEY={self.PRIVATE_KEY}\n")                
            if line.startswith("BLOCKCHAIN_ADDRESS"):
                modified_lines.append(f"BLOCKCHAIN_ADDRESS={self.BLOCKCHAIN_ADDRESS}\n")
            if line.startswith("CONTRACT_ADDRESS"):
                modified_lines.append(f"CONTRACT_ADDRESS={self.CONTRACT_ADDRESS}\n")
            if line.startswith("NODE_URL"):
                modified_lines.append(f"NODE_URL={self.NODE_URL}\n")
            if line.startswith("WORKING_DIR"):
                modified_lines.append(f"WORKING_DIR={self.WORKING_DIR}\n")
                #self.parent.label_working_dir.setPlainText(self.WORKING_DIR)
       
        # Write the modified lines back to the .env file
        with open(env_file, 'w') as file:
            file.writelines(modified_lines)

        #print(f"The value of '{key}' in '{env_file}' has been modified to '{new_value}'.")

        file.close()
    
    except Exception as e:
          print(f'Exception saving file with environment variables. Please check + {e}')
          #QMessageBox.information(None, "DEBUG:", 'Exception checking environment variables. ') 

  def get_working_dir(self):
    return self.WORKING_DIR

  def get_private_key(self):
    return self.PRIVATE_KEY
  
  def get_blockchain_address(self):
    return self.BLOCKCHAIN_ADDRESS
  
  def get_contract_address(self):
    return self.CONTRACT_ADDRESS

  def get_node_url(self):
    return self.NODE_URL

  def showPlot(self):
      #self.XX.load(QUrl(''))
      pass


  def greetings(self):
      print("Hello {}")


  