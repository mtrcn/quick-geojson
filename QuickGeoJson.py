"""
Date                 : 24/12/2022
Author               : Mete Ercan Pakdil
"""

from __future__ import print_function
from __future__ import absolute_import
from builtins import str
from builtins import object
# Import the PyQt and QGIS libraries
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from qgis.core import Qgis, QgsVectorLayer, QgsJsonUtils, QgsMessageLog, QgsProject

import os
import inspect

# Import the code for the dialog
from .QuickGeoJsonDialog import QuickGeoJsonDialog


class QuickGeoJson(object):

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        self.canvas = iface.mapCanvas()
        # TODO: remove: unused
        self.layerNum = 1
        self.typeMap = {
            1: 'Point',
            2: 'LineString',
            3: 'Polygon',
            4: 'MultiPoint',
            5: 'MultiLineString',
            6: 'MultiPolygon'
        }

    def initGui(self):
        current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        self.action = QAction(QIcon(os.path.join(current_directory, "quick_geojson.png")),
             "&QuickGeoJson", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.load)

        # Add toolbar button and menu item

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("QuickGeoJson", self.action)

        # create dialog
        self.dlg = QuickGeoJsonDialog()
        self.dlg.txtGeoJson.setPlainText("")
        self.dlg.txtLayerName.setText('QuickGeoJson')

        self.dlg.btnClear.clicked.connect(self.clearButtonClicked)


    def clearButtonClicked(self):
        self.dlg.txtGeoJson.setPlainText('')

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu("QuickGeoJson", self.action)
        self.iface.removeToolBarIcon(self.action)

     # run
    def load(self):
        # show the dialog
        self.dlg.show()
        self.dlg.adjustSize()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1 and self.dlg.txtGeoJson.toPlainText():
            txtGeoJson = str(self.dlg.txtGeoJson.toPlainText())
            layerName = self.dlg.txtLayerName.text() or 'QuickGeoJson'
            features = QgsJsonUtils.stringToFeatureList(txtGeoJson)
            layers = {}
            for feature in features:
                wkbType = feature.geometry().wkbType()
                if not wkbType in self.typeMap:
                    QgsMessageLog.logMessage("Geometry type (%d) is not recognized." % wkbType, 'QuickGeoJson', level=Qgis.Warning)
                    continue
                geomType = self.typeMap[wkbType]
                layer = None
                if not geomType in layers:
                    layer = self.createLayer(geomType, layerName + ' - ' + geomType)
                    layers[geomType] = layer
                    QgsMessageLog.logMessage("New layer created for the new geometry type (%s)" % geomType, 'QuickGeoJson', level=Qgis.Info)
                else:
                    layer = layers[geomType]
                self.saveFeature(layer, feature)
            QgsMessageLog.logMessage("Feature read: %d" % len(features), 'QuickGeoJson', level=Qgis.Info)

            # Refresh the map
            self.canvas.refresh()
            return

    def createLayer(self, geometryType, layerName):
        crs = self.canvas.mapSettings().destinationCrs()

        typeString = "%s?crs=%s" % (geometryType, crs.authid())

        layer = QgsVectorLayer(typeString.lower(), layerName, "memory")

        registry = QgsProject.instance()

        registry.addMapLayer(layer)
        return layer

    def saveFeature(self, layer, feature):
        layer.dataProvider().addFeatures([feature])
        layer.updateExtents()
        layer.reload()
        self.canvas.refresh()

    def constraintMessage(self, message):
        """return a shortened version of the message"""
        if len(message) > 128:
            message = message[:64] + ' [ .... ] ' + message[-64:]
        return message


if __name__ == "__main__":
    pass
