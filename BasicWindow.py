# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 15:23:07 2017

@author: aakash.chotrani
"""

import sys
from PyQt5.QtWidgets import QApplication,QWidget

app = QApplication(sys.argv)


window = QWidget()
window.setGeometry(50,50,500,300)
window.setWindowTitle("Course Recommender")

window.show()
sys.exit(app.exec_())
