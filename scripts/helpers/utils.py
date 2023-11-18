import os
import shutil
import tempfile
import zipfile
import pandas as pd
import geopandas as gpd


def save_coordinates_to_csv(coordinates: list, output_file: str):
    """
    Save a list of coordinates to a CSV file.

    :param coordinates: List of coordinates in the format [(latitude, longitude), ...].
    :param output_file: Location of the output file to save the coordinates.
    """
    df = pd.DataFrame(coordinates, columns=['LATITUDE', 'LONGITUDE'])
    df.to_csv(output_file, index=False)


def filter_shapefile_by_parameters(input_shapefile, parameter_tuple, output_zipfile):
    column_name, parameter_list = parameter_tuple

    gdf = gpd.read_file(input_shapefile)

    filtered_features = []

    for param_value in parameter_list:
        filtered_features.extend(gdf[gdf[column_name].isin([param_value])].to_dict(orient='records'))

    filtered_gdf = gpd.GeoDataFrame(filtered_features)

    filtered_gdf = filtered_gdf.set_crs('EPSG:4326')

    temp_dir = tempfile.mkdtemp()
    temp_shapefile = os.path.join(temp_dir, 'filtered_shapefile.shp')

    filtered_gdf.to_file(temp_shapefile)

    with zipfile.ZipFile(output_zipfile, 'w') as zipf:
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))

    shutil.rmtree(temp_dir)