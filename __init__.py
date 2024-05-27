# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MapSafe
                                 A QGIS plugin
 complete geoprivacy approach for safeguarding and verifying geospatial datasets
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2023-11-24
        copyright            : (C) 2023 by Pankajeshwara Sharma
        email                : pankajeshwara@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MapSafe class from file MapSafe.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .mapsafe import MapSafe
    return MapSafe(iface)