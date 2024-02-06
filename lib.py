# Python Library
import sys
import datetime
import time
import re
import locale
locale.setlocale(locale.LC_ALL, 'vi_VN')

from datetime import datetime

#Matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.ticker as ticker

# GUI Libaray
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QWidget, QStackedWidget, QLineEdit, QCompleter, QListView, QVBoxLayout, QWidget, QTableWidgetItem, QGridLayout, QSpinBox, QPushButton, QTextEdit, QSizePolicy, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QColor, QBrush
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QPoint, QRect, QDateTime, QTimer

# Send Email Libray
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Import UI file
import ui.ui_home as ui_home
import ui.ui_addData_window as ui_addData_window

# Import Database
import pyodbc
connection = pyodbc.connect('DRIVER = {ODBC Driver 18 for SQL Server}; SERVER=PAL; DATABASE=MarketingDA; DSN=InventorySaleManagement; Trusted_Connection=yes; encrypt=yes; TrustServerCertificate=yes')
db=connection.cursor()

import random

import pandas as pd