**MapSafe QGIS Geoprivacy plugin**
================

Our proposed MapSafe QGIS geoprivacy plugin furnishes a complete approach for safeguarding,
sharing, and verifying geospatial datsets from within the familiar QGIS
desktop application. Data owners can perform multiple geospatial data safeguarding
functions (geomasking or hexabinning, encryption, and notarization), along with verification
features, using their desktop application by themselves, eliminating reliance
on a third party for dataset protection. 

The plugins safeguarding and verification features are demonstrated in a 5-minute
YouTube video (https://www.youtube.com/watch?v=gq4wX3kMTfE). 
Please click on video image.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/gq4wX3kMTfE/0.jpg)](https://www.youtube.com/watch?v=gq4wX3kMTfE)

The help menu is online at https://sharmapn.github.io/MapSafeQGISGeoPrivPlugin/


**Getting started** 

Installing Python and the required libraries

1. Python can be installed using installer is at https://www.python.org/downloads/.
    The required Python libraries can be installed via pip. To use pip in a Windows environment, one needs to run the OSGeo4W.bat from the 'D:\QGIS' directory (not from 'D\OSGEO4W').

These commands need to be issued using the D:\QGIS\OSGEO.bat
```D:\QGIS>pip install cryptography
D:\QGIS>pip install web3
D:\QGIS>pip install python-dotenv
D:\QGIS>pip install xkcdpass
D:\QGIS>pip install easygui or python -m pip install easygui
D:\QGIS>pip install python-dotenv
D:\QGIS>(python -m) pip install pyqt-switch
```

2. Download the plugin zip file from the  https://github.com/sharmapn/MapSafe-QGIS-plugin
3. Install plugin in QGIS
4. There should be an .env file in the installed plugin directory.
    You should change the parameters (especially the Working Directory) in this file directly by editing it. 
    In my machine, it was C:\Users/Pankaj/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\mapsafe/.env
    Or you can change the values from the "Set ENV values" button from the plugin's top right.
    
Full details are at https://sharmapn.github.io/MapSafeQGISGeoPrivPlugin/gettingstarted.html

Plugin version 1.0 and above can only be used in QGIS version 3. 
