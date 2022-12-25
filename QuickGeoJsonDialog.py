"""
Date                 : 24/12/2022
Author               : Mete Ercan Pakdil
"""

from qgis.PyQt.QtWidgets import QDialog
from qgis.PyQt import uic
import os

class QuickGeoJsonDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        ui_path = os.path.join(os.path.dirname(__file__), 'QuickGeoJsonDialog.ui')
        uic.loadUi(ui_path, self)
