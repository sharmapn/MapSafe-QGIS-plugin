#from .h3_grid_from_layer import HexTest
import os
from qgis.utils import iface
from qgis.core import (
    QgsCoordinateReferenceSystem,
    QgsCoordinateTransform,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsGeometry,
    QgsPointXY,
    QgsProject,
    QgsProcessingFeedback,
    QgsSymbol,
    QgsSymbolLayer,
    QgsRendererCategory,
    QgsSimpleFillSymbolLayer,
    QgsCategorizedSymbolRenderer,
    QgsGraduatedSymbolRenderer,
    QgsStyle,
    QgsMessageLog,
    QgsVectorFileWriter,
    QgsVectorLayer,
    QgsWkbTypes,
)
from qgis.PyQt.QtCore import QVariant

from qgis.utils import Qgis

# qmessage
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox

import processing
import h3

#import processing
from processing.core.Processing import Processing

# binning example
# provide file name index and field's unique values
from random import randrange

# START BINNING
class H3Binning:

    debug = ''
    min_resolution = 0
    max_resolution = 9
    out_filename_prefix = ''
    projectPath = ''
    geo_csrs = ''
    out_csrs = ''
    mylayer = ''
    geographic_coordsys =''
    output_projection = ''
    dataPath = ''

    working_directory = ''  # working dir used throughout the plugin
    data_dir  = ''          # data directory to store hex files within the working directory
    original_layer = ''     # the main layer from which hexagons are generated from
    hexabinning_folder = '' # the folder in which to store the hexabinned datasets 
    
    def __init__(self):
        self.data_dir = ''
        # https://gis.stackexchange.com/questions/152762/error-algorithm-not-found-qgis
        Processing.initialize()
        #Processing.updateAlgsList()

    # set the parameters to be used in the next 'binning' function
    def set_parameters(self, data_dir, working_directory, original_layer):
        self.data_dir  = data_dir
        self.working_directory = working_directory
        self.original_layer = original_layer


    # https://github.com/maphew/mhwcode/blob/1ef8338e20ff24ddbe741af225e556b9d81ec416/gis/qgis/h3-grid-from-layer.py    
    def binning_function(self, binning_resolution, layerName, safeguard_progressBar, two_binning_levels):             
        print('binning function')

        self.debug = False

        ###---------- Edit these variables ----------
        # Min & max h3 resolution levels, from 0 to 15 (global to sub-meter)
        # High resolutions over broad areas can be slow and consume a lot of storage space
        # https://h3geo.org/docs/core-library/restable
        # Resolution 7 is ~2,000m across, 9 is ~320m across, 11 is ~45m (in YT Albers)
        #self.min_resolution = 0
        #self.max_resolution = 9

        # Output files are {prefix}_{resolution}: Hex_3, Hex_4, ...
        # too many files are created so we have to crateb a sub folder to house these
        self.hexabinning_folder = "hexabinned_datasets/"        # 'hexabinned_datasets'
        self.out_filename_prefix = layerName + "_Hex"               # oil_drills_north_coromandel — layers/POINT.shp_Hex_6.shp

        # D:\datasets\hexabinned_datasets/oil_drills_north_coromandel — layers/POINT.shp_Hex_6.shp
        # D:\datasets\hexabinned_datasets/oil_drills_north_coromandel — layers/POINT.shp_Hex_6._count.shp

        self.geographic_coordsys = "EPSG:4617"  # e.g. WGS84, NAD83(CSRS)
        self.output_projection   = "EPSG:3579"  # placeholder, not currently used
        # --------------------------------------------

        #projectPath = os.path.dirname(QgsProject.instance().fileName())
        self.geo_csrs = QgsCoordinateReferenceSystem(self.geographic_coordsys)
        self.out_csrs = QgsCoordinateReferenceSystem(self.output_projection)
                                # projectPath
        self.dataPath = os.path.join(self.working_directory, self.hexabinning_folder) 
        print('output ' + str(self.dataPath))  # D:\datasets\hexabinned_datasets
        
        try:
            if not os.path.exists(self.dataPath):
                os.mkdir(self.dataPath)
                print('Directory created: ' + str(self.dataPath))
            #instead of chooser, just use active layer, and selected features within that layer
            self.mylayer = iface.activeLayer()
            print('self.mylayer: ' + str(self.mylayer))

            if(self.mylayer is None):
                QMessageBox.information(None, "DEBUG:", 'Please select a layer. ') 
                return   
        
            if self.mylayer.selectedFeatures():
                params = {'INPUT':self.mylayer, 'OUTPUT':'memory:sel'}
                self.mylayer = processing.run("qgis:saveselectedfeatures", params)["OUTPUT"]
                if self.debug:
                    QgsProject.instance().addMapLayer(self.mylayer)
        except Exception as e:
            print(f'Error selecting features. Please select a layer for hexabinning + {e}')    
        
        print('Before calling run function')
        
        # user selected binning resolution
        self.run(binning_resolution, two_binning_levels)
        print('After calling run function')

        # classify the two layers
        #for res in range(binning_resolution, binning_resolution + 2):
        #    self.classify(layerName, res)

        if two_binning_levels is True:
            self.classify(layerName, binning_resolution)
            self.classify(layerName, binning_resolution + 1)

        else:
            self.classify(layerName, binning_resolution)

        safeguard_progressBar.setValue(33) 

    # 8th April 2024
    # automating all the sybology steps
    # https://gis.stackexchange.com/questions/478718/qgis-use-python-script-to-show-hexabinning-results-instead-of-manually-using-sym
    def classify(self, layerName, res):
        print('Classify Function')

        hexabined_layer = str(self.out_filename_prefix) + str(res) # + str(".shp")
        print('hexabined_layer: ' + hexabined_layer)

        #layer = QgsProject.instance().utils.iface.activeLayer() # when run from within QGIS Python console        
        # working but needs exact filename
        #layer = QgsProject.instance().mapLayersByName("all_clusters_kamloops_Hex7")[0] 
        layer = QgsProject.instance().mapLayersByName(hexabined_layer)[0] 
        print(' layer ' + str(layer))

        color_ramp = QgsStyle().defaultStyle().colorRamp('Blues')
        v_symbol = QgsSymbol.defaultSymbol(layer.geometryType()) #QgsSymbol.defaultSymbol(Qgis.Polygon)

        renderer = QgsGraduatedSymbolRenderer.createRenderer(
            vlayer=layer,
            attrName= 'numpoints',     #layer.fields().names()[-1],
            classes=5,
            mode=QgsGraduatedSymbolRenderer.Quantile,
            symbol = v_symbol, # symbol=QgsSymbol.defaultSymbol(layer.geometryType()),
            ramp=color_ramp
        )
        layer.setRenderer(renderer)
        layer.triggerRepaint()

    def log(self, item):
        return QgsMessageLog.logMessage(str(item))


    def proj_to_geo(self, in_layer):
        """Project to geographic coordinate system, in memory.
        H3 needs all coordinates in decimal degrees"""
        params = {
            "INPUT": self.mylayer,
            "TARGET_CRS": self.geographic_coordsys,
            "OUTPUT": "memory:dd_",
        }
        geo_lyr = processing.run("native:reprojectlayer", params)["OUTPUT"]
        if self.debug:
            QgsProject.instance().addMapLayer(geo_lyr)
        return geo_lyr


    def poly_from_extent(self, layer):
        """Return polygon as coordinate list from layer's extent
        Ex:
            [(-142.0, 74.0), (-115.0, 74.0), (-115.0, 54.0), (-142.0, 54.0)]

        Adapted from
        https://gis.stackexchange.com/questions/245811/getting-layer-extent-in-pyqgis
        """
        ext = layer.extent()
        xmin = ext.xMinimum()
        xmax = ext.xMaximum()
        ymin = ext.yMinimum()
        ymax = ext.yMaximum()
        return [(xmin, ymax), (xmax, ymax), (xmax, ymin), (xmin, ymin)]


    def hexes_within_layer_extent(self, layer, level):
        """Return list of HexID within layer's extent
        In: qgis layer object, hex resolution level (0-15)
        Out: ['8412023ffffffff', '84029d5ffffffff', '8413a93ffffffff']
        """
        ext_poly = self.poly_from_extent(layer)
        hex_ids = set(h3.polyfill_polygon(ext_poly, res=level, lnglat_order=True))
        self.log(f"Hex IDs within extent poly: {str(len(hex_ids))}")
        return hex_ids

    def run(self, res, two_binning_levels):
        print('Run Function, res = ' + str(res))
        geo_layer = self.proj_to_geo(self.mylayer)

        levels = 1 
        if two_binning_levels is True:
            levels = 2

        # For each resolution level fetch geometry of each hex feature and write to shapefile with id
        # We produce two levels of binning to cater for different levels of user privilege
        # one user provided, and the other with 1 added on it 

        # 26 may 2024. We just do one
        # https://gis.stackexchange.com/questions/342352/apply-a-color-ramp-to-vector-layer-using-pyqgis3

        for res in range(res, res + levels):  # (previously) for res in range(res, res + 2):
            self.log("Resolution: {res}")
            fields = QgsFields()
            fields.append(QgsField("id", QVariant.String))
            shpfile = os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}.shp")
            #shpfile = os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}.shp")
            print("shpfile 1: " + str(shpfile))
            
            writer = QgsVectorFileWriter(
                shpfile, "UTF8", fields, QgsWkbTypes.Polygon, driverName="ESRI Shapefile"
            )
            
            features = []
            
            for id in set(self.hexes_within_layer_extent(geo_layer, res)):
                f = QgsFeature()
                f.setGeometry(
                    QgsGeometry.fromPolygonXY(
                        [
                            # note reversing back to X,Y
                            [QgsPointXY(c[1], c[0]) for c in h3.h3_to_geo_boundary(id)]
                        ]
                    )
                )
                f.setAttributes([id])
                if self.debug:
                    self.log(f"Hex: {id} " + str(h3.h3_to_geo_boundary(id)))
                features.append(f)
            writer.addFeatures(features)
            del writer
            self.log("Features out: " + str(len(features)))

            print(os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}.shp") )
            print(os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}_count.shp") )

            print("Here x")
            print("shpfile 2: " + str(shpfile))
            # shpfile D:\datasets\hexabinned_datasets/all_clusters_kamloops — all_clusters_kamloops.shp_Hex_6.shp
            print("CRS " + str(self.geo_csrs))
            #shpfile = "D:\datasets\all_clusters_kamloops.zip"

            processing.run("qgis:definecurrentprojection", {"INPUT": shpfile, "CRS": self.geo_csrs})
                       
            # https://github.com/ThomasG77/30DayMapChallenge/blob/master/day4_hexagons/data/h3-processing.py

            try:
                #lets try adding the count function
                processing.run('qgis:countpointsinpolygon', {
                    'CLASSFIELD' : None,
                    'FIELD' : 'numpoints',
                    # polygons are the input file, and they should be in the same folder as the output
                    #'POLYGONS': os.path.join(self.working_directory, "data/hexagon_" + str(res) + ".shp"), 
                    'POLYGONS': os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}.shp"),
                    'OUTPUT' : os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}_count.shp"),
                    'POINTS' : self.mylayer, #"all_clusters_kamloops", #mylayer,
                    'WEIGHT' : None
                })
            except Exception as e:
                print(f"Error during calling 'processing.run()' function + {e}")
                QMessageBox.information(None, "DEBUG:", 'Error processing ')

            print('Processing Run2 ')

            #layer = QgsVectorLayer(shpfile, f"{self.out_filename_prefix} {res}", "ogr")
            #QgsProject.instance().addMapLayer(layer)

            # # load the count layer in qgis
            # #count_shpfile = os.path.join(self.dataPath, f"{self.out_filename_prefix}_{res}.shp")
            # count_shpfile = os.path.join(self.dataPath, f"{self.out_filename_prefix}_{res}_count.shp")
            # count_layer = QgsVectorLayer(count_shpfile, f"{self.out_filename_prefix} {res}", "ogr")
            # QgsProject.instance().addMapLayer(count_layer)
            count_shpfile = os.path.join(self.dataPath, f"{self.out_filename_prefix}{res}_count.shp")
            count_layer = QgsVectorLayer(count_shpfile, f"{self.out_filename_prefix}{res}", "ogr")
            QgsProject.instance().addMapLayer(count_layer)


    # END BINNING