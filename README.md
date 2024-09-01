**MapSafe QGIS Geoprivacy plugin**
================

Our proposed MapSafe QGIS geoprivacy plugin furnishes a complete approach for safeguarding,
sharing, and verifying geospatial datsets from within the familiar QGIS
desktop application. Data owners can perform multiple geospatial data safeguarding
functions (geomasking or hexabinning, encryption, and notarization), along with verification
features, using their desktop application by themselves, eliminating reliance
on a third party for dataset protection. 

This plugin compliments the browser-based tool of the same name (https://mapsafe.xyz/) by accommodating masking and encryption of much larger datasets.

The plugin's homepage is at https://sharmapn.github.io/MapSafeQGISGeoPrivPlugin/ where details of the safeguarding and verification processes are described.

The plugins safeguarding and verification features are demonstrated in a 5-minute
YouTube video (https://www.youtube.com/watch?v=gq4wX3kMTfE). 
Please click on video image.

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/gq4wX3kMTfE/0.jpg)](https://www.youtube.com/watch?v=gq4wX3kMTfE)




**Getting started** 

With version 1.3, the python libraries should be installed when the plugin is installed. A command prompt will be invoked whoch will install the libraries.

Installing Python and the required libraries

1. Python can be installed using installer is at https://www.python.org/downloads/.
   **Please choose Python version 3.12.4** (https://www.python.org/downloads/release/python-3124/)
   Install dependencies: The following required Python libraries can be installed via pip. To use pip in a Windows environment, one needs to run the OSGeo4W.bat from the 'D:\QGIS' directory (not from 'D\OSGEO4W').
These commands need to be issued using the D:\QGIS\OSGEO.bat. Open OSGeo4W Shell installed with QGIS as Administrator and type:

```D:\QGIS>pip install cryptography
D:\QGIS>pip install web3
D:\QGIS>pip install python-dotenv
D:\QGIS>pip install xkcdpass
D:\QGIS>pip install easygui or python -m pip install easygui
D:\QGIS>(python -m) pip install pyqt-switch
```

2. Download the plugin zip file from the  https://github.com/sharmapn/MapSafe-QGIS-plugin
3. Install plugin in QGIS
4. The 'parameter.txt' file in the installed plugin directory contains the environment variables.
    You can change the values from the "Set ENV values" button from the plugin's top right.
    Or you can also change the values (especially the Working Directory) in this file directly by editing it. 
    In my machine, it was C:\Users/Pankaj/AppData/Roaming/QGIS/QGIS3\profiles\default/python/plugins\mapsafe/parameter.txt
    
Note: A sample dataset is in the 'datasets' directory.

Full details are at https://sharmapn.github.io/MapSafeQGISGeoPrivPlugin/gettingstarted.html

Plugin version 1.0 and above can only be used in QGIS version 3. 
