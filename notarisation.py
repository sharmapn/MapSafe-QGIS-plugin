# 1. Add imports
from web3 import Web3
import json
import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
# import env variable class
from .envvariables import envvariables

class Notarisation:

    web3 = ''
    abi = ''

    # Notarisation details
    CONTRACT_ADDRESS   = ''
    BLOCKCHAIN_ADDRESS = ''
    PRIVATE_KEY        = ''
    NODE_URL           = '' 

    transaction_hash   = '' 

    def __init__(self, plugin_dir, envvar): 

        # https://ethereum.stackexchange.com/questions/46706/web3-py-how-to-use-abi-in-python-when-solc-doesnt-work
        filename = os.path.join(plugin_dir, 'abis/Location.json')
        with open(filename) as f:
            LocationNFT = json.load(f)
        self.abi = LocationNFT["abi"]               
        
        self.PRIVATE_KEY = envvar.get_private_key() 
        self.BLOCKCHAIN_ADDRESS = envvar.get_blockchain_address()
        self.CONTRACT_ADDRESS = envvar.get_contract_address()    
        self.NODE_URL = envvar.get_node_url()      
         # 2. Add the Web3 provider logic here: 
        self.web3 = Web3(Web3.HTTPProvider(node_url))  # Change to correct network   

        print('ENV Variables read from file ') 
        print('self.BLOCKCHAIN_ADDRESS: '   + str(self.BLOCKCHAIN_ADDRESS))
        print('self.CONTRACT_ADDRESS: '     + str(self.CONTRACT_ADDRESS))
        print('self.NODE_URL: '             + str(self.NODE_URL))
        print('self.PRIVATE_KEY: '          + str(self.PRIVATE_KEY))

        # have to make this check
        # note the init function is only called when notarisation is invoked from the notarisation tab
        self.check_env_variables()

    def check_env_variables(self):
        error = False

        try:
            if self.PRIVATE_KEY is None or self.PRIVATE_KEY == "":
                error = True
                print("PRIVATE_KEY not set in ENV file.")
                QMessageBox.information(None, "DEBUG:", 'PRIVATE_KEY not set in ENV file. ')
            if self.BLOCKCHAIN_ADDRESS is None or self.BLOCKCHAIN_ADDRESS == "":
                error = True
                print("BLOCKCHAIN_ADDRESS not set in ENV file.")
                QMessageBox.information(None, "DEBUG:", 'BLOCKCHAIN_ADDRESS not set in ENV file. ')
            if self.CONTRACT_ADDRESS is None or self.CONTRACT_ADDRESS == "":
                error = True
                print("CONTRACT_ADDRESS not set in ENV file.")
                QMessageBox.information(None, "DEBUG:", 'CONTRACT_ADDRESS not set in ENV file. ')
            if self.NODE_URL is None or self.NODE_URL == "":
                error = True
                print("NODE_URL not set in ENV file.")
                QMessageBox.information(None, "DEBUG:", 'NODE_URL not set in ENV file. ')
            
            return error
        except Exception as e:
            print(f'Exception checking environment variables. Please check + {e}')
            QMessageBox.information(None, "DEBUG:", 'Exception checking environment variables. ') 

        return error    

    def mint(self, string_to_mint):

        # return True if there was an error
        if self.check_env_variables() == True:            
            return
            # no need to show error as would have been shown from the called function 

        # 3. Create variables
        account_from = {
            'private_key': self.PRIVATE_KEY, 
            'address':     self.BLOCKCHAIN_ADDRESS, 
        }
        # contract address will always be this constant address
        contract_address = '0x8dD5Ca941A9F839062b6589A2E3f701458B011A9'

        print(f"Calling the mint() function in contract at address: { contract_address }")

        try:

            # Fill in your account here
            #balance = Web3.eth.getBalance(self.BLOCKCHAIN_ADDRESS)
            #print(Web3.fromWei(balance, "ether"))

            # 4. Create contract instance
            minter = self.web3.eth.contract(address=contract_address, abi=self.abi)
            # 5. Build reset tx
            mint_tx = minter.functions.mintNFT(string_to_mint).build_transaction(
                {
                    "from": Web3.to_checksum_address(account_from["address"]),
                    "nonce": self.web3.eth.get_transaction_count(
                        Web3.to_checksum_address(account_from["address"])
                    ),
                }
            )

            # 6. Sign tx with PK
            tx_create = self.web3.eth.account.sign_transaction(mint_tx, account_from["private_key"])
            # 7. Send tx and wait for receipt
            tx_hash = self.web3.eth.send_raw_transaction(tx_create.rawTransaction)
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)

            self.transaction_hash = tx_receipt.transactionHash.hex()

            print(f"Tx successful with hash: { tx_receipt.transactionHash.hex() }")            
            return True #success

        except Exception as e:
            print(f"Notarisation unsuccessful - {e}")
            QMessageBox.information(None, "DEBUG:", 'Notarisation unsucessfull 2. ') 

            return False # failure        

    def getTransaction(self):
        return self.transaction_hash
