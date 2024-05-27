MapSafe qgis geoprivacy plugin
================




Our proposed MapSafe QGIS geoprivacy plugin furnishes a complete approach for safeguarding,
sharing, and verifying geospatial datsets from within the familiar QGIS
desktop application. Data owners can perform multiple geospatial data safeguarding
functions (geomasking or hexabinning, encryption, and notarization), along with verification
features, using their desktop application by themselves, eliminating reliance
on a third party for dataset protection. These features are demonstrated in a 5-minute
YouTube video (https://www.youtube.com/watch?v=gq4wX3kMTfE) and on the online
help menu at https://sharmapn.github.io/MapSafeQGISGeoPrivPlugin/

Getting started 

Installing Python and the required libraries
Python can be installed on the machine. The The Windows installer is at https://www.python.org/downloads/windows/
The required Python libraries can be installed via pip. To use pip in a Windows environment, one needs to run the OSGeo4W.bat from the 'D:\QGIS' directory (not from 'D\OSGEO4W').
These commands need to be issued using the D:\QGIS\OSGEO.bat
```D:\QGIS>pip install cryptography
D:\QGIS>pip install web3
D:\QGIS>pip install python-dotenv
D:\QGIS>pip install xkcdpass
D:\QGIS>pip install easygui or python -m pip install easygui
D:\QGIS>pip install python-dotenv
D:\QGIS>(python -m) pip install pyqt-switch
'''


Full details are at https://sharmapn.github.io/MapSafeQGISGeoPrivPlugin/gettingstarted.html

Plugin version 1.0 and above can only be used in QGIS version 3. 
