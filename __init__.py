"""
***************************************************************************
Name			 	 : QuickGeoJSON
Description          : Quick GeoJSON viewer
***************************************************************************

 This script initializes the plugin, making it known to QGIS.
"""


def classFactory(iface):
    # load GeoCoding class from file GeoCoding
    from .QuickGeoJson import QuickGeoJson
    return QuickGeoJson(iface)
