# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'envvariables.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(408, 300)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.label_working_directory = QLabel(Dialog)
        self.label_working_directory.setObjectName(u"label_working_directory")
        self.label_working_directory.setGeometry(QRect(20, 20, 91, 16))
        self.txt_private_key = QTextEdit(Dialog)
        self.txt_private_key.setObjectName(u"txt_private_key")
        self.txt_private_key.setGeometry(QRect(120, 140, 271, 41))
        self.txt_working_dir = QTextEdit(Dialog)
        self.txt_working_dir.setObjectName(u"txt_working_dir")
        self.txt_working_dir.setGeometry(QRect(120, 20, 271, 25))
        self.label_peivate_key = QLabel(Dialog)
        self.label_peivate_key.setObjectName(u"label_peivate_key")
        self.label_peivate_key.setGeometry(QRect(20, 140, 91, 16))
        self.btc_save = QPushButton(Dialog)
        self.btc_save.setObjectName(u"btc_save")
        self.btc_save.setGeometry(QRect(30, 243, 75, 23))
        self.label_peivate_key_2 = QLabel(Dialog)
        self.label_peivate_key_2.setObjectName(u"label_peivate_key_2")
        self.label_peivate_key_2.setGeometry(QRect(20, 50, 91, 16))
        self.txt_blockchain_addr = QTextEdit(Dialog)
        self.txt_blockchain_addr.setObjectName(u"txt_blockchain_addr")
        self.txt_blockchain_addr.setGeometry(QRect(120, 50, 271, 25))
        self.label_peivate_key_3 = QLabel(Dialog)
        self.label_peivate_key_3.setObjectName(u"label_peivate_key_3")
        self.label_peivate_key_3.setGeometry(QRect(20, 80, 91, 16))
        self.txt_contract_addr = QTextEdit(Dialog)
        self.txt_contract_addr.setObjectName(u"txt_contract_addr")
        self.txt_contract_addr.setGeometry(QRect(120, 80, 271, 25))
        self.txt_node_url = QTextEdit(Dialog)
        self.txt_node_url.setObjectName(u"txt_node_url")
        self.txt_node_url.setGeometry(QRect(120, 110, 271, 25))
        self.label_peivate_key_4 = QLabel(Dialog)
        self.label_peivate_key_4.setObjectName(u"label_peivate_key_4")
        self.label_peivate_key_4.setGeometry(QRect(20, 110, 91, 16))

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_working_directory.setText(QCoreApplication.translate("Dialog", u"Working Directory", None))
        self.label_peivate_key.setText(QCoreApplication.translate("Dialog", u"Private Key", None))
        self.btc_save.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.label_peivate_key_2.setText(QCoreApplication.translate("Dialog", u"Blockchain Address", None))
        self.label_peivate_key_3.setText(QCoreApplication.translate("Dialog", u"Contract Address", None))
        self.label_peivate_key_4.setText(QCoreApplication.translate("Dialog", u"Node URL", None))
    # retranslateUi

