import csv
import numpy as np
import pandas as pd
from geopy.distance import geodesic
import geopandas as gpd
from shapely.geometry import Point


def generate_grid(border_points_location_file1, shapefile, output_file, distance):

    """
    This function generates dots within the border points at the specified distance apart, filters them
    through the provided shapefile, and returns only those that fall within the shape. The result
    contains the coordinates of the filtered dots.

    :param border_points_location_file1: Points for the northwestern, southwestern, northeastern and southeastern border point
    :param distance: Distance between the generated dots (in longitude and latitude)
    :param shapefile: The file path to the shapefile containing the geographical boundaries of the USA,
                            used to filter the generated dots.
    :param output_file: The file path where the result, containing the coordinates of the filtered dots, will be written.

    :return: Result is written in a csv file that is provided in the function
    """

    border_points = pd.read_csv(border_points_location_file1)

    northwestern = tuple(border_points.iloc[0, [0, 1]])
    southwestern = tuple(border_points.iloc[1, [0, 1]])
    northeastern = tuple(border_points.iloc[2, [0, 1]])

    geography = gpd.read_file(shapefile).to_crs("EPSG:4326")

    lat_distance_miles = geodesic(northwestern, southwestern).miles
    lat_total_dots = int(lat_distance_miles / distance) + 1
    lat_step = (northwestern[0] - southwestern[0]) / (lat_total_dots - 1)
    latitudes = np.arange(northwestern[0], southwestern[0] - 0.1, -lat_step)

    lon_distance_miles = geodesic(northwestern, northeastern).miles
    lon_total_dots = int(lon_distance_miles / distance) + 1
    lon_step = (northeastern[1] - northwestern[1]) / (lon_total_dots - 1)
    longitudes = np.arange(northwestern[1], northeastern[1] + 0.1, lon_step)

    lat_grid, lon_grid = np.meshgrid(latitudes, longitudes)

    points = np.array([lat_grid.ravel(), lon_grid.ravel()]).T

    dots_df = pd.DataFrame(points, columns=['Latitude', 'Longitude'])

    geometry = [Point(xy) for xy in zip(dots_df['Longitude'], dots_df['Latitude'])]
    dots_gdf = gpd.GeoDataFrame(dots_df, geometry=geometry)

    dots_gdf.crs = "EPSG:4326"

    dots_inside_shapefile = gpd.sjoin(dots_gdf, geography, how="inner", predicate='within')

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Latitude', 'Longitude'])
        writer.writerows(dots_inside_shapefile[['Latitude', 'Longitude']].values)


if __name__ == "__main__":

    shapefile_path = '../res/COUNTY-2020-US-SL050-Coast-Clipped/COUNTY_2020_US_SL050_Coast_Clipped.shp'
    border_points_location_file = '../res/border_grid_points.csv'
    output_file_path = '../res/filtered_dots_coordinates.csv'

    dot_distance_miles = 100
    generate_grid(border_points_location_file, shapefile_path, output_file_path, dot_distance_miles,)
