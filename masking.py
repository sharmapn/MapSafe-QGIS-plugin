from qgis.core import QgsVectorLayer, QgsGeometry, QgsFeature, QgsProject, QgsSpatialIndex   

from random import uniform
from math import pi, sin, cos
from datetime import datetime

import time  

from tqdm import tqdm

from PyQt5.QtGui import QColor

class GeoMasking:
    def geomasking_each_point(self, geom: QgsGeometry, min_distance, max_distance) -> QgsGeometry:
        """
        Translates point geometry at a random angle and random distance within a range [min_distance : max_distance]
        Parameters:
        ==========
        :param geom: the feature's geometry
        :param min_distance: the minimum distance
        :param max_distance: the maximum distance
        """
        angle = uniform(0, 2*pi)
        distance = uniform(min_distance, max_distance)
        dx = distance * cos(angle)
        dy = distance * sin(angle)
        geom.translate(dx, dy)

        return geom

    def count_points_in_layer(self, layer):
        point_lyr = QgsProject.instance().mapLayersByName(layer)[0]
        count = 0

        for feat in point_lyr.getFeatures():
            count = count + 1            
        print("Points in Layer: " + str(count))

        return count
    
    def distance_to_nearest_point_in_all_features(self,  masked_geom, sp_idx, input_layer):
        #nearestPoint = turf.nearestPoint(currentFeatureMasked, sensitive.data)
        # Find nearest point to current geom (returns feature id)
        # (default is 1 but you can add additional arguments for number of neighbors/max search distance)
        nn_id = sp_idx.nearestNeighbor(masked_geom)
        #print(f'Nearest neighbor ID: {nn_id}')
        nn = input_layer.getFeature(nn_id[0])
        nn_geom = nn.geometry()
        # We can also find the distance to the current point
        # This will return cartesian distance in the layer's CRS units
        nearestPoint = masked_geom.distance(nn_geom)
        #### print(f'Distance to nearest neighbor: {nearestPoint}')
        # Insert the current feature back into the spatial index
        
        return nearestPoint
    
    def geomasking_function(self, layerName, minimum_distance, maximum_distance, 
                            calculate_sp_measure, two_geomasking_levels,
                            min_offset, max_offset,label_privacy_rating, label_masking_time,
                            progress, safeguard_progressBar, add_layer_to_canvas):
       
        privacy_rating = 0
        print("minimum_distance received: " + str(minimum_distance))
        print("maximum_distance received: " + str(maximum_distance))

        current = time.time()
        print ('##### start ' + str(current))

        input_layer = QgsProject.instance().mapLayersByName(layerName)[0]  #"all_clusters_kamloops"  
        little_masked = layerName + "_masked"
        # creating a new layer for the output
        output_layer = QgsVectorLayer(f"Point?crs={input_layer.crs().authid()}&index=yes", little_masked, "memory")
        # accessing output layer provider
        provider = output_layer.dataProvider()
        provider.addAttributes(input_layer.fields())
        output_layer.updateFields()
        # Create a QgsSpatialIndex instance & load layer features
        sp_idx = QgsSpatialIndex(input_layer.getFeatures())
        sp_idx_more = QgsSpatialIndex(input_layer.getFeatures())
        spruill = []  # spruill measure
        spruill_more = []  # spruill measure

        # perform the same for two levels masking
        if two_geomasking_levels is True:
            more_masked = layerName + "_moremasked" 
            output_layer_more = QgsVectorLayer(f"Point?crs={input_layer.crs().authid()}&index=yes", more_masked, "memory")
            provider_more = output_layer_more.dataProvider()
            # inheriting data from the original layer      
            provider_more.addAttributes(input_layer.fields())
            output_layer_more.updateFields()  
            sp_idx_two_levels = QgsSpatialIndex(input_layer.getFeatures())
            spruill_two_levels = []  # spruill measure     

        feature_count = self.count_points_in_layer(layerName) 
        feature_count_more = feature_count #self.count_points_in_layer(layerName) 
        print('count_points_in_layer ' + str(feature_count))

        # processing new features
        # count features - for progress bar
        # Full explanation how to implment TQDM
        # https://github.dev/stjordanis/mhn-react/blob/a17bacd146507d6303595b97c97f2df601d556be/mhnreact/molutils.py#L514

        pbar_counter = 0  
        progress.setMaximum(feature_count)
        print('Set feature count ' + str(feature_count))

        # https://gis.stackexchange.com/questions/62053/how-to-add-layer-raster-with-specific-position-in-the-qgis-layer-list
        #root = QgsProject.instance().layerTreeRoot()

        for original_feat in input_layer.getFeatures():
            # providing geometry
            masked_feat = QgsFeature()            
            masked_geom = self.geomasking_each_point(original_feat.geometry(), minimum_distance, maximum_distance)               
            masked_feat.setGeometry(masked_geom)
            # providing attributes
            masked_feat.setAttributes(original_feat.attributes())
            # adding new feature to the output layer
            provider.addFeature(masked_feat)
            if two_geomasking_levels is True:
                masked_feat_more = QgsFeature()
                minimum_distance2 = minimum_distance + min_offset
                maximum_distance2 = maximum_distance + max_offset
                masked_geom_more = self.geomasking_each_point(original_feat.geometry(), minimum_distance2, maximum_distance2)
                masked_feat_more.setGeometry(masked_geom_more)
                masked_feat_more.setAttributes(original_feat.attributes())
                provider_more.addFeature(masked_feat_more)

            # Remove current feature so nn search doesn't just return itself
            # sp_idx.deleteFeature(original_feat)
            # sp_idx.deleteFeature(new_feat)
            
            if(calculate_sp_measure is True): 
                nearestPoint = self.distance_to_nearest_point_in_all_features(masked_geom, sp_idx, input_layer)
                # create a spatial index for just oen feature
                sp_idx_one_point = QgsSpatialIndex()
                sp_idx_one_point.insertFeature(original_feat)
                actualDist = self.distance_to_nearest_point_in_all_features(masked_geom, sp_idx_one_point, input_layer )
                ## print('nearestPoint ' + str(nearestPoint) + ' actualDist ' + str(actualDist))
                # actualDist   = turf.nearestPoint(currentFeatureMasked, currentFeature)
                #actualDist   =  self.distanceToNearestPoint(masked_geom, original_feat , sp_idx, input_layer )
                if (nearestPoint == actualDist):
                     spruill.append("yes")
                     #print('spruill appended ')

                if two_geomasking_levels is True:
                    #print('Two levels chosen')
                    nearestPoint_more = self.distance_to_nearest_point_in_all_features(masked_geom_more, sp_idx_more, input_layer)
                    # create a spatial index for just oen feature
                    sp_idx_one_point_more = QgsSpatialIndex()
                    sp_idx_one_point_more.insertFeature(original_feat)
                    actualDist_more = self.distance_to_nearest_point_in_all_features(masked_geom_more, sp_idx_one_point_more, input_layer )
                    # print('nearestPoint ' + str(nearestPoint) + ' actualDist ' + str(actualDist))
                    # actualDist   = turf.nearestPoint(currentFeatureMasked, currentFeature)
                    # actualDist   =  self.distanceToNearestPoint(masked_geom, original_feat , sp_idx, input_layer )
                    if (nearestPoint_more == actualDist_more):
                        spruill_more.append("yes")
                        #print('spruill appended ')     
                       
            # Insert the current feature back into the spatial index
            #sp_idx.insertFeature(original_feat)
            #while pbar_counter < 100:
            pbar_counter = pbar_counter + 1
            progress.setValue(pbar_counter)
            
        if add_layer_to_canvas:
            # adding new layer to the map
            QgsProject.instance().addMapLayer(output_layer)
            output_layer.renderer().symbol().setColor(QColor("#8fff49"))      # path_to_decrypt
            #root.insertLayer(1, output_layer)
        
        if two_geomasking_levels is True:
            QgsProject.instance().addMapLayer(output_layer_more)
            output_layer_more.renderer().symbol().setColor(QColor("#f6e016"))       # path_to_decrypt
            #root.insertLayer(2, output_layer)
                
        if (calculate_sp_measure is True):
            ##print('( (len(spruill)/2 ) ) ' + str( (len(spruill)/2 ) ) )
            ##print('( (len(spruill)/2 ) / count) ' + str( (len(spruill)/2 ) / count) )
            #Do Spruill's Measure and turn on stats divs
            #sensitive.length = Object.keys(sensitive.data.features).length; #find the number of points in the sensitive layer
            spruill_measure = ( 100 - (( (len(spruill)/2 ) / feature_count) * 100)); #calculate spruill's measure
            ##print('(( (len(spruill)/2 ) / count) * 100) ' + str(    (( (len(spruill)/2 ) / count) * 100)    ))
            ##print('spruill_measure ' + str(spruill_measure))
            #Do HTML edits to insert spruill's measure, show the privacy rating element, show the center movement element, and edit the text in the masking button
            #print("Privacy Rating: " +  str(round(spruill_measure) ) + "/100 (higher is better)")
            privacy_rating = round(spruill_measure, 2)
            print("Privacy Rating: " +  str(privacy_rating)  + "/100 (higher is better)")
            label_privacy_rating.setStyleSheet("background-color: lightgreen") 
            label_privacy_rating.setText( str(privacy_rating)  + "/100 (higher is better)" )
        #self.get_layers()


            if two_geomasking_levels is True:
                print('Two levels chosen D')
                spruill_measure_more = ( 100 - (( (len(spruill_more)/2 ) / feature_count_more) * 100)); #calculate spruill's measure
                print("Privacy Rating More: " +  str( round(spruill_measure_more, 2) )  + "/100 (higher is better)")
                #label_privacy_rating.setStyleSheet("background-color: lightgreen") 
                #label_privacy_rating.setText( str( round(spruill_measure, 2) )  + "/100 (higher is better)" )

        end = time.time()
        print('end ' + str(end))
        diff = end - current

        print('diff ' + str(diff))
        #label_masking_time.setStyleSheet("background-color: lightgreen") 
        label_masking_time.setText( " Completed "+ str( round(diff, 2) )  + " seconds." )
        safeguard_progressBar.setValue(33)  

        return privacy_rating  # privacy rating (for the first level)