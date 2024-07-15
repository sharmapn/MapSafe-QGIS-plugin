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

# just for the env window 
from PyQt5 import QtCore as qtc

# open window to save env variables
#from mapsafe_dialog import MapSafeDialog

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'envvariables.ui'))

###################################

class envvariables(QtWidgets.QDialog, FORM_CLASS):
  
  # for the envariables window to get and show the 'working directory' in the main window
  submitClicked = qtc.pyqtSignal(str)  # <-- This is the sub window's signal

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
    self.btc_save.clicked.connect(self.save_env_variables)

    self.plugin_dir = os.path.dirname(__file__)
    self.internal_envfile_loc = f'{self.plugin_dir}/parameters.txt'  
    print('self.internal_envfile_loc: ' + self.internal_envfile_loc)

    self.read_env_variables()
       

  def read_env_variables(self):
      print('read_env_variables(): ')
      self.plugin_dir = os.path.dirname(__file__)
      self.internal_envfile_loc = f'{self.plugin_dir}/parameters.txt'  
      print('self.internal_envfile_loc: ' + self.internal_envfile_loc)
      
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
           
  def save_env_variables(self):
      
      self.plugin_dir = os.path.dirname(__file__)
      self.internal_envfile_loc = f'{self.plugin_dir}/parameters.txt'        
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
                         
              # modify the env variables in the env file
              self.modify_env_value(self.internal_envfile_loc)
              
              # read variables into the textboxes in the dialog box              
              self.read_env_variables() 
              
              print("Environment variables saved.")
          
              # emit
              # https://stackoverflow.com/questions/68453805/how-to-pass-values-from-one-window-to-another-pyqt
              self.submitClicked.emit( self.txt_working_dir.toPlainText())

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
  